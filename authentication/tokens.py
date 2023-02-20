from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# Unique token used to activate user account
class TokenGenerate(PasswordResetTokenGenerator):
    def _make_hash(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)
        )
        
generate_token = TokenGenerate()