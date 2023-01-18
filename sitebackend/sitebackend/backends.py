from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class SimpleBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Si el usuario no existe, devuelve None
            return None
        
        # Verifica si la contraseña es válida
        if user.check_password(password):
            # Devuelve el usuario si la contraseña es correcta
            return user
        return None