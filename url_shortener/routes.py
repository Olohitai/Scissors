from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, login_user, logout_user

from .extensions import db
from .models import Link
from .auth import login, register

shortener = Blueprint('shortener', __name__)


@shortener.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.views = link.views + 1
    db.session.commit()
    return redirect(link.original_url)


@shortener.route('/create_link', methods=['POST'])
@login_required  # Apply the login_required decorator
def create_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()
    return render_template('link_success.html', new_url=link.short_url, original_url=link.original_url)


@shortener.route('/')
def index():
    return render_template('index.html')


@shortener.route('/analytics')
@login_required
def analytics():
    links = Link.query.all()
    return render_template('analytics.html', links=links)


@shortener.errorhandler(404)
def page_not_found(e):
    return '<h1> Page not found </h1>', 404


@shortener.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        success, message = register(email, username, password)
        if success:
            flash("Registration successful", "success")
            return redirect('/login')
        else:
            flash(message, "danger")

    return render_template('register.html')


@shortener.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        success, message = login(email, password)
        if success:
            flash("Login successful", "success")
            return redirect('/')
        else:
            flash(message, "danger")

    return render_template('login.html')


@shortener.route('/logout')  # Define the logout route
@login_required  # Apply the login_required decorator
def logout():
    logout_user()  # Log the user out
    flash("Logged out successfully", "success")
    # Redirect to the index page or any other desired page
    return redirect(('/'))
