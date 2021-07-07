from django.shortcuts import render
from django.db.models import Q, F
from store.models import Collection, Customer, Order, OrderItem, Product


def say_hello(request):
    query_set_pr = Product.objects.all()[15:20]

    return render(
        request,
        "hello.html",
        {
            "products": list(query_set_pr),
        },
    )
