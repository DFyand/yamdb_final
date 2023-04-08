from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_SENDER_ADDRESS


def send_msg(email, username, confirmation_code):
    body = f"username:{username}, confirmation_code:{confirmation_code}, "
    send_mail('confirmation code', body, EMAIL_SENDER_ADDRESS, [email, ], )
