from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        users = User.objects.all()
        args = {'users': users}
        return render(request, self.template_name, args)
