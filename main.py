import mail, student
import getpass

with open("template.html") as f:
	TEMPLATE_HTML = "\n".join(f.readlines())

students = student.load_students("students.csv")

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

SENDER_EMAIL = input("Your email: ")
EMAIL_SUBJECT = input("Email subject: ")
SENDER_PASSWORD = getpass.getpass("Your password: ")
SENDER_NAME = input("Your name: ")
CLASS_CODE = input("Class code: ")

server = mail.get_smtp_server(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)

for student in students:
	print("Sending to: ", student.name)
	email = mail.create_email(SENDER_EMAIL, student, "[%s]%s"%(CLASS_CODE, EMAIL_SUBJECT), TEMPLATE_HTML, 
								sender_name = SENDER_NAME, class_code = CLASS_CODE
			)
	server.sendmail(email["From"], email["To"], email.as_string())
	server.sendmail(email["From"], email["CC"], email.as_string())

server.quit()