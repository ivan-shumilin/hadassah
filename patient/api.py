from datetime import date, timedelta

from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.functions.bot import formatting_full_name
from doctor.functions.translator import translate_diet, get_day_of_the_week
from nutritionist.models import CustomUser, CommentProduct
from patient.functions import (
    create_menu_patient_for_the_day,
    creating_menu_for_patient,
    create_patient_select,
    del_if_not_garnish,
    del_if_not_product_without_garnish,
    ready_menu_for_dump,
)
from patient.serializers import CommentSerializer
from doctor.tasks import my_job_send_messang_changes


class PatientDetail(APIView):
    def get(self, request, user_id):
        ''' Возращает инфрмацию о пользователе: комментарий, ФИО, отделение, диету'''
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": f"Пациента с id {user_id} не существует",},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.status != "patient":
            return Response(
                {
                    "error": f"Пациент не имеет статус 'patient'. Его статус {user.status}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        comment = user.comment
        full_name = user.full_name
        department = user.department
        diet = user.type_of_diet

        data = {
            "comment": comment,
            "full_name": full_name,
            "department": department,
            "diet": diet,
        }

        return JsonResponse(data, status=status.HTTP_200_OK)


class PatientHistory(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                type=str,
                description="Date in YYYY-MM-DD format (default today)",
                required=False,
            )
        ],
        responses=JsonResponse,
    )
    def get(self, request, user_id):
        ''' возращает историю блюд пациента на опредленный день '''
        show_date = request.GET.get("date", date.today().isoformat())
        try:
            menu_on_show_date: dict = create_menu_patient_for_the_day(
                show_date, user_id
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return JsonResponse(menu_on_show_date, status=status.HTTP_200_OK)

    @extend_schema(request=CommentSerializer)
    def post(self, request, user_id):
        ''' Проставляет оценку на продукт '''
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get("product_id")
            rating = serializer.validated_data.get("rating")
            text = serializer.validated_data.get("text")
            get_date = serializer.validated_data.get("date")
            product_name = serializer.validated_data.get("product_name")
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse(
                    {"error": f"CustomUser with id {user_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return JsonResponse(
                    {"error with get user from database": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            try:
                comment = CommentProduct()
                comment.user_id = user
                comment.product_id = product_id
                comment.comment = text
                comment.rating = rating
                comment.save()

            except Exception as e:
                return JsonResponse(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            check_mark = "&#9989;"
            messange = f"{check_mark} <b>Отзыв на заказ от {get_date}\n</b>"
            messange += f"{formatting_full_name(user.full_name)}\n"
            messange += f"{product_name}\n"
            messange += f"Оценка {rating} из 5\n"
            messange += f"{text}\n"

            # my_job_send_messang_changes.delay(messange)

            return JsonResponse(
                {
                    "comment": comment.comment,
                    "text": text,
                    "rating": rating,
                    "product": product_name,
                },
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientMenuDetail(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                type=str,
                description="Date in YYYY-MM-DD format (default today)",
                required=False,
            )
        ],
        responses=JsonResponse,
    )
    def get(self, request, user_id):
        """ Возращает меню пацента на запрашиваемый день """

        date_get = request.GET.get("date", date.today().isoformat())

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # если у пользователя Нулевая диета или протертное питание или энтеральное питание, то выбор блюд не доступен
        if (
            user.type_of_diet in ["Нулевая диета"]
            or user.is_probe
            or user.is_pureed_nutrition
        ):
            return JsonResponse(
                {
                    "detail": "Invalid diet type.",
                    "error_message": f"Для диеты {user.type_of_diet} выбор блюд недоступен",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        diet, translated_diet, day_of_the_week = initialize_data_for_patient_menu(
            user, date_get
        )

        try:
            menu_for_lk_patient, fix_dishes = creating_menu_for_patient(
                date_get, diet, day_of_the_week, translated_diet, user
            )
        except Exception as e:
            return JsonResponse(
                {"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            patient_select: dict = create_menu_patient_for_the_day(
                date_get, user_id
            )
        except Exception as e:
            return JsonResponse(
                {"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # проверяем есть ли ганрир, если нет удаляем блюда, которые идут без гарнира
            menu_for_lk_patient = del_if_not_garnish(menu_for_lk_patient)

            # проверяем есть ли блюда в которым нужен гарнир, если нет, тогда удаляем гарниры из блюд cafe
            menu_for_lk_patient = del_if_not_product_without_garnish(
                menu_for_lk_patient
            )

            # сделаем словарь для дампа (всю информацию о продукти записываем в словарь)
            ready_menu_for_dump(menu_for_lk_patient)

            # если пациент выбрал сразу 2 блюда, то их надо вместе отобразить
            fix_dishes = ",".join(fix_dishes)
        except Exception as e:
            return JsonResponse(
                {"errors": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return JsonResponse(
            {"possible_choice_of_dishes_by_the_patient": menu_for_lk_patient,
             "current_patient_choice": patient_select,
             "fix_dishes": fix_dishes
             },
            status=status.HTTP_200_OK,
        )


def initialize_data_for_patient_menu(user, date_get):
    """ Определяем диету пациента, переводим диету, смотрит на день если диета БД"""

    # по БД через день одинаковое питание
    if user.type_of_diet == "БД день 1":
        day_of_the_week_bd = {
            str(date.today()): "понедельник",
            str(date.today() + timedelta(days=1)): "вторник",
            str(date.today() + timedelta(days=2)): "понедельник",
        }
    if user.type_of_diet == "БД день 2":
        day_of_the_week_bd = {
            str(date.today()): "вторник",
            str(date.today() + timedelta(days=1)): "понедельник",
            str(date.today() + timedelta(days=2)): "вторник",
        }

    diet = translate_diet(user.type_of_diet)
    translated_diet = user.type_of_diet

    if user.type_of_diet in ["БД день 1", "БД день 2"]:
        day_of_the_week = day_of_the_week_bd[date_get]
        diet = "bd"
        translated_diet = "БД"
    else:
        day_of_the_week = get_day_of_the_week(date_get)

    return diet, translated_diet, day_of_the_week
