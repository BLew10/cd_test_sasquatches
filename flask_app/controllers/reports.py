# controllers.py, however many tables you have is however many controllers you need
from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.report import Report
from flask_app.models.user import User
from flask_app.models.skeptic import Skeptic


#controllers file name shoudl be plural
#model file name should be singular
#table_name is plural
#table_class is uppercase and singular
#table_name_singular represents the singular version of whatever the table is representing. Ex: Dojos -> dojo. 

#route convention
#table_name/new -> displaying the form -> get method
#table_name/create -> processes form above -> post method
#table_name/<int:id> -> show -> get method
#table_name/<int:id>/edit -> displaying the form -> get method
#table_name/<int:id>/update -> processes the form -> post method
#table_name/<int:id>/delete-> deletes the row -> get method


@app.route('/report/new')
def report_new():
    user = User.get_one({"id": session['user_id']})
    return render_template("create_report.html", user = user)

@app.route('/report/create', methods = ["post"])
def create_report():
    #creates a new __ from the client side and stores in the db
    if not Report.validate_report(request.form):
        return redirect('/report/new')
    new_report_data = { **request.form}
    Report.create(new_report_data)
    print(new_report_data)
    return redirect('/dashboard')

@app.route('/report/<int:id>')
def report_show_one(id):

    report_id = {
        "id": id
    }
    #grabs all existing in the db
    report = Report.get_one(report_id)
    user = User.get_one({"id": session['user_id']})
    skeptics = Skeptic.get_all_skeptics_for_report(report_id)
    print(skeptics, "************************")
    return render_template("view_report.html", report = report, user= user, skeptics = skeptics)

@app.route('/report/<int:id>/edit')
def report_edit(id):
    report_id = {
        "id": id
    }
    report = Report.get_one(report_id)
    user = User.get_one({"id": session['user_id']})
    return render_template("edit_report.html", report = report, user = user)

@app.route('/report/<int:id>/update', methods = ['POST'])
def update_report(id):
    if not Report.validate_report(request.form):
        return redirect(f'/report/{id}/edit')
    updated_report_data = { **request.form,
    "id": id
    }
    Report.update_report(updated_report_data)
    return redirect('/dashboard')

@app.route('/report/<int:id>/delete')
def delete_report(id):
    #deletes the target instance
    deleted_report_id = {
        "id": id
    }
    Report.delete_report(deleted_report_id)
    return redirect("/dashboard")

