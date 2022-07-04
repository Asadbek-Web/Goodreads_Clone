from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))
        
        self.assertContains(response, "No books found")   # assertContains --> ushbu narsa bormi yo'qmi shuni tekshiradi     Test_driven_developmeent --> testni fail ligini ko'rib uni xatosini to'g'irlash

    def test_books_list(self):
        Book.objects.create(title="Book1", description="Description1", isbn="1111111")
        Book.objects.create(title="Book2", description="Description2", isbn="2222222")
        Book.objects.create(title="Book3", description="Description3", isbn="3333333")

        response = self.client.get(reverse("books:list"))

        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1111111")

        response = self.client.get(reverse("books:detail", kwargs={"id" : book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)