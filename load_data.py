import pandas as pd
import datetime


def load_data():
    # TODO: load diff files acc to month.
    bf_menu = pd.read_csv('bf_menu.csv')
    dinz_menu = pd.read_csv('dinz_menu.csv')
    return bf_menu, dinz_menu


def format_date(tdy_raw):
    tdy_str = format(tdy_raw, '%Y-%m-%d')
    return tdy_str


def format_menu(menu):
    dtime = str(datetime.datetime.today() + datetime.timedelta(hours=8))
    res = menu.dropna().to_string(index=False, header=False, na_rep="")

    words_to_bold = ['Breakfast', 'Dinner']
    words_to_italicized = ['Choose 1', 'Drinks', 'Meat', 'Side Dish', '-Soup-', 'Main', 'Vegetable', 'Dessert', 'Set A', 'Set B']
    res.replace(" ", "")
    for word in words_to_bold:
        res = res.replace(word, '*{0}*'.format(word.upper()))
    for word in words_to_italicized:
        res = res.replace(word, '_{0}_\n'.format(word))
    res = res.replace("/restart", "")
    res = res.replace("  ", "")
    res = res.replace("\n ", "\n")
    return res + "\n "


def get_indv_menus(type, raw_date):
    if type == 'Breakfast':
        overall_menu = bf_menu
    elif type == 'Dinner':
        overall_menu = dinz_menu
    try:
        dateStr = format_date(raw_date + datetime.timedelta(hours=8))
        res = dateStr + "\n" + format_menu(overall_menu[dateStr])
        return res
    except:
        return "None available "
