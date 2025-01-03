from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Role, User
from ..decorators import admin_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<int:userid>')
def user(userid):
    user = User.query.filter_by(id=userid).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', userid=current_user.id))
    form.username.data = current_user.username
    return render_template('edit_profile.html', form=form, admin=False)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', userid=user.id))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    return render_template('edit_profile.html', form=form, user=user)
