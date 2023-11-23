from http import HTTPStatus
from flask import flash, request
import sys
from extensions import db
from flask import Flask, jsonify, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_restful import Api
from models.recipe import Recipe
from config import Config

def create_app():
    print("Hello", file=sys.stderr)
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)

    routes(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def routes(app):
    @app.route('/')

    def all():
        all_recipes = Recipe.get_all()
        
        return render_template('index.html', recipes=all_recipes)

    # @app.route('/recipes')

    @app.route('/search')
    def get_by_id():
        rid = request.args.get('search')
        if rid.isdigit():
            rid = int(rid)
            data = Recipe.get_by_id(rid)
            if data is None:
                return  {"Message":" recipe not found"}
            return render_template('search-recipe.html',recipes=data)
        return {"Message":"Entry type should be integer or number"}
    

    @app.route('/update-recipe/<int:recipe_id>', methods=["GET", "POST"])
    def update_recipe(recipe_id):
        if request.method == 'POST':
            name = request.form.get('name')
            instructions = request.form.get('instructions')
            ingredients = request.form.get('ingredients')
            category = request.form.get('category')
            rating = request.form.get('rating')

            data = {
                'name': name,
                'instructions': instructions,
                'ingredients': ingredients,
                'category': category,
                'rating': rating
            }

            response, status = Recipe.update(recipe_id, data)
            all_recipes = Recipe.get_all()
        
            return render_template('index.html', recipes=all_recipes)

        else:
            
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                return render_template("update.html", recipe=recipe)
            else:
                return jsonify({'message': 'Recipe not found'}), HTTPStatus.NOT_FOUND


    
    @app.route('/add-recipe', methods=["GET", "POST"])
    def add_recipe():
        if request.method == 'POST':
            name = request.form.get('name')
            instructions = request.form.get('instructions')
            ingredients = request.form.get('ingredients')
            category = request.form.get('category')
            rating = int(request.form.get('rating'))
            if not name or not instructions or not ingredients or not category or not rating:
                return jsonify({'message': 'All fields are required.'}), HTTPStatus.BAD_REQUEST

            data = {
                'name': name,
                'instructions': instructions,
                'ingredients': ingredients,
                'category': category,
                'rating': rating
            }

            response, status = Recipe.add(data)
            all()
            all_recipes = Recipe.get_all()
        
            return render_template('index.html', recipes=all_recipes)
            


        return render_template('add_recipe.html')
        
    @app.route("/delete/<int:recipe_id>")
    def delete_recipe(recipe_id):
        print(recipe_id)
        respones , status = Recipe.delete(recipe_id)

        all_recipes = Recipe.get_all()
    
        return render_template('index.html', recipes=all_recipes)


if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)