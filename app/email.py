# -*- coding: utf-8 -*-
from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_email(to, subject, template, **kwargs):
	msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
				  sender=current_app.config['MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)