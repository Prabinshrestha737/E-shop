from django.db import models 

from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0)
    descripiton = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to='uploads/products/', height_field=None, width_field=None, max_length=None)



    @staticmethod 
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.objects.all()