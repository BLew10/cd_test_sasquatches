from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash   
from flask_app import app, bcrypt, DATABASE   # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
#regex 





# model.py, however many tables you have is however many models you need

#Necessary if importing another Class to be referenced 
# from flask_app.models import (child_model file)
# Example
# from flask_app.models.ninja import Ninja

# Things to change:
# Table_Class_Name
# reports lowercase
# report lowercase
# (scehma_name)


class Report:
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.creator_id = data['creator_id']
        self.num_sasquatch = data['num_sasquatch']
        self.date_of_report = data['date_of_report']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO reports ( location, description, creator_id, num_sasquatch, date_of_report ) VALUES (%(location)s, %(description)s, %(creator_id)s, %(num_sasquatch)s, %(date_of_report)s);"
        new_report_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_report_id
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reports JOIN users on users.id = reports.creator_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_reports_dicts_from_db = connectToMySQL(DATABASE).query_db(query)


        if not list_of_reports_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_reports_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for report_dict in list_of_reports_dicts_from_db:
            report_dict_info = {
                "id": report_dict['id'],
                "description": report_dict['description'],
                "location": report_dict['location'],
                "num_sasquatch": report_dict['num_sasquatch'],
                "date_of_report": report_dict['date_of_report'],
                "creator_id": report_dict['creator_id'],
                "created_at": report_dict['created_at'],
                "updated_at": report_dict['updated_at']
            }
            report_dict_info = cls(report_dict_info)
            report_dict_info.creator_name = report_dict["first_name"]
            list_of_reports_instances.append(report_dict_info)
        return list_of_reports_instances

    @classmethod
    def get_skeptics(cls):
        query = "SELECT COUNT(report_id), report_id FROM skeptics group by report_id;"
        list_of_reports = connectToMySQL(DATABASE).query_db(query)

        report_skeptics_count = {}
        for report in list_of_reports:
            report_skeptics_count[report["report_id"]]  = report["COUNT(report_id)"]
        return report_skeptics_count

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM reports JOIN users on users.id = reports.creator_id WHERE reports.id = %(id)s;'
        list_of_one_report_dict = connectToMySQL(DATABASE).query_db(query, data)
        if not list_of_one_report_dict:
            return False
        
        current_report = cls(list_of_one_report_dict[0])
        current_report.creator_name = list_of_one_report_dict[0]['first_name']

        return current_report

    @classmethod
    def delete_report(cls, data:dict):
        query_two = 'DELETE FROM believers WHERE report_id = %(id)s;'
        report_two = connectToMySQL(DATABASE).query_db(query_two, data)
        query_three = 'DELETE FROM skeptics WHERE report_id = %(id)s;'
        report_two = connectToMySQL(DATABASE).query_db(query_three, data)
        query = 'DELETE FROM reports WHERE id = %(id)s;'
        report = connectToMySQL(DATABASE).query_db(query, data)

        
        return report

    @classmethod
    def update_report(cls, data:dict):
        query = 'UPDATE reports SET location=%(location)s, description=%(description)s, num_sasquatch=%(num_sasquatch)s, date_of_report = %(date_of_report)s WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_report(report):
        is_valid = True  # we assume this is true

        if len(report['location']) < 1:
            flash("Where did this happen?", "report")
            is_valid = False

        if len(report['description']) < 1:
            flash("Fill out what happen", "report")
            is_valid = False

        if  not report['num_sasquatch'] or int(report['num_sasquatch']) < 1:
            flash("How many sasquatches did you see?", "report")
            is_valid = False

        if not report['date_of_report']:
            flash("Please fill out when this occurred", "report")         
            is_valid = False

        return is_valid
