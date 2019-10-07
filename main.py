import mail
from smtplib import SMTPAuthenticationError
from student import load_students
import getpass
import webbrowser
import pathlib


with open("template.html") as f:
    TEMPLATE_HTML = "\n".join(f.readlines())

students = load_students("students.csv")
if len(students) == 0:
    print("Please update students.csv first")

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

SENDER_EMAIL = input("Your email: ")
EMAIL_SUBJECT = input("Email subject: ")
SENDER_PASSWORD = getpass.getpass("Your password: ")
SENDER_NAME = input("Your name (as shown in the email): ")
CLASS_CODE = input("Class code (as shown in the email): ")
input("Generating a preview of the email, please press [enter] to continue..")
with mail.generate_email_preview_file(
    TEMPLATE_HTML,
    students[0],
    sender_name=SENDER_NAME,
    class_code=CLASS_CODE
) as f:
    webbrowser.open_new(
        pathlib.Path(f.name).as_uri()
    )
    CONFIRMATION_RESPONSE = None
    while (CONFIRMATION_RESPONSE is None
            or CONFIRMATION_RESPONSE not in ["y", "n"]):
        CONFIRMATION_RESPONSE = input(
            "Please review the email template, "
            "type Y to confirm, N to abort: "
        ).lower().strip()
        if CONFIRMATION_RESPONSE == "n":
            exit(-1)


try:
    server = mail.get_smtp_server(
        SMTP_SERVER,
        SMTP_PORT,
        SENDER_EMAIL,
        SENDER_PASSWORD
    )

    for student in students:
        print("Sending to: ", student.name)
        email = mail.create_email(
            SENDER_EMAIL,
            student,
            "[%s]%s" % (CLASS_CODE, EMAIL_SUBJECT),
            TEMPLATE_HTML,
            sender_name=SENDER_NAME,
            class_code=CLASS_CODE
        )
        server.sendmail(email["From"], email["To"], email.as_string())
        server.sendmail(email["From"], email["CC"], email.as_string())

except SMTPAuthenticationError:
    print(
        "Cannot be authenticated by the mail server,"
        " please check your email and password"
    )
    exit(-1)

server.quit()
