from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models import user_model

class recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long")
            is_valid = False
        
        
        if len(recipe['description']) < 10:
            flash("Description must be at least 3 characters long")
            is_valid = False

        if len(recipe['instructions']) < 3:
            flash("Instruction must be at least 3 characters long")
            is_valid = False

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long")
            is_valid = False

        if len(recipe['date']) < 3:
            flash("Please enter the Date")
            is_valid = False
        
        
        # if len(recipe['time']) < 3:
        #     flash("Please if Recipe is under 30minutes, check YES OR NO")
        #     is_valid = False
        
        return is_valid

    @classmethod
    def create_recipes(cls,data):
        query = '''
        INSERT INTO recipes(user_id, name, description, instructions, date, time)
        VALUES(%(user_id)s,  %(name)s, %(description)s,  %(instructions)s, %(date)s, %(time)s)
        '''
        results = connectToMySQL(DB).query_db(query,data)

        return results
    
    @classmethod
    def read_all_recipes(cls):
        query = '''
        SELECT * FROM recipes 
        JOIN users 
        ON recipes.user_id = users.id;
        '''
        results = connectToMySQL(DB).query_db(query)

        
        all_recipes = []

        for row in results:
            recipe = cls(row)
        
            # user_data = {**row}

            creator_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            recipe.creator = user_model.User(creator_data)
            
            all_recipes.append(recipe)

        return all_recipes


    # Read ONE recipe method

    @classmethod
    def read_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])
    
    # UPDATE RECIPE

    @classmethod
    def update_recipe(cls, data):
        query = """
                UPDATE recipes 
                SET name=%(name)s, description=%(description)s,instructions=%(instructions)s, date=%(date)s, time=%(time)s 
                WHERE id = %(id)s;
                
            """

        results = connectToMySQL(DB).query_db(query, data)
        return results
    
    # DELETE RECIPE

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query,data)
        
        if results == None:
            return "success"
        else:
            return "failure"