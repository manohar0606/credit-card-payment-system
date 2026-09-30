from django.contrib import admin
from django.urls import path
from django.db.models import Sum,Count
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from .models import User,Cards,Transactions,AdminLogs

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active"
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "card_type",
        "card_number",
        "last_four_digit",
        "expiry_data",
        "card_holder_name",
    )

    search_fields = (
        "user__username",
        "card_holder_name",
        "last_four_digit",
    )

    list_filter = (
        "card_type",
    )


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "card",
        "amount",
        "status",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "status",
    )

    list_filter = (
        "status",
        "timestamp",
    )

    ordering = (
        "-timestamp",
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "daily-summary/",
                self.admin_site.admin_view(self.daily_summary),
                name="daily-payment-summary",
            ),
        ]

        return custom_urls + urls

    def daily_summary(self, request):

        today = timezone.now().date()

        transactions = Transactions.objects.filter(
            timestamp__date=today
        )

        total_payments = transactions.count()

        successful_payments = transactions.filter(
            status="SUCCESS"
        ).count()

        failed_payments = transactions.filter(
            status="FAILED"
        ).count()

        total_amount = transactions.aggregate(
            total=Sum("amount")
        )["total"] or 0

        context = {
            "today": today,
            "total_payments": total_payments,
            "successful_payments": successful_payments,
            "failed_payments": failed_payments,
            "total_amount": total_amount,
        }

        return render(
            request,
            "admin/daily_payment_summary.html",
            context
        )

    
@admin.register(AdminLogs)
class AdminLogsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "admin",
        "action",
        "timestamp",
    )
    search_fields = (
        "admin__username",
        "action"
    )

    list_filter = (
        "timestamp",
    )

    ordering = (
        "-timestamp",
    )
