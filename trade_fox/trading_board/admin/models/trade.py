from django.contrib import admin


class TradeAdmin(admin.ModelAdmin):
    ordering = ["-date"]
