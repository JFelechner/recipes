
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask import flash


import re

from flask_app.models.user_model import User
# the regex module
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.prep_time = data['prep_time']
        self.date_created = data['date_created']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator = None




    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 1 or len(data['name']) > 100:
            is_valid = False
            flash("Recipe name should be between 1 & 100 characters")

        if len(data['description']) < 1 or len(data['description']) > 255:
            is_valid = False
            flash("Description name should be between 1 & 250 characters")

        if len(data['instruction']) < 1 or len(data['instruction']) > 255:
            is_valid = False
            flash("Instruction name should be between 1 & 2500 characters")

        if len(data['date_created']) != 10:
            is_valid = False
            flash("Please provide a valid date")

        return is_valid
        




    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, prep_time, date_created, creator_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(prep_time)s, %(date_created)s, %(creator_id)s);"
        result = connectToMySQL('recipes').query_db(query, data)
        return result




    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for item in results:
            new_recipe = cls(item)
            new_user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at']
            }
            new_user = User(new_user_data)
            new_recipe.creator = new_user
            recipes.append(new_recipe)
        return recipes




    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        recipe = cls(result[0])
        new_user_data = {
            'id' : result[0]['users.id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        new_user = User(new_user_data)
        recipe.creator = new_user
        return recipe



    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, prep_time = %(prep_time)s, date_created = %(date_created)s WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)



    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL('recipes').query_db(query, data)





