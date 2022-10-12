from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash   
from flask_app import app, bcrypt, DATABASE   

class Believer:
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.report_id = data['report_id']
        self.user_id = data['user_id']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO believers (report_id, user_id) VALUES (%(report_id)s, %(user_id)s);"
        new_believer_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_believer_id
    

    @classmethod
    def get_all_believers_for_report(cls,data):
        query = "SELECT * FROM believers JOIN users on users.id = believers.user_id JOIN reports ON reports.id = believers.report_id WHERE reports.id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_believers_dicts_from_db = connectToMySQL(DATABASE).query_db(query,data)

        print(list_of_believers_dicts_from_db, "********************xysysy")

        if not list_of_believers_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_believers_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for believer_dict in list_of_believers_dicts_from_db:
            believer_dict_info = {
                "user_id": believer_dict['user_id'],
                "report_id": believer_dict['report_id'],
            }
            believer_dict_info = cls(believer_dict_info)
            believer_dict_info.believer_name = believer_dict["first_name"]
            list_of_believers_instances.append(believer_dict_info)
        return list_of_believers_instances

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM believers JOIN users on users.id = believers.creator_id WHERE believers.id = %(id)s;'
        list_of_one_believer_dict = connectToMySQL(DATABASE).query_db(query, data)
        if not list_of_one_believer_dict:
            return False
        
        current_recipe = cls(list_of_one_believer_dict[0])
        current_recipe.creator_name = list_of_one_believer_dict[0]['first_name']

        return current_recipe

    @classmethod
    def delete_believer(cls, data:dict):
        query = 'DELETE FROM believers report_id = %(report_id)s AND user_id = %(user_id)s;'
        believer = connectToMySQL(DATABASE).query_db(query, data)
        return believer

    # @classmethod
    # def update_believer(cls, data:dict):
    #     query = 'UPDATE believers SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;'
    #     believer = connectToMySQL(DATABASE).query_db(query, data)
    #     return cls(believer)

    # @staticmethod
    # def validate_believer(believer):
    #     is_valid = True  # we assume this is true

    #     if len(believer['location']) < 1:
    #         flash("Where did this happen?", "believer")
    #         is_valid = False

    #     if len(believer['description']) < 1:
    #         flash("Fill out what happen", "believer")
    #         is_valid = False

    #     if  not believer['num_sasquatch'] or int(believer['num_sasquatch']) < 1:
    #         flash("How many sasquatches did you see?", "believer")
    #         is_valid = False

    #     if not believer['date_of_believer']:
    #         flash("Please fill out when this occurred", "believer")         
    #         is_valid = False

    #     return is_valid
