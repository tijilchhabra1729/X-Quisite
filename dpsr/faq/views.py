from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dpsr.models import User , Question , Answer , Like , Unlike
from dpsr.faq.forms import MakeQForm , SearchQForm , MakeAForm
from sqlalchemy import desc , asc

faqs = Blueprint('faqs', __name__)

@faqs.route('/allfaq' , methods = ['GET' , 'POST'])
def all_faq():
    form = SearchQForm()
    results = []
    question = Question.query.order_by(Question.date.desc())
    if form.validate_on_submit():
        searcher = []
        if ' ' in form.search.data:
            search = form.search.data.split()
        else:
            search = [form.search.data]
        for q in question:
            n = 0
            for s in search:
                if s.lower() in q.question.lower() :
                    n+=1
            l = (n , q.id)
            searcher.append(l)
        searcher.sort(reverse=True)
        for s , q in searcher:
            q1 = Question.query.get(q)
            results.append(q1)

    else:
        for q in question:
            results.append(q)

    return render_template('all_faq.htm' , form = form , results = results)

@faqs.route('/makefaq' , methods = ['GET' , 'POST'])
@login_required
def ask_q():
    form = MakeQForm()
    if form.validate_on_submit():
        q = Question(question = form.question.data,
                    userid = current_user.id)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('faqs.ask_q'))
    return render_template('makeq.htm' , form = form)

@faqs.route('/<q_id>/singleq' , methods = ['GET' , 'POST'])
def singleq(q_id):
    question = Question.query.get_or_404(q_id)
    ans = []
    like = []
    unlike = []
    for answer in question.answer:
        ans.append(answer)
        n = 0
        for l in answer.likes:
            n += 1
        like.append(n)
        n = 0
        for l in answer.unlikes:
            n += 1
        unlike.append(n)
    return render_template('singleq.htm' , question = question , q_id = q_id , ans = ans , like = like , unlike = unlike)

@faqs.route('/<q_id>/answer' , methods = ['GET' , 'POST'])
@login_required
def ans_q(q_id):
    form = MakeAForm()
    question = Question.query.get_or_404(q_id)
    if form.validate_on_submit():
        answer = Answer(answer = form.answer.data,
                        userid = current_user.id,
                        questionid = q_id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('faqs.ans_q' , q_id = q_id))

    return render_template('answer.htm' , form = form)

@faqs.route('/<q_id>/<a_id>/<type>/like_unlike' , methods = ['GET' , 'POST'])
@login_required
def liun(q_id, a_id , type):
    a = Answer.query.get_or_404(a_id)
    if type == 'like':
        for l in a.likes:
            if current_user == l.user:
                db.session.delete(l)
                db.session.commit()
                return redirect(url_for('faqs.singleq' , q_id = q_id))
        like = Like(answerid = a_id,
                    userid = current_user.id)
        db.session.add(like)
        db.session.commit()

    else:
        for l in a.unlikes:
            if current_user == l.user:
                db.session.delete(l)
                db.session.commit()
                return redirect(url_for('faqs.singleq' , q_id = q_id))
        unlike = Unlike(answerid = a_id,
                    userid = current_user.id)
        db.session.add(unlike)
        db.session.commit()
        return redirect(url_for('faqs.singleq' , q_id = q_id))

    return redirect(url_for('faqs.singleq' , q_id = q_id))
