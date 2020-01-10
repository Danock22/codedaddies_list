from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    stuff_for_frotend = {'search':search}
    
    return render(request, template_name='my_app/new_search.html', context=stuff_for_frotend)
    