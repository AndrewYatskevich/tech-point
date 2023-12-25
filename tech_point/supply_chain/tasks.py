import base64
import random
from io import BytesIO

import qrcode
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from PIL import Image

from supply_chain.models import SupplyChainLink


@shared_task
def random_increase_in_supplier_debt():
    link = SupplyChainLink.objects.first()
    link.debt += random.randint(5, 500)
    link.save()


@shared_task
def random_reduce_in_supplier_debt():
    link = SupplyChainLink.objects.last()
    random_number = random.randint(100, 100000)
    if random_number <= link.debt:
        link.debt -= random_number
    else:
        link.debt = 0
    link.save()


@shared_task
def clear_debt_task(link_ids: list):
    links = SupplyChainLink.objects.filter(id__in=link_ids)
    links.update(debt=0)


@shared_task
def send_email_with_link_address(address: str, email: str):
    qr_image = qrcode.make(address)
    qr_offset = Image.new("RGB", (310, 310), "white")
    qr_offset.paste(qr_image)
    stream = BytesIO()
    qr_offset.save(stream, "PNG")
    buffered = BytesIO()
    qr_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    ctx = {
        "name": "employee",
        "qr_code_image": qr_image_base64,
    }
    msg = EmailMessage(
        subject="Here are your supply chain contacts",
        body=render_to_string("qr.html", ctx),
        to=[email],
        from_email="tech.point@example.com",
    )
    msg.content_subtype = "html"
    msg.send()
