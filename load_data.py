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
    res = menu.to_string(index=False, header=False, na_rep="")

    words_to_bold = ['Breakfast', 'Dinner']
    words_to_italicized = ['Choose 1', 'Drinks', 'Meat', 'Side Dish', 'Vegetable', 'Dessert']
    res.replace(" ","")
    for word in words_to_bold:
        res =res.replace(word, '*😊' + word.upper() + '😊*')
    for word in words_to_italicized:
        res = res.replace(word, '_-' + word + '_-')
    res = res.replace("/restart","")
    res = res.replace("  ","")
    return res

def get_indv_menus(overall_menu, day):
  try:
    return format_menu(overall_menu[day])
  except:
    return "None available"

tdy_raw = datetime.datetime.today()
tdy = format_date(tdy_raw)
tmr = format_date(tdy_raw + datetime.timedelta(days=1))
bf_menu, dinz_menu = load_data()

def get_all_menus():
  tdy_bf_m = get_indv_menus(bf_menu,tdy)
  tdy_din_m = get_indv_menus(dinz_menu, tdy)
  tmr_bf_m = get_indv_menus(bf_menu, tmr)
  tmr_din_m = get_indv_menus(dinz_menu, tmr)
  return tdy_bf_m, tdy_din_m, tmr_bf_m, tmr_din_m 