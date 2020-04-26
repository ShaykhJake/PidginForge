from django_registration.forms import RegistrationFormUniqueEmail
from users.models import CustomUser

class CustomUserForm(RegistrationFormUniqueEmail):
    
    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
