import csv
import locale
import logging
import os
import re
from pathlib import Path
from datetime import datetime

from Menu.datatypes import MenuItem, Ingredient
from Menu.util import CopyOnFetchDict

locale.setlocale(locale.LC_ALL, 'en_IE.utf8')
LOG_DIRECTORY = Path('logs')
CONFIG_DIRECTORY = Path('config')

INGREDIENTS = {}

MENU_ITEMS = CopyOnFetchDict()

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

if os.path.isfile(LOG_DIRECTORY / 'direkt-latest.log'):
    with open(LOG_DIRECTORY / 'direkt-latest.log', 'r') as latest_logfile:
        timestamp = next(iter(re.findall(r'\d{2}-\w*-\w{4} \d{2}:\d{2}:\d{2}', latest_logfile.readline())), None)
        if timestamp is not None:
            os.rename(LOG_DIRECTORY / 'direkt-latest.log', LOG_DIRECTORY / f'direkt-{timestamp}.log')

logging.basicConfig(
    filename=LOG_DIRECTORY / 'direkt-latest.log',
    filemode='w',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)
logging.info(f'Started {datetime.now().strftime("%d-%b-%Y %H:%M:%S")}')

# Load all Ingredients form disk
ingredients_file = CONFIG_DIRECTORY / 'Menu - Ingredients.csv'
with open(ingredients_file, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

    logging.info('Loading Ingredients:')
    for ln, row in enumerate(reader):
        ingredient = dict(zip(headers, row))
        if all(key in ingredient for key in ['Title', 'Price']):
            INGREDIENTS[ingredient['Title']] = Ingredient.factory(title=ingredient['Title'],
                                                                  cost=float(ingredient['Price']))
            logging.debug(f'Added ingredient: {ingredient["Title"]}')
        else:
            logging.warning(f'Unable to parse ingredient file "{ingredients_file.absolute()}" line {ln}')

# Load all Menu Items from disk
menu_items_file = CONFIG_DIRECTORY / 'Menu - Menu Items.csv'
with open(menu_items_file, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

    logging.info('Loading Menu Items:')
    item_title = item_price = item_category = None
    item_ingredients = set()

    for ln, row in enumerate(reader):
        menu_item = dict(zip(headers, row))

        if all(key in menu_item for key in ['Title', 'Price', 'Path', 'Ingredient', 'Quantity']):

            if all([menu_item[k] != '' for k in ['Title', 'Price', 'Path']]):
                if all([e is not None for e in [item_title, item_price, item_category]]):
                    f = MenuItem(
                        title=item_title,
                        base_cost=float(item_price),
                        ingredients={INGREDIENTS[e[0]](included_in_price=e[1], quantity=e[1]) for e in item_ingredients}
                    )

                    MENU_ITEMS.set_by_path([p.strip() for p in item_category.split('->')], f)

                    logging.debug(f'Added Menu Items: {item_title}')

                    item_ingredients.clear()

                item_title = menu_item['Title']
                item_price = menu_item['Price']
                item_category = menu_item['Path']

            elif all([menu_item[k] != '' for k in ['Ingredient', 'Quantity']]):
                if menu_item['Ingredient'] in INGREDIENTS:
                    item_ingredients.add((menu_item['Ingredient'], int(menu_item['Quantity'])))
                else:
                    logging.warning(
                        f'Unable to parse {item_title} from file "{menu_items_file.absolute()}" line {ln}: "{menu_item["Ingredient"]}" not found!')
                    item_title = None
                    item_price = None
                    item_ingredients.clear()

        else:
            logging.warning(f'Unable to parse Menu Items file "{menu_items_file.absolute()}" line {ln}')

    if item_title is not None and item_price is not None and item_price is not None:
        f = MenuItem(
            title=item_title,
            base_cost=float(item_price),
            ingredients={
                INGREDIENTS[title](included_in_price=quantity, quantity=quantity) for title, quantity in
                item_ingredients
            }
        )

        MENU_ITEMS.set_by_path([p.strip() for p in item_category.split('->')], f)
        logging.debug(f'Added Menu Items: {item_title}')
        item_ingredients.clear()
