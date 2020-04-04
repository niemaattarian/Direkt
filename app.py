from flask import Flask, render_template

from Menu import MENU_ITEMS

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', links=MENU_ITEMS)


@app.route('/product')
def product():
    return render_template('product.html', product=MENU_ITEMS['Burgers']['Beef']['Big Mac'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
