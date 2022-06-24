from flask import Flask, render_template, jsonify
import yaml

app = Flask(__name__)


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


@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/getRecipes')
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


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
