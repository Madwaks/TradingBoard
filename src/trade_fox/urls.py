"""trade_fox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

import core.urls
import decision_maker.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include((core.urls, "core"), namespace="core")),
    path(
        "screener/",
        include((decision_maker.urls, "decision_maker"), namespace="decision_maker"),
    ),
    path("login", LoginView.as_view(template_name="login.html"), name="login"),
    path("__debug__/", include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
