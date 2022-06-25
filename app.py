from flask import Flask, render_template, jsonify, request
import yaml

app = Flask(__name__)

main_recipe_data = {}

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
    build_recipe(request.form)
    print("Well we're here... we called the endpoint")
    return ""
# SERVICE ROUTES - END

# FUNCTIONS - START
def build_recipe(args):
    # Define Title and Servings
    recipe = {"Title": args.get("title"), "Servings": args.get("servings")}
    with open('/Users/devinswenson/PycharmProjects/recipe_book/static/test_yaml.yml', 'w') as file:
        yaml.dump(recipe, file)
    print(recipe)

def get_recipes(recipes=[]):
    with open('/Users/devinswenson/PycharmProjects/recipe_book/static/test_yaml.yml', 'r') as file:
        data = yaml.safe_load_all(file)
        for doc in data:
            recipe = doc
            recipes.append({
                "Title": recipe.get('Title'),
                "Servings": recipe.get('Servings')
            })
    return jsonify(recipes)

if __name__ == '__main__':
    app.run()
