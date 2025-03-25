from flask import Blueprint, render_template, request, flash, jsonify
from . import db
from flask_login import  login_required, current_user
from .model import Note, Expense
import json
from datetime import datetime
from sqlalchemy import extract # thư viện dùng để trích datetime cụ thể
views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required

def home():
    """if request.method == 'POST':
        note = request.form.get('note')
        if len(note) >0:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user = current_user)"""

    if request.method == "POST":
        amount = request.form.get('amount')
        categories = request.form.get('categories')
        if not categories and amount>0:
            flash('Please input the data',category='error')
        else:
            new_expense = Expense(user_id = current_user.id, timestamp = datetime.utcnow())
            db.session.add(new_expense)
            db.session.commit()
            flash('Data updated', category='success')

    current_month = datetime.now()

    monthly_expense = Expense.query.filter(
        Expense.user_id == current_user.id,
        extract('month', Expense.timestamp) == current_month.month
    ).all() 
    # Tổng số tiền từ danh sách chi tiêu
    total = 0
    for expense in monthly_expense:
        total += expense.amount
    #Kiểm tra lại    
    return render_template('home.html', user = current_user, total = total)
    

@views.route('delete-expense', methods=['POST'])
def delete_expense():
    """  data = json.loads(request.data)
    expense_Id = data['noteId']
    #truy cập note có id, nếu tồn tại thì xóa note đi
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    #trả về emty response
    return jsonify({})"""
    data = json.load(request.data)
    expense_id = data['expenseId']
    expense = Expense.query.get(expense_id)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense_id)
            db.session.commit()
    return jsonify({})

    
  
  
