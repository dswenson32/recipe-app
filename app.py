from flask import Flask, render_template, jsonify, request, redirect
import yaml

app = Flask(__name__)


@app.route('/test-save')
def test_save():
    recipes = get_recipes().json
    save_recipes(recipes)
    return "It's done"


# WEB PAGE ROUTES - START
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recipe/<name>')
def get_recipe(name):
    return render_template('recipe.html', json_data=get_recipe(name))


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/edit/<name>')
def edit(name):
    return render_template('edit.html', json_data=get_recipe(name))


# WEBPAGE ROUTES - END

# SERVICE ROUTES - START
@app.route('/getRecipes')
def call_get_recipes():
    return get_recipes()


@app.route('/submit-recipe', methods=['POST', 'PUT'])
def submit_recipe():
    built_recipe = build_recipe(request.form)
    recipes = get_recipes().json
    if request.method == 'PUT':
        for recipe in recipes:
            if recipe.get("Title") == built_recipe.get("Title"):
                print("i found it!")
                recipes.remove(recipe)
                break
    recipes.append(built_recipe)
    save_recipes(recipes)
    return redirect('/')


# SERVICE ROUTES - END

# FUNCTIONS - START
def build_recipe(args):
    recipe = {"Title": str(args.get("title")), "Servings": str(args.get("servings")), "Ingredients": [],
              "Instructions": []}
    idx = 1
    while True:
        if str(args.get("quantity-" + str(idx))) == "None":
            break
        recipe["Ingredients"].append([str(args.get("quantity-" + str(idx))), str(args.get("measure-" + str(idx))),
                                      str(args.get("ingredient-" + str(idx)))])
        idx = idx + 1
    idx = 1
    while True:
        if str(args.get("direction-" + str(idx))) == "None":
            break
        recipe["Instructions"].append(str(args.get("direction-" + str(idx))))
        idx = idx + 1
    print(recipe)
    return recipe


def get_recipes():
    recipes = []
    with open('/Users/devinswenson/PycharmProjects/recipe_book_new/static/test_yaml.yml', 'r') as file:
        data = yaml.safe_load_all(file)
        for recipe in data:
            ingredients = []
            for ingredient in recipe.get("Ingredients"):
                entry = [ingredient[0], ingredient[1], ingredient[2]]
                ingredients.append(entry)
            recipes.append({
                "Title": recipe.get('Title'),
                "Servings": recipe.get('Servings'),
                "Ingredients": ingredients,
                "Instructions": recipe.get("Instructions")
            })
    return jsonify(recipes)


def get_recipe(name):
    with open('/Users/devinswenson/PycharmProjects/recipe_book_new/static/test_yaml.yml', 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            if doc.get('Title') == name:
                recipe = doc
                print(doc)
    json_data = {
        "Title": recipe.get('Title'),
        "Ingredients": recipe.get('Ingredients'),
        "Instructions": recipe.get('Instructions'),
        "Servings": recipe.get('Servings')
    }
    return json_data


def save_recipes(recipes):
    with open('/Users/devinswenson/PycharmProjects/recipe_book_new/static/test_yaml.yml', 'w') as file:
        yaml.safe_dump_all(recipes, file)
    print("recipes saved!")


if __name__ == '__main__':
    app.run()
