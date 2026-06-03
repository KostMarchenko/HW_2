class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, val):
        val = float(val)
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self):
        return f"Ingredient(name='{self.name}', quantity={self.quantity}, unit='{self.unit}')"
    def __eq__(self, other):
        return (self.name == other.name and self.unit == other.unit)
class Recipe:
    def __init__(self,title, ingredients=None):
        self.title = title
        if ingredients is not None:
            self.ingredients = ingredients
        else:
            self.ingredients = []
    def add_ingredient(self, ingredient: Ingredient):
        for ingr in self.ingredients:
            if ingr == ingredient:
                ingr.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    @staticmethod
    def is_valid_ratio(ratio):
        if ratio > 0:
            return True
        return False
    def scale(self,ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Число должно быть больше 0")
        new_ingr = [Ingredient(ingr.name, ingr.quantity*ratio, ingr.unit) for ingr in self.ingredients]
        return Recipe(self.title, new_ingr)
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        ingr_str = ", ".join(str(ingr) for ingr in self.ingredients)
        return f"Блюдо: {self.title}, для его приготовления нужны: {ingr_str}"
class ShoppingList:
    def __init__(self):
        self._items = []
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        rec = recipe.scale(portions)
        for ingr in rec.ingredients:
            self._items.append((ingr,rec.title))
    def remove_recipe(self, title: str):
        for it in self._items[:]:
            if it[1] == title:
                self._items.remove(it)
    def get_list(self):
        ingr_dict = {}
        for it in self._items:
            ingr = it[0]
            key = (ingr.name, ingr.unit)
            if key in ingr_dict.keys():
                ingr_dict[key] += ingr.quantity
            else:
                ingr_dict[key] = ingr.quantity
        array = []
        for key in ingr_dict.keys():
            array.append(Ingredient(key[0],ingr_dict[key],key[1]))
        array.sort(key=lambda ingr: ingr.name)
        return array
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients = None):
        super().__init__(title,ingredients)
        self.diet_type = diet_type
    def scale(self, ratio: float):
        new_recipe = super().scale(ratio)
        return DietaryRecipe(new_recipe.title,self.diet_type,new_recipe.ingredients)
    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"