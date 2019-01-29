import smtplib
import email.message

def get_smtp_server(url, port, username, password):
	server = smtplib.SMTP(url, port)
	server.starttls()
	server.login(username, password)
	return server

def replace_placeholder(template, student, sender_name, class_code):
	placeholders = {
		"student name": student.name,
		"username": student.username,
		"password": student.password,
		"helper name": sender_name,
		"class code": class_code
	}

	replaced_mail = template

	for placeholder, value in placeholders.items():
		replaced_mail = replaced_mail.replace("%%%s%%"%(placeholder), str(value))

	return replaced_mail


def create_email(sender_email, student, subject, template_html, **kwargs):
	msg = email.message.Message()
	msg['Subject'] =  subject
	msg['From'] = sender_email
	msg['To'] = student.email + ", " + student.sid + "@link.cuhk.edu.hk"
	msg['CC'] = sender_email
	msg.add_header('Content-Type','text/html')
	msg.set_payload(replace_placeholder(template_html, student, **kwargs))

	return msg
	