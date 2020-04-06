import urllib.parse
from functools import reduce

from flask import Flask, render_template, redirect, request
from Menu import MENU_ITEMS, MenuItem

app = Flask(__name__)


@app.route('/')
def home():
    category = request.args.get('category', None)

    if category is not None:
        keys = [p.strip() for p in category.split('/')]

        try:
            path = list(reduce(lambda o, k: dict.__getitem__(o, k), keys, MENU_ITEMS))
            items = list(filter(lambda i: MENU_ITEMS.get_item_by_title(i) is not None, path))

            if len(items) > 0:
                return render_template('index.html', products=items)

            return render_template('index.html', links=path, path='/'.join(keys) + '/')
        except KeyError:
            return redirect('/')

    return render_template('index.html', links=MENU_ITEMS, path='')


@app.route('/products/<product_name>')
def product(product_name):
    name = urllib.parse.unquote(product_name)
    product = MENU_ITEMS.get_item_by_title(name)

    if product is not None:
        return render_template('product.html', product=product)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


