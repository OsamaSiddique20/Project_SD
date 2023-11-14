import sys
from extensions import db
from resources.user import UserListResource
from models.user import User
from http import HTTPStatus


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    num_of_servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    directions = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'num_of_servings': self.num_of_servings,
            'cook_time': self.cook_time,
            'directions': self.directions,
            'User': User.get_name_by_id(self.user_id)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.filter_by(is_publish=True).all()

        result = []

        for i in r:
            result.append(i.data)

        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter((cls.id == id) & (cls.is_publish == True)).first()
    
    @classmethod
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == False)).first()
        return x

    @classmethod
    def update(cls, id, data):
        recipe = cls.query.filter(cls.id == id).first()

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']
        db.session.commit()
        return recipe.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        recipe = cls.query.filter(cls.id == id).first()
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(recipe)
        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    @classmethod
    def publish(cls, recipe_id):
        recipe = Recipe.get_by_id_n(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True
        db.session.commit()
        return recipe.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False
        db.session.commit()
        return recipe.data, HTTPStatus.OK
