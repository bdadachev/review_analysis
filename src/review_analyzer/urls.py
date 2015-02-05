from django.conf.urls import patterns, url

from review_analyzer import views

urlpatterns = patterns('',
	# home page
	url(r'^$', views.home, name='home'),
	url(r'^validate_coordinates/$', views.validate_coordinates, name='validate_coordinates'),
	# about page
	url(r'^about/$', views.about, name='about'),
	# restaurant page
	url(r'^biz/(?P<hash>.+)$', views.restaurant_by_hash, name='restaurant_by_hash'),
	url(r'^regional_statistics/$', views.regional_statistics, name='regional_statistics'),
	url(r'^ratings/$', views.ratings, name='ratings'),
	# map page
	url(r'^location/(?P<address>.+)$', views.location, name='location'),
	url(r'^update_map/$', views.get_restaurants_on_map, name='update_map'),
)
