import logging

from doctor.logic.create_ingredient import create_ingredients, add_ingredient_in_tkk
from nutritionist.functions.ttk import write_ttk_in_bd

logging = logging.getLogger('main_logger')


def update_ttk():
    logging.info('Start updating ttk')
    try:
        create_ingredients()
    except Exception as e:
        logging.error(e)
    logging.info('Successfully updated ttk')
    try:
        write_ttk_in_bd()
    except Exception as e:
        logging.error(e)
    logging.info('Writing ttk in bd')
    try:
        add_ingredient_in_tkk()
    except Exception as e:
        logging.error(e)
    logging.info('Add ttk in bd')

