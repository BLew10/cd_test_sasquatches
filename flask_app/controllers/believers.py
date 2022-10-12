from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.skeptic import Skeptic
from flask_app.models.believer import Believer



@app.route('/believer/report/<int:report_id>/user/<int:user_id>')
def add_believer(report_id, user_id):
    believer_info = {
        "report_id": report_id,
        "user_id": user_id
    }
    Believer.create(believer_info)
    Skeptic.delete_skeptic(believer_info)
    return redirect(f"/report/{report_id}")