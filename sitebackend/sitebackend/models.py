from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
        }

class Offer(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    image = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    offers = models.ManyToManyField(Offer, blank=True)
    
    def __str__(self):
        return self.name



class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'ShoppingCart {self.id}'

class Order(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order {self.id}'
    def recalculate_total_price(self):
        total = 0
        for order_product in self.orderproduct_set.all():
            total += order_product.product.price * order_product.quantity
        self.total_price = total
        self.save()

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'OrderProduct {self.id}'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    
    def __str__(self):
        return f'Payment {self.id}'

class ShoppingCartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)

    class Meta:
        unique_together = ('product', 'shopping_cart')

    def __str__(self):
        return f'ShoppingCartProduct {self.id}'