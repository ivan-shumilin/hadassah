import logging

from doctor.logic.create_ingredient import create_ingredients, add_ingredient_in_tkk
from nutritionist.functions.ttk import write_ttk_in_bd

logging = logging.getLogger('main_logger')


def update_ttk():
    logging.info('Start updating ttk')
    create_ingredients()
    logging.info('Successfully updated ttk')
    write_ttk_in_bd()
    logging.info('Writing ttk in bd')
    add_ingredient_in_tkk()
    logging.info('Add ttk in bd')

