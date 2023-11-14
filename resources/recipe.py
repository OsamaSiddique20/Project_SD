import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe


class RecipeListResource(Resource):

    def get(self):
        data = Recipe.get_all()

        if data is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        recipe = Recipe(name=data['name'],
                        description=data['description'],
                        num_of_servings=data['num_of_servings'],
                        cook_time=data['cook_time'],
                        directions=data['directions'],
                        user_id=data["user_id"])
        recipe.save()

        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):

    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    def put(self, recipe_id):
        data = request.get_json()

        return Recipe.update(recipe_id, data)

    def delete(self, recipe_id):
        return Recipe.delete(recipe_id)


class RecipePublishResource(Resource):

    def put(self, recipe_id):
        return Recipe.publish(recipe_id)

    def delete(self, recipe_id):
        return Recipe.un_publish(recipe_id)
