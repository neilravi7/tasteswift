import imp
from django.conf import settings
# from django.core.mail import send_mail


def send_account_activation_email(email , email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.DEFAULT_FROM_EMAIL
    message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    # Commenting email sending code couse of email service free priod expired.
    # send_mail(subject , message , email_from , [email])
    print("-*"*75)
    print(f"|HI {email} {' '*59}|")
    print("| Please open this link to verify your account |")
    print(message)
    print("-*"*75)
    return None