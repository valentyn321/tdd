from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


def home_page(request):
    if request.method != "POST":
        items = Item.objects.all()
        return render(request, "home.html", {'items': items})
    else:
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
