from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import threading

from django.http import JsonResponse

def email(request):
    if request.method == "POST":
        # Mengambil data dari form
        name = request.POST.get('name')
        sender_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Pesan yang akan dikirim dalam email
        email_body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"

        try:
            # Mengirim email
            mail = EmailMessage(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                ['mhdmasruri292@gmail.com'],
                reply_to=[sender_email],
            )
            mail.send()
            # Mengembalikan respons sukses dalam format JSON
            return JsonResponse({"status": "success", "message": "Email berhasil dikirim!"})

        except Exception as e:
            # Mengembalikan respons gagal dalam format JSON
            return JsonResponse({"status": "error", "message": f"Gagal mengirim email: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Metode tidak diizinkan."})


