from nutritionist.models import Report

rs = Report.objects.filter(
    date_create="2023-12-02",
    meal="lunch"
)

for r in rs:
    Report.objects.create(
        date_create="2023-12-02",
        meal="breakfast",
        user_id=r.user_id,
        type_of_diet=r.type_of_diet,
        category=r.category,
    )