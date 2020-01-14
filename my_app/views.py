from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus, quote
from . import models
import re

# BASE_CRAIGSLIST_URL = "https://colombia.craigslist.org/search/jjj?query={}"
BASE_CRAIGSLIST_URL = "https://listado.mercadolibre.com.co/{}"

# Create your views here.
def home(request):
    return render(request, template_name='base.html')

def new_search(request):

    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(markup=data, features='html.parser')

    post_listings = []
    post_listings = soup.find_all(name='li', class_= re.compile('results-item highlighted article'))
    # post_location = post_listings[0].find(class_='item__location').text

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='main-title').text
        if post.find(class_='item__price'):
            post_price = post.find(class_='item__price').text
        else:
            post_price = 'N/A'
        post_url = post.find('a').attrs['href']
        post_img = post.find_all(name='img')
        # print("\n-------------------------------------------------\n", post)

        # post_img = post_img[0].get("src")
        if post_img[0].get("src") is None:
            post_img = post_img[0].get("data-src")
        else:
            post_img = post_img[0].get("src")
        # print("---------------------------\nIMAGE: ", post_img)

        final_postings.append({'url': post_url, 'title': post_title, 'price': post_price, 'img': post_img})
    
    stuff_for_frotend = {'search':search, 'final_postings': final_postings}
    
    return render(request, template_name='my_app/new_search.html', context=stuff_for_frotend)
    