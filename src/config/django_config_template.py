"""
Check https://docs.djangoproject.com/en/1.7/ref/settings/ for details.
"""

# secret key for django security features; customize and keep a secret
SECRET_KEY = 'MY_SECRET_KEY'
# customize if you want Google Analytics
GOOGLE_ANALYTICS_CODE = 'MY_GOOGLE_ANALYTICS_ID'

# keep these to False in production
DEBUG = False
TEMPLATE_DEBUG = False
# host(s) served by the app
ALLOWED_HOSTS = ["MY_SERVER_URL"]

# list of people notified when the app raises an exception
ADMINS = [("MY_ADMIN_NAME", "MY_ADMIN@SOME_DOMAIN.COM")]
# from email, when the app raises an exception
SERVER_EMAIL = "django@MY_SERVER_URL"

# How to send emails?
# - console.EmailBackend: use for debug, writes emails to the console
# - smtp.EmailBackend: use for production, sends emails to ADMINS when exceptions occur 
# (if you use Heroku, you can use the addon/email-server MailGun)
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# settings for email server and authentication 
# (for smtp.EmailBackend only, you can comment all this is if use console.EmailBackend)
EMAIL_USE_TLS = True
EMAIL_HOST = "MY_EMAIL_HOST"
EMAIL_HOST_USER = "MY_EMAIL_USER"
EMAIL_HOST_PASSWORD = "MY_EMAIL_PASSWORD"
EMAIL_PORT = "MY_EMAIL_PORT"
