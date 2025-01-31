from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm, EditPasswordForm, EditEmailForm, EditUsernameForm, EditUserkeyForm, EditProfileAdminForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/user/<int:userid>')
@login_required
def user(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    return render_template('auth/user.html', user=user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), username=form.username.data, userkey=form.userkey.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete!')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/user/<int:userid>/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password(userid):
    if current_user.id != userid:
        return redirect(url_for('.user', userid=current_user.id))
    form = EditPasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('.user', userid=current_user.id))
        else:
            flash('Invalid password.')
    return render_template("auth/edit_password.html", form=form)


@auth.route('/user/<int:userid>/edit-email', methods=['GET', 'POST'])
@login_required
def edit_email(userid):
    if current_user.id != userid:
        return redirect(url_for('.user', userid=current_user.id))
    form = EditEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.email = form.email.data.lower()
            db.session.add(current_user)
            db.session.commit()
            flash('Your email has been updated.')
            return redirect(url_for('.user', userid=current_user.id))
        else:
            flash('Invalid email or password.')
    return render_template("auth/edit_email.html", form=form)


@auth.route('/user/<int:userid>/edit-username', methods=['GET', 'POST'])
@login_required
def edit_username(userid):
    if current_user.id != userid:
        return redirect(url_for('.user', userid=current_user.id))
    form = EditUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your username has been updated.')
        return redirect(url_for('.user', userid=current_user.id))
    form.username.data = current_user.username
    return render_template('auth/edit_username.html', form=form, admin=False)


@auth.route('/user/<int:userid>/edit-userkey', methods=['GET', 'POST'])
@login_required
def edit_userkey(userid):
    if current_user.id != userid:
        return redirect(url_for('.user', userid=current_user.id))
    form = EditUserkeyForm()
    if form.validate_on_submit():
        current_user.userkey = form.userkey.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your userkey has been updated.')
        return redirect(url_for('.user', userid=current_user.id))
    form.userkey.data = current_user.userkey
    return render_template('auth/edit_userkey.html', form=form, admin=False)
