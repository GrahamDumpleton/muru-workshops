import asyncio
import os
import threading

from django.http import JsonResponse

from .models import Product


def index(request):
    """A synchronous view: the products, and where the view ran."""

    return JsonResponse(
        {
            "products": [product.name for product in Product.objects.order_by("id")],
            "worker process": os.getpid(),
            "thread": threading.current_thread().name,
        }
    )


def stock(request):
    raise RuntimeError("the stock count for Teapot is negative")


async def ping(request):
    """An asynchronous view: whether it ran on an event loop, and on which thread."""

    try:
        asyncio.get_running_loop()
        on_loop = True
    except RuntimeError:
        on_loop = False

    return JsonResponse({"on an event loop": on_loop, "thread": threading.current_thread().name})
