from doctor.logic.create_ingredient import create_ingredients, add_ingredient_in_tkk
from nutritionist.functions.ttk import write_ttk_in_bd

def update_ttk():
    create_ingredients()
    write_ttk_in_bd()
    add_ingredient_in_tkk()

