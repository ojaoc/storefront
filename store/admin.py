from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.contrib.admin.decorators import action
from django.contrib.admin.helpers import AdminField
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [("<10", "Low")]

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["promotions"]
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_display = ["title", "unit_price", "inventory_status", "collection"]
    list_editable = ["unit_price"]
    search_fields = ["title"]
    list_per_page = 10

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request: HttpRequest, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products were successfully updated"
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html(
            '<a href="{}">{}</a>', url, f"{customer.orders_count} orders"
        )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .prefetch_related("order_set")
            .annotate(orders_count=Count("order"))
        )


class OrderItemInLine(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInLine]
    list_display = ["id", "placed_at", "payment_status", "customer"]
    ordering = ["-placed_at", "payment_status"]
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count("product"))
