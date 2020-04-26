"""pidginforge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from allauth.account.views import confirm_email

# note that this skips the email verification...
from django_registration.backends.one_step.views import RegistrationView
# from django_registration.backends.model_activation.views import RegistrationView
# to do email verification...read this reference: https://django-registration.readthedocs.io/en/3.0/activation-workflow.html

from core.views import IndexTemplateView
from users.forms import CustomUserForm

urlpatterns = [
    path('idara/', admin.site.urls),

    # path("accounts/", include("django_registration.backends.two_step.urls")),
    # path("accounts/", include("django_registration.backends.activation.urls")),

    # path("accounts/register/", RegistrationView.as_view(form_class=CustomUserForm, success_url="/"), name="django_registration_register"),
    # path("accounts/", include("django.contrib.auth.urls")),

    path('accounts/', include('allauth.urls')),    
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api-auth/", include("rest_framework.urls")),    
    path("api/users/", include("users.api.urls")),
    path("api/elements/", include("elements.api.urls")),
    path("api/malapropos/", include("malapropos.api.urls")),
    path("api/", include("questions.api.urls")),
    path("api/categories/", include("categories.api.urls")),
    re_path('rest-auth/registration/account-confirm-email/(?P<key>.+)/', confirm_email, name='account_confirm_email'),
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")

]
