from django.conf.urls.defaults import *

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', "django.views.generic.simple.direct_to_template", {"template": "index.html"})
)
