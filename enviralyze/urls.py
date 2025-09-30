from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

class PasswordResetStubView(TemplateView):
    template_name = "password_reset_confirm_stub.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uid"] = kwargs.get("uidb64")
        context["token"] = kwargs.get("token")
        return context

schema_view = get_schema_view(
   openapi.Info(
      title="Enviralyze API",
      default_version='v1',
      description="Description of Enviralyze App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="enviralyze@enviralyze.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path("api/", include("profiles.urls")),
    path("api/", include("products.urls")),
    path("api/", include("lists.urls")),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetStubView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/", include("allauth.urls")),
    path("accounts/", include("allauth.urls")),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("api/schema/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]