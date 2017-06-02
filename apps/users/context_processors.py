from apps.models.models import Initiative
from django.urls import reverse

# current_user_initiative_name_processor

def current_user_hello(request):
    """Injects into global context the name of the Initiative related to the user"""

    current_user = request.user

    if current_user.is_staff:
        current_user_hello = "<a href='/admin'>admin</a>"
    elif current_user.is_authenticated:
        current_user_initiative = Initiative.objects.filter(user=request.user).first()
        if current_user_initiative:
            current_user_hello = "Hola, <a href='" + reverse('users:dashboard') + "'>" + current_user_initiative.name + "</a>"
        else:
            current_user_hello = "Bienvenido! <a href='/'>¿Creaste tu iniciativa</a>?"
    else:
        current_user_hello = None

    return { 'current_user_hello' : current_user_hello }
