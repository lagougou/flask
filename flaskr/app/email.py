from flask.ext.mail import Mail,Message
from . import mail
from manage import app
from flask import render_template
from threading import Thread

def send_ansy_emaail(app,msg):
    with app.app_context():
        mail.send(msg)

#function of sending email
def send_email(to,subject,template,**kwargs):

    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    tr=Thread(target=send_ansy_emaail,args=(app,msg))
    tr.start()
    return tr