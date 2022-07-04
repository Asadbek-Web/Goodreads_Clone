from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from books.models import Book

# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books" 

class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        paginator = Paginator(books, 2)

        page_obj = paginator.get_page(1)

        return render(request, "books/list.html", {"page_obj": page_obj})


class BookDetailView(DetailView):
    template_name = "books/detail.html"
    pk_url_kwarg = "id"
    model = Book

# class BookDetailView(View):
#     def get(self, request, id ):
#         book = Book.objects.get(id=id)

#         return render(request, "books/detail.html", {"book": book})