from django.conf.urls import include, url

from .api import urls as api_urls

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
]
