from registration.tests.default_backend import *
from registration.tests.forms import *
from registration.tests.models import *
from registration.tests.simple_backend import *
# The following tests can only be run if
# AUTH_USER_MODEL is set to a user which does
# not rely on a username field, such as the user model
# found in https://github.com/Rethought/rtl_django_tools
#from registration.tests.email_backend import *
