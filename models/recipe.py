


from extensions import db
from http import HTTPStatus
class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(1000))  
    instructions = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    rating = db.Column(db.String(1000))

    @property
    def data(self):
        return {
            'recipe_id': self.recipe_id,
            'name': self.name,
            'ingredients': self.ingredients, 
            'instructions': self.instructions,
            'category': self.category,
            'rating': self.rating
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_all(cls):
        result = cls.query.all()
        return [recipe.data for recipe in result]
    
    @classmethod
    def get_by_id(cls,id):
        result = cls.query.filter(cls.id == id).first()
        return result.data if result else None
            
    @classmethod
    def update(cls, id, data):
        recipe = cls.query.filter_by(id=id).first()
        if not recipe:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.name = data.get('name', recipe.name)
        recipe.instructions = data.get('instructions', recipe.instructions)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        recipe.category = data.get('category', recipe.category)
        recipe.rating = data.get('rating', recipe.rating)
        db.session.commit()
        return recipe.data, HTTPStatus.OK
    @classmethod
    def delete(cls,id):
        recipe = cls.query.filter(cls.id == id).first()
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        db.session.delete(recipe)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT
    
    @classmethod
    def add(cls, data):
        new_recipe = cls(
            name=data['name'],
            instructions=data['instructions'],
            ingredients=data.get('ingredients'),
            category=data.get('category'),
            rating=data.get('rating')
        )
        db.session.add(new_recipe)
        db.session.commit()

        return {'name': new_recipe.name, 'instructions': new_recipe.instructions,'ingredients':new_recipe.ingredients,'category':new_recipe.category,'rating':new_recipe.rating}, 201

    
        