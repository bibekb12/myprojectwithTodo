from django.http import HttpResponse
from myapp.tasks import send_mail_fun
from projectCelery import settings


def send_mail(request):
    send_mail_fun.delay(
        "your subject",
        "my message in msg",
        settings.EMAIL_HOST,
        "receiver_email_address",
    )
    return HttpResponse("sent email successfull..check your mail please")
