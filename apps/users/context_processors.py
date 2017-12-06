from apps.models.models import Initiative
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# current_user_initiative_name_processor

def current_user_hello(request):
    """Injects into global context the name of the Initiative related to the user"""

    current_user = request.user
    current_user_hello = None

    if current_user.is_staff:
        current_user_hello = _("Hola <a class='username' href='%(link)s'>%(name)s <span class='icon-agent'></span></a>") % { 'link' : reverse('users:dashboard') , 'name' : request.user.username }
    elif current_user.is_authenticated:
        current_user_initiative = Initiative.objects.filter(user=request.user).first()
        if current_user_initiative:
            current_user_hello = _("Hola <a class='username' href='%(link)s'>%(name)s <span class='icon-agent'></span></a>") % { 'link': reverse('users:dashboard') , 'name': request.user.username }
        else:
            current_user_hello = _("Hola %(name)s, <br/><a class='create-link' href='%(link)s'>¿creaste tu iniciativa?</a>") % { 'link' : reverse('modelforms:create_initiative'), 'name' : request.user.username }

    return { 'current_user_hello' : current_user_hello }
