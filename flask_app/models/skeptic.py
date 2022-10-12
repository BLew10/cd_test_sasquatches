from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash   
from flask_app import app, bcrypt, DATABASE   

class Skeptic:
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.report_id = data['report_id']
        self.user_id = data['user_id']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO skeptics (report_id, user_id) VALUES (%(report_id)s, %(user_id)s);"
        new_skeptic_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_skeptic_id
    

    @classmethod
    def get_all_skeptics_for_report(cls,data):
        query = "SELECT * FROM skeptics JOIN users on users.id = skeptics.user_id JOIN reports ON reports.id = skeptics.report_id WHERE reports.id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_skeptics_dicts_from_db = connectToMySQL(DATABASE).query_db(query,data)

        print(list_of_skeptics_dicts_from_db, "********************xysysy")

        if not list_of_skeptics_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_skeptics_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for skeptic_dict in list_of_skeptics_dicts_from_db:
            skeptic_dict_info = {
                "user_id": skeptic_dict['user_id'],
                "report_id": skeptic_dict['report_id'],
            }
            skeptic_dict_info = cls(skeptic_dict_info)
            skeptic_dict_info.skeptic_name = skeptic_dict["first_name"]
            list_of_skeptics_instances.append(skeptic_dict_info)
        return list_of_skeptics_instances

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM skeptics JOIN users on users.id = skeptics.creator_id WHERE skeptics.id = %(id)s;'
        list_of_one_skeptic_dict = connectToMySQL(DATABASE).query_db(query, data)
        if not list_of_one_skeptic_dict:
            return False
        
        current_recipe = cls(list_of_one_skeptic_dict[0])
        current_recipe.creator_name = list_of_one_skeptic_dict[0]['first_name']

        return current_recipe

    @classmethod
    def delete_skeptic(cls, data:dict):
        query = 'DELETE FROM skeptics WHERE report_id = %(report_id)s AND user_id = %(user_id)s;'
        skeptic = connectToMySQL(DATABASE).query_db(query, data)
        return skeptic

    # @classmethod
    # def update_skeptic(cls, data:dict):
    #     query = 'UPDATE skeptics SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;'
    #     skeptic = connectToMySQL(DATABASE).query_db(query, data)
    #     return cls(skeptic)

    # @staticmethod
    # def validate_skeptic(skeptic):
    #     is_valid = True  # we assume this is true

    #     if len(skeptic['location']) < 1:
    #         flash("Where did this happen?", "skeptic")
    #         is_valid = False

    #     if len(skeptic['description']) < 1:
    #         flash("Fill out what happen", "skeptic")
    #         is_valid = False

    #     if  not skeptic['num_sasquatch'] or int(skeptic['num_sasquatch']) < 1:
    #         flash("How many sasquatches did you see?", "skeptic")
    #         is_valid = False

    #     if not skeptic['date_of_skeptic']:
    #         flash("Please fill out when this occurred", "skeptic")         
    #         is_valid = False

    #     return is_valid
