from django.shortcuts import render
from django.views import View
from apps.models.models import City
from apps.models import categories

class Dashboard(View):

    def get(self, request):
        return render(request, 'users/dashboard.html', locals())
