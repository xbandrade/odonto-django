# flake8: noqa
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


def send_confirmation(appointment, site_url):
    logo_url = settings.EMAIL_LOGO_URL
    confirmation_url = f'http://{site_url}/schedule/confirm/{appointment.confirmation_token}/'
    subject = _('Your Appointment Confirmation')
    text_message = _('Thank you for scheduling an appointment with OdontoDj!\n'
                     'Please check the information below and if everything '
                     'is correct, click on the confirmation link.\n\n'
                     'Date: {date}\nTime: {time}\n'
                     'Procedure: {name}\n'
                     'Price: R$ {price}\n\n'
                     '{site}\n\n'
                     'Best regards,\n'
                     'OdontoDj').format(
        date=appointment.date.strftime('%d-%b-%Y'),
        time=appointment.time,
        name=str(appointment.procedure),
        price=str(appointment.procedure.price).replace('.', ','),
        site=confirmation_url,
    )
    html_message = _(
        '<div style="background-color:#f2ffff;">'
        '<div style="background-color:#f8f8f8;padding:20px;text-align:center;">'
        '<img src="{logo}" alt="Logo" width="8%">'
        '</div>'
        '<p style="color:purple;font-size:22px;text-align:center;">'
        'Thank you for scheduling an appointment with <strong>OdontoDj</strong>!</p>'
        '<div style="margin-left:30px;font-size:16px;">'
        '<p>Please check the information below and if everything '
        'is correct, click on the confirmation link.</p><br>'
        '<strong>Date</strong>: {date}<br>'
        '<strong>Time</strong>: {time}<br>'
        '<strong>Procedure</strong>: {name}<br>'
        '<strong>Price</strong>: R$ {price}<br><br>'
        '<a style="padding:10px 20px;margin-top:5px;border:none;background:#000;color:#fff;cursor:pointer;text-decoration:none;" '
        'href="{site}">Confirm</a>'
        '</div>'
        '<div style="margin-left:15px;margin-bottom:30px;font-size:15px">'
        '<br><br>Best regards,<br>'
        '<strong style="color:purple;font-size:18px;">OdontoDj</strong>'
        '<br><br>'
        '</div>'
        '</div>'
    ).format(
        logo=logo_url,
        date=appointment.date.strftime('%d-%m-%Y'),
        time=appointment.time.strftime('%H:%M'),
        name=str(appointment.procedure),
        price=str(appointment.procedure.price).replace('.', ','),
        site=confirmation_url,
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [appointment.user.email]
    send_mail(subject, text_message, from_email,
              recipient_list, html_message=html_message)


if __name__ == '__main__':
    send_confirmation('', 'localhost')
