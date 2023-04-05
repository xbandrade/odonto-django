from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


def send_confirmation(appointment):
    subject = _('Your Appointment Confirmation')
    text_message = _('Thank you for scheduling an appointment with OdontoDj!\n'
                     'Please check the information below and if everything '
                     'is correct, click on the confirmation link.\n\n'
                     'Date: {date}\nTime: {time}\n'
                     'Procedure: {name}\n'
                     'Price: R$ {price}\n\n'
                     'https://www.example.com/confirm\n\n'
                     'Best regards,\n'
                     'OdontoDj').format(
        date=appointment.date.strftime('%d-%b-%Y'),
        time=appointment.time,
        name=appointment.procedure.name,
        price=str(appointment.procedure.price).replace('.', ','),
    )
    html_message = _('<p>Thank you for scheduling an appointment with '
                     '<strong>OdontoDj</strong>!</p>'
                     '<p>Please check the information below and if everything '
                     'is correct, click on the confirmation link.</p>'
                     '<br><br>Date: {date}<br>Time: {time}<br>'
                     'Procedure: {name}<br>'
                     'Price: R$ {price}<br><br>'
                     '<a href="https://recipes-django.onrender.com">Confirm'
                     '</a><br><br>Best regards,<br>'
                     '</strong>OdontoDj<strong>').format(
        date=appointment.date.strftime('%d-%m-%Y'),
        time=appointment.time,
        name=appointment.procedure.name,
        price=str(appointment.procedure.price).replace('.', ','),
    )
    from_email = 'devbaxx@gmail.com'
    recipient_list = [appointment.user.email]
    send_mail(subject, text_message, from_email,
              recipient_list, html_message=html_message)


if __name__ == '__main__':
    send_confirmation('myyuuxx@gmail.com')
