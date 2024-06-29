from django.shortcuts import render


# Create your views here.
# MIRE BIENVENUE
def index(request):
    return render(request, 'accounts/index.html')
