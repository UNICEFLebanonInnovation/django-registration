from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from registration.signals import user_activated
from registration.models import (
    RegistrationProfile,
    EmailRegistrationProfile,
)


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    registration_profile = RegistrationProfile

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not already
        activated.
        
        """
        for profile in queryset:
            activated = self.registration_profile.objects.activate_user(
                profile.activation_key
            )
            if activated:
                # also fire the activated signal
                user_activated.send(
                    sender=self.__class__,
                    user=profile.user,
                    request=request
                )
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")


class EmailRegistrationAdmin(RegistrationAdmin):
    """
    Overrides the default admin to handle users with just an email address
    """
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    registration_profile = EmailRegistrationProfile


admin.site.register(RegistrationProfile, RegistrationAdmin)
admin.site.register(EmailRegistrationProfile, EmailRegistrationAdmin)
