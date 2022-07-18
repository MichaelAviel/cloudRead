from django.db import models
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
# Create your models here.

class BookType(models.TextChoices):
    Fiction = 'Fiction'
    NonFiction = 'NonFiction'
    Comic = 'Comic'


class BookGenre(models.TextChoices):
    Fantasy = 'Fantasy'
    Horror = 'Horror'
    ScienceFiction = 'ScienceFiction'
    Biography = 'Biography'
    Action = 'Action'
    Adventure = 'Adventure'
    Mystery = 'Mystery'
    Thriller = 'Thriller'
    Suspense = 'Suspense'
    Historical = 'Historical'
    Romance = 'Romance'
    Graphic = 'Graphic'
    Short = 'Short'
    AutoBiography = 'AutoBiography'
    Food = 'Food'
    Drink = 'Drink'
    Art = 'Art'
    History = 'History'
    TrueCrime = 'TrueCrime'
    Travel = 'Travel'
    Humor = 'Humor'
    Science = 'Science'
    Technology = 'Technology'
    Dystopian = 'Dystopian'
    Photography = 'Photography'



class Book(models.Model):
    title = models.CharField(max_length=400, null=True, blank=True)
    description = RichTextField(default="", blank=True, null=True)
    description_short = RichTextField(default="", blank=True, null=True)
    book_address = models.CharField(max_length=500, null=True, blank=True, default="")
    book_genre = MultiSelectField(choices=BookGenre.choices)
    book_category = MultiSelectField(choices=BookType.choices)
    file = models.FileField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    secret_access_code = models.CharField(max_length=400, null=True, blank=True, default="")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        # overrides the .save() function to add the coordinates before saving the Job.
        address = get_random_string(length=64)
        access_code = get_random_string(length=85)
        print(address)

        self.book_address = address
        self.secret_access_code = access_code
        super(Book, self).save(*args, **kwargs)
