from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.skeptic import Skeptic
from flask_app.models.believer import Believer



@app.route('/skeptic/report/<int:report_id>/user/<int:user_id>')
def add_skeptic(report_id, user_id):
    skeptic_info = {
        "report_id": report_id,
        "user_id": user_id
    }
    Skeptic.create(skeptic_info)
    Believer.delete_believer(skeptic_info)
    return redirect(f"/report/{report_id}")