from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

from books.models import Book, Author


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))
        
        self.assertContains(response, "No books found")   # assertContains --> ushbu narsa bormi yo'qmi shuni tekshiradi     Test_driven_developmeent --> testni fail ligini ko'rib uni xatosini to'g'irlash

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="1111111")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="2222222")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="3333333")

        response = self.client.get(reverse("books:list") + "?page_size=2")


        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2") 

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1111111")

        response = self.client.get(reverse("books:detail", kwargs={"id" : book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    

    # def test_author_page(self):
    #     author = Author.objects.create(
    #         first_name="Kamol",
    #         last_name="Qodirov"
    #     )

    #     response = self.client.get(reverse("books:detail"))

    #     self.assertContains(response, author.first_name)
    #     self.assertContains(response, author.last_name)

    def test_search_books(self):
        book1 = Book.objects.create(title="science", description="Description1", isbn="1111111")
        book2 = Book.objects.create(title="hello", description="Description2", isbn="2222222")
        book3 = Book.objects.create(title="python", description="Description3", isbn="3333333")

        response = self.client.get(reverse("books:list") + "?q=science")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=hello")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=python")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)



class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1111111")

        user = CustomUser.objects.create(
            username="asadbek",  first_name="Asadbek", last_name="Abdumalikov", email="asadbekabdumalikovfifth@gmail.com"
        )
        user.set_password("somepassword")
        user.save()
        self.client.login(username="asadbek", password="somepassword")

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={ "stars_given": 3, "comment": "Nice book" })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)

  