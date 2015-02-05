from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_range(value):
	"""
	{% load customtags %}
    	Use: {% for i in 3|get_range %}...
  	"""
	return range(value)

@register.simple_tag
def settings_variable(name):
	"""
	{% load customtags %}
    	Use: {% settings_variable "NAME" %}...
  	"""
	return getattr(settings, name, "")
