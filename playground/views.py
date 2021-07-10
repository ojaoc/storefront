from tags.models import TaggedItem, TaggedItemManager
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Avg, Count, Max, Min, Sum
from django.shortcuts import render
from django.db.models import Q, F
from django.db import transaction
from store.models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product


@transaction.atomic()
def say_hello(request):
    # Get the last 5 orders with their customer, items including product
    # https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm
    # query_set_or = Customer.objects.aggregate(Count("id"))
    # query_set_cu = Order.objects.filter(customer__id=1).aggregate(Count("id"))
    # query_set_oi = OrderItem.objects.filter(product__id=1).aggregate(Sum("quantity"))
    # query_set_pr = Product.objects.filter(collection__id=3).aggregate(
    #     Min("unit_price"), Max("unit_price"), Avg("unit_price")
    # )
    # query_set_pc = Product.objects.filter(collection__id=3).aggregate(
    #     Min("unit_price"), Max("unit_price"), Avg("unit_price")
    # )

    # print(query_set_or)
    # print(query_set_cu)
    # print(query_set_oi)
    # print(query_set_pr)

    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    # collection = Collection.objects.get(pk=11)
    # collection.title = "Games"
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # cart = Cart()
    # cart.save()

    # cartItem = CartItem()
    # cartItem.cart = cart
    # cartItem.quantity = 1
    # cartItem.product = Product(pk=1)

    # cartItem.save()

    # cartItem.quantity = 2
    # cartItem.save()

    # cart.delete()  # because cascading is enabled, we only need to
    # # delete the cart, django will take care of
    # # deleting the cartItems associated

    order = Order()
    order.customer = Customer(pk=1)
    order.save()

    item = OrderItem()
    item.order = order
    item.product = Product(pk=1)
    item.quantity = 1
    item.unit_price = 10
    item.save()

    return render(
        request,
        "hello.html",
        {
            "orders": {},
        },
    )
