from . import auth
from flask.ext.login import login_user,logout_user,current_user,login_required
from flask import  render_template,flash,redirect,url_for,request
from ..models import User
from .forms import LoginForm,RegisterForm
from ..email import send_email
from .. import db


@auth.route('/login',methods=['POST','GET'])
def login():
    loginform=LoginForm()
    if loginform.validate_on_submit():
        user=User.query.filter_by(email=loginform.email.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user,loginform.remember_me.data)
            return redirect(url_for('main.index'))
        flash('invalid username or password!')
    return render_template('auth/login.html',form=loginform)


@auth.route('/logout')
def logout():
    logout_user()
    flash('you have been logout!')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmatin_token()
        send_email(user.email,'Confirm your account','/auth/email/confirm',user=user,token=token)
        flash('now you can login in!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')

    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated :
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5]!='auth.' \
            and request.endpoint!='static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed',methods=['GET','POST'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.html')


@auth.route('/confirm')
@login_required
def send_confirmation():
    token=current_user.generate_confirmatin_token()
    send_email(current_user.email,'Confirm your account','auth/email/confirm',
               user=current_user,token=token)
    flash('a confirmation email has been sent to you')
    return redirect(url_for('main.index'))



