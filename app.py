import urllib.parse

from flask import Flask, render_template, redirect
from Menu import MENU_ITEMS

app = Flask(__name__)





@app.route('/')
def home():
    return render_template('index.html', links=MENU_ITEMS)


@app.route('/products/<product_name>')
def product(product_name):
    name = urllib.parse.unquote(product_name)
    product = MENU_ITEMS.get_item_by_title(name)

    if product is not None:
        return render_template('product.html', product=product)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
