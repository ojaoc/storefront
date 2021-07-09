from django.db.models.aggregates import Avg, Count, Max, Min, Sum
from django.shortcuts import render
from django.db.models import Q, F
from store.models import Collection, Customer, Order, OrderItem, Product


def say_hello(request):
    # Get the last 5 orders with their customer, items including product
    # https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm
    query_set_or = Customer.objects.aggregate(Count("id"))
    query_set_cu = Order.objects.filter(customer__id=1).aggregate(Count("id"))
    query_set_oi = OrderItem.objects.filter(product__id=1).aggregate(Sum("quantity"))
    query_set_pr = Product.objects.filter(collection__id=3).aggregate(
        Min("unit_price"), Max("unit_price"), Avg("unit_price")
    )
    query_set_pc = Product.objects.filter(collection__id=3).aggregate(
        Min("unit_price"), Max("unit_price"), Avg("unit_price")
    )

    print(query_set_or)
    print(query_set_cu)
    print(query_set_oi)
    print(query_set_pr)

    return render(
        request,
        "hello.html",
        {
            "orders": query_set_pr,
        },
    )
