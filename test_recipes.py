import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe
def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"
def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"
def test_ingredient_eq_same_name_and_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 100, "г")
    assert ingredient1 == ingredient2
def test_ingredient_eq_different_name():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Чипсы", 500, "г")
    assert ingredient1 != ingredient2
def test_ingredient_eq_different_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 500, "кг")
    assert ingredient1 != ingredient2

def test_recipe_creation():
    ingredients = [Ingredient("Мука", 500, "г"),Ingredient("Сыр", 100, "г")]
    recipe = Recipe("Маргарита", ingredients)
    assert recipe.title == "Маргарита"
    assert recipe.ingredients == ingredients
def test_recipe_add_ingredient():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[0].unit == "г"
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 600.0
def test_recipe_scale_returns_new_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = recipe.scale(2)
    assert isinstance(scaled, Recipe)
    assert scaled is not recipe
def test_recipe_scale_multiplies():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = recipe.scale(2)
    assert scaled.ingredients[0].quantity == 1000.0
def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Пицца")
    with pytest.raises(ValueError):
        recipe.scale(-1)
def test_recipe_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 50, "г"))
    assert len(recipe) == 2

def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0
    assert result[0].unit == "г"
def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Пицца")
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1)
def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Пирог")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe2 = Recipe("Пицца")
    recipe2.add_ingredient(Ingredient("Сыр", 200, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)
    shopping_list.remove_recipe("Пирог")
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Сыр"
    assert result[0].quantity == 200.0
def test_shopping_list_remove_no_recipe():
    recipe = Recipe("Пирог")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    shopping_list.remove_recipe("Пицца")
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 500.0
def test_shopping_list_get_list_summ_sameingredients():
    recipe1 = Recipe("Пирог")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe2 = Recipe("Пицца")
    recipe2.add_ingredient(Ingredient("Мука", 300, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 800.0
    assert result[0].unit == "г"
def test_shopping_list_get_list_sorted_by_name():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Ананас", 200, "г"))
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Яйцо", 2, "шт"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    result = shopping_list.get_list()
    names = []
    for ingr in result:
        names.append(ingr.name)
    assert names == ["Ананас", "Мука", "Яйцо"]
def test_shopping_list_add_summ_2_lists():
    recipe1 = Recipe("Пирог")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe2 = Recipe("Пицца")
    recipe2.add_ingredient(Ingredient("Сыр", 200, "г"))
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    result_list = list1 + list2
    result = result_list.get_list()
    assert isinstance(result_list, ShoppingList)
    assert len(result) == 2
    names = []
    for ingr in result:
        names.append(ingr.name)
    assert names == ["Мука", "Сыр"]
def test_shopping_list_add_do_not_change_original_lists():
    recipe1 = Recipe("Пирог")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe2 = Recipe("Пицца")
    recipe2.add_ingredient(Ingredient("Сыр", 200, "г"))
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    result_list = list1 + list2
    assert len(list1.get_list()) == 1
    assert list1.get_list()[0].name == "Мука"
    assert len(list2.get_list()) == 1
    assert list2.get_list()[0].name == "Сыр"