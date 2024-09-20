import logging

from doctor.logic.create_ingredient import create_ingredients, add_ingredient_in_tkk
from nutritionist.functions.ttk import write_ttk_in_bd

logger = logging.getLogger('main_logger')

def update_ttk():
    logger.info("Создания ингридиентов")
    try:
        create_ingredients()
    except Exception as e:
        logger.error(e)

    logger.info("Начало записи ттк в БД")
    try:
        write_ttk_in_bd()
    except Exception as e:
        logger.error(e)

    logger.info("Начало добавление всекм ТТК связь с Ингридиент")
    try:
        add_ingredient_in_tkk()
    except Exception as e:
        logger.error(e)

