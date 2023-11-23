# test_app.py
import unittest
from flask import Flask, jsonify, render_template
from app import create_app
from models.recipe import Recipe

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_search_route(self):
    #     response = self.app.get('/search?search=1')
    #     self.assertEqual(response.status_code, 200)

    def test_add_recipe_route(self):
        response = self.app.get('/add-recipe')
        self.assertEqual(response.status_code, 200)

    def test_update_recipe_route(self):
        response = self.app.get('/update-recipe/17')
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe_route(self):
        response = self.app.get('/delete/17')
        self.assertEqual(response.status_code, 200)

class TestRecipeModel(unittest.TestCase):
    def setUp(self):
        # Set up your Flask app
        app = create_app()
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_add_recipe(self):
        data = {
            'name': 'Test Recipe',
            'instructions': 'Test Instructions',
            'ingredients': 'Test Ingredients',
            'category': 'Test Category',
            'rating': 5
        }
        response = self.app.post('/add-recipe', data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_recipe(self):
        recipe_id = 17
        data = {
            'name': 'Updated Recipe',
            'instructions': 'Updated Instructions',
            'ingredients': 'Updated Ingredients',
            'category': 'Updated Category',
            'rating': 4
        }
        response = self.app.post(f'/update-recipe/{recipe_id}', data=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe(self):
        recipe_id = 17
        response = self.app.get(f'/delete/{recipe_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
