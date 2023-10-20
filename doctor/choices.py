TYPE_DEPARTMENT = (
    ('Не выбрано', 'Не выбрано'),
    ('Хирургия', 'Хирургия'),
    ('Онкология', 'Онкология'),
    ('Реанимация', 'Реанимация'),
    ('Интенсивная терапия', 'Интенсивная терапия'),
    ('Check-up', 'Check-up'),
    ('Ядерная медицина', 'Ядерная медицина')
)

ROOM_NUMBERS = (
    ('2а-1', '2а-1'),
    ('2а-2', '2а-2'),
    ('2а-3', '2а-3'),
    ('2а-4', '2а-4'),
    ('2а-5', '2а-5'),
    ('2а-6', '2а-6'),
    ('2а-7', '2а-7'),
    ('2а-8', '2а-8'),
    ('2а-9', '2а-9'),
    ('2а-10', '2а-10'),
    ('2а-11', '2а-11'),
    ('2а-12', '2а-12'),
    ('2а-13', '2а-13'),
    ('2а-14', '2а-14'),
    ('2а-15', '2а-15'),
    ('2а-16', '2а-16'),
    ('2а-17', '2а-17'),
    ('3а-1', '3а-1'),
    ('3а-2', '3а-2'),
    ('3а-3', '3а-3'),
    ('3а-4', '3а-4'),
    ('3а-5', '3а-5'),
    ('3а-6', '3а-6'),
    ('3а-7', '3а-7'),
    ('3а-8', '3а-8'),
    ('3а-9', '3а-9'),
    ('3а-10', '3а-10'),
    ('3а-11', '3а-11'),
    ('3а-12', '3а-12'),
    ('3а-13', '3а-13'),
    ('3а-14', '3а-14'),
    ('3а-15', '3а-15'),
    ('3а-16', '3а-16'),
    ('3а-17', '3а-17'),
    ('3b-1', '3b-1'),
    ('3b-2', '3b-2'),
    ('3b-3', '3b-3'),
    ('3b-4', '3b-4'),
    ('3b-5', '3b-5'),
    ('3b-6', '3b-6'),
    ('3b-7', '3b-7'),
    ('3b-8', '3b-8'),
    ('3b-9', '3b-9'),
    ('3b-10', '3b-10'),
)

BED = (
    ('K1', 'K1'),
    ('K2', 'K2'),

)

TYPE_DIET = (
    ('Не выбрано', 'Не выбрано'),
    ('ОВД', 'ОВД'),
    ('ОВД без сахара', 'ОВД без сахара'),
    ('ОВД веган (пост) без глютена', 'ОВД веган (пост) без глютена'),
    ('Нулевая диета', 'Нулевая диета'),
    ('ЩД', 'ЩД'),
    ('ЩД без сахара', 'ЩД без сахара'),
    ('БД', 'БД'),
    ('БД день 1', 'БД день 1'),
    ('БД день 2', 'БД день 2'),
    ('НБД', 'НБД'),
    ('ВБД', 'ВБД'),
    ('НКД', 'НКД'),
    ('ВКД', 'ВКД'),
    ('Безйодовая', 'Безйодовая'),
    ('ВКД', 'ВКД'),
    ('ПЭТ/КТ', 'ПЭТ/КТ'),
    ('Без ограничений', 'Без ограничений'),
    ('ОВД (Энтеральное питание)', 'ОВД (Энтеральное питание)'),
)

TYPE_DIET_FOR_FORM = (
    ('Не выбрано', 'Не выбрано'),
    ('ОВД', 'ОВД'),
    ('ОВД без сахара', 'ОВД без сахара'),
    ('ОВД веган (пост) без глютена', 'ОВД веган (пост) без глютена'),
    ('Нулевая диета', 'Нулевая диета'),
    ('ЩД', 'ЩД'),
    ('ЩД без сахара', 'ЩД без сахара'),
    ('БД день 1', 'БД день 1'),
    ('БД день 2', 'БД день 2'),
    ('НБД', 'НБД'),
    ('ВБД', 'ВБД'),
    ('НКД', 'НКД'),
    ('ВКД', 'ВКД'),
    ('Безйодовая', 'Безйодовая'),
    ('ПЭТ/КТ', 'ПЭТ/КТ'),
    ('Без ограничений', 'Без ограничений'),
)

TYPE_DIET_FOR_MENU = (
    ('ovd', 'ОВД'),
    ('ovd_sugarless', 'ОВД без сахара'),
    ('ОВД веган (пост) без глютена', 'ОВД веган (пост) без глютена'),
    ('Нулевая диета', 'Нулевая диета'),
    ('shd', 'ЩД'),
    ('ЩД без сахара', 'ЩД без сахара'),
    ('БД', 'БД'),
    # ('bd-2', 'БД день 2'),
    ('nbd', 'НБД'),
    ('vbd', 'ВБД'),
    ('nkd', 'НКД'),
    ('vkd', 'ВКД'),
    ('Безйодовая', 'Безйодовая'),
    ('ПЭТ/КТ', 'ПЭТ/КТ'),
    ('Без ограничений', 'Без ограничений'),
)


STATUS_PATIENT = (
    ('patient', 'patient'),
    ('patient_archive', 'patient_archive'),
)

TYPE_PAY = (
    ('petrushka', 'petrushka'),
    ('hadassah', 'hadassah'),
)

STATUS_BARCODES = (
    ('active', 'active'),
    ('no_active', 'no_active'),
)

DAT_OF_THE_WEEK = (
    ('понедельник', 'понедельник'),
    ('вторник', 'вторник'),
    ('среда', 'среда'),
    ('четверг', 'четверг'),
    ('пятница', 'пятница'),
    ('суббота', 'суббота'),
    ('воскресенье', 'воскресенье'),
)

MEALS = (
    ('breakfast', 'breakfast'),
    ('lunch', 'lunch'),
    ('afternoon', 'afternoon'),
    ('dinner', 'dinner'),
)

DAYS = (
    ('tomorrow', 'tomorrow'),
    ('after-tomorrow', 'after-tomorrow'),
)