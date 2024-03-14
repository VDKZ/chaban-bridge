# Third-party
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Django
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# Application
import jobs.views as job_views

router = routers.DefaultRouter()
router.register("jobs", job_views.JobViewSet, basename="jobs")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/", include(router.urls)),
]
