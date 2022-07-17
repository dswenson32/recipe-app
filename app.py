from flask import Flask, render_template, jsonify, request
import yaml

app = Flask(__name__)

main_recipe_data = []

@app.route('/oldtest')
def hello_world(recipe=None):
    with open('/Users/devinswenson/PycharmProjects/recipe_book/static/test_yaml.yml', 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            if doc.get('Title') == 'Sausage and Bean Ragout':
                recipe = doc
                print(doc)
    json_data = {
        "Title": recipe.get('Title'),
        "Ingredients": recipe.get('Ingredients'),
        "Instructions": recipe.get('Instructions'),
        "Servings": recipe.get('Servings')
    }
    return render_template('recipe.html', json_data=json_data)

# WEB PAGE ROUTES - START
@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/')
def home():
    return render_template('index.html')
# WEBPAGE ROUTES - END


# SERVICE ROUTES - START
@app.route('/getRecipes')
def call_get_recipes():
    return get_recipes()

@app.route('/submit-recipe', methods=['POST'])
def submit_recipe():
    print(request.form)
    built_recipe = build_recipe(request.form)
    print("Well we're here... we called the endpoint")
    main_recipe_data.append(built_recipe)
    return ""
# SERVICE ROUTES - END

# FUNCTIONS - START
def build_recipe(args):
    recipe = {"Title": str(args.get("title")), "Servings": str(args.get("servings")), "Ingredients": [], "Instructions": []}
    idx = 1
    while True:
        if str(args.get("quantity-" + str(idx))) == "None":
            break
        recipe["Ingredients"].append([str(args.get("quantity-" + str(idx))), str(args.get("measure-" + str(idx))), str(args.get("ingredient-" + str(idx)))])
        idx = idx+1
    idx = 1
    while True:
        if str(args.get("direction-" + str(idx))) == "None":
            break
        recipe["Instructions"].append(str(args.get("direction-" + str(idx))))
        idx = idx+1
    print(recipe)
    return recipe

def get_recipes(recipes=[]):
    with open('/Users/devinswenson/PycharmProjects/recipe_book/static/test_yaml.yml', 'r') as file:
        data = yaml.safe_load_all(file)
        for recipe in data:
            ingredients = []
            for ingredient in recipe.get("Ingredients"):
                entry = {"Quantity": ingredient[0], "Measure": ingredient[1], "Ingredient": ingredient[2]}
                ingredients.append(entry)
            recipes.append({
                "Title": recipe.get('Title'),
                "Servings": recipe.get('Servings'),
                "Ingredients": ingredients,
                "Instructions": recipe.get("Instructions")
            })
            main_recipe_data = recipes
    return jsonify(main_recipe_data)

if __name__ == '__main__':
    app.run()


 # with open('/Users/devinswenson/PycharmProjects/recipe_book/static/test_yaml.yml', 'w') as file:
    #     yaml.dump(recipe, file)