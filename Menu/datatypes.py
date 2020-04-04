import copy
from functools import partial
from typing import Dict, Set


class Ingredient:

    def __init__(self, title: str, cost: float, included_in_price=0, quantity=0):
        self.title = title
        self.cost = cost
        self.included_in_price = included_in_price
        self.quantity = quantity

    @staticmethod
    def factory(**kwargs):
        return partial(Ingredient, **kwargs)

    def __repr__(self):
        return self.title


class MenuItem:
    def __init__(self, title: str, base_cost: float, ingredients: Set[Ingredient]):
        self.title = title
        self.base_cost = base_cost
        self.ingredients: Dict[str, Ingredient] = {i.title: copy.deepcopy(i) for i in ingredients}

    @property
    def price(self):
        price = self.base_cost

        for ingredient in self.ingredients.values():
            if ingredient.quantity > ingredient.included_in_price:
                price += (ingredient.quantity - ingredient.included_in_price) * ingredient.cost

        return price

    def __str__(self):
        alterations = []

        for key, ingredient in self.ingredients.items():
            if ingredient.quantity == 0:
                alterations.append(f'NO {ingredient.title}!')
            elif ingredient.quantity > ingredient.included_in_price:
                alterations.append(f'+{ingredient.quantity - ingredient.included_in_price} {ingredient.title}')
            elif ingredient.quantity < ingredient.included_in_price:
                alterations.append(f'-{ingredient.included_in_price - ingredient.quantity} {ingredient.title}')

        if len(alterations) == 0:
            return self.title
        else:
            return f'{self.title} ({", ".join(alterations)})'

    def __repr__(self):
        return self.__str__()
