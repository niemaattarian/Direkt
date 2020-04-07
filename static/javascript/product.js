/* Incrementing and Decrementing buttons for ingredients */
function reevaluate_ability(button) {
    const MAX_QUANTITY = 2;
    const MIN_QUANTITY = 0;

    let quantity = parseInt(button.parentElement.getElementsByClassName("quantity")[0].innerText);
    const add_button = document.getElementsByClassName("add-ingredients")[0];
    const remove_button = document.getElementsByClassName("remove-ingredients")[0];

    /* Incrementing value if '+' button is selected */
    if (button.classList.contains('add-ingredients')) {
        if (quantity < MAX_QUANTITY) {
            quantity += 1;
            remove_button.disabled = false;
        /* Disable button if max quantity is reached */
        } else {
            add_button.disabled = true;
        }
    }

    /* Decrementing value if '+' button is selected */
    else if (button.classList.contains('remove-ingredients')) {
        if (quantity > MIN_QUANTITY) {
            quantity -= 1;
            add_button.disabled = false;
        } else {
            remove_button.disabled = true;
        }
    }

    button.parentElement.getElementsByClassName("quantity")[0].innerText = quantity;
}

Array.from(document.getElementsByClassName("remove-ingredients")).forEach(function (element) {
    element.addEventListener('click', () => {
        reevaluate_ability(element);
    });
});
Array.from(document.getElementsByClassName("add-ingredients")).forEach(function (element) {
    element.addEventListener('click', () => {
        reevaluate_ability(element);
    });
});

/* Serializing  */
const product = {
    title: document.getElementById('product-name').innerText,
    ingredients: []
};

/* Confirm button */
function store() {
    Array.from(document.getElementsByClassName("ingredient")).forEach(function (element) {
        product.ingredients.push({
            title: element.getElementsByClassName('ingredient-description')[0].innerText,
            quantity: element.getElementsByClassName('quantity')[0].innerText,
        });
    });

    /* Converting to JSON */
    cart = JSON.parse(window.sessionStorage.getItem("cart")) || [];
    cart.push(product);
    window.sessionStorage.setItem("cart", JSON.stringify(cart));

    alert(product.title + " Added");
}