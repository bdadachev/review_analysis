from django.conf.urls import patterns, include, url
from django.contrib import admin

handler404 = 'review_analyzer.views.error404'
handler500 = 'review_analyzer.views.error500'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    # redirect everything to review_analyzer
    url(r'^', include("review_analyzer.urls", namespace="review_analyzer")),
)
