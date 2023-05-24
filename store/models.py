from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)              # slug is a short label for something containing only letters, _ or -. They are generally used in urls

    class Meta:
        verbose_name_plural = 'Categories'              # used to change the spelling of the model in the admin page
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    no_of_items = models.IntegerField(default=1)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)                   # sets the products in the order they were created

    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail((self.image))
                self.save()

                return self.thumbnail.url
            else:
                return 'https://png.pngtree.com/thumb_back/fh260/background/20210207/pngtree-gray-simple-gradient-background-image_557031.jpg'

    
    def make_thumbnail(self, image, size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail
    

class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)








