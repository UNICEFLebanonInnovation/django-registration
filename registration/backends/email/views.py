from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.backends.default.views import (
    RegistrationView,
    ActivationView
)
from registration.models import EmailRegistrationProfile
from registration.forms import EmailRegistrationForm


class RegistrationView(RegistrationView):
    """
    A registration backend for registering with just
    an email address, uses a custom registration manager

    """
    registration_profile = EmailRegistrationProfile
    form_class = EmailRegistrationForm

    def register(self, request, **cleaned_data):
        """
        Given a email address and password, register a new
        user account, which will initially be inactive.

        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = self.registration_profile.objects.create_inactive_user(
            email,
            password,
            site)
        signals.user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=request)
        return new_user


class ActivationView(ActivationView):
    """
    Super class implementation is what we want,
    just need use our custom profile instead

    """
    registration_profile = EmailRegistrationProfile
