from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    def Make_Hash_Value(self, user, timestamp):
        return(six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active))

account_confirmation_token= TokenGenerator()
