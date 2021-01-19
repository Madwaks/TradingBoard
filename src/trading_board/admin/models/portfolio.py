from django.contrib import admin


class PortfolioAdmin(admin.ModelAdmin):
    ordering = ["-amount"]
