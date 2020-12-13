from django.http import HttpResponse
from django.shortcuts import render, redirect


# def add_book(request):
#     if request.method == 'POST':
#         title = request.POST.get("title")
#         price = request.POST.get("price")
#         publish = request.POST.get("publish")
#         pub_date = request.POST.get("pub_date")
#         books = models.Book.objects.create(title=title, price = price, 
#             publish = publish, pub_date = pub_date)
#         return HttpResponse('Adding success!')
#     return render(request, "add_book.html")

# def table(request):
#     data = models.Book.objects.all()
#     return render(request, "table.html", locals())

# def del_book(request):
