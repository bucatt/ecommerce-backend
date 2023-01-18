from rest_framework import serializers
from .models import Product, ProductCategory, Offer, ShoppingCart, Order, OrderProduct, Payment, ShoppingCartProduct

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description')

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'name', 'start_date', 'end_date', 'discount_percentage')

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    offers = OfferSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'image', 'category', 'offers')

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user')

class OrderSerializer(serializers.ModelSerializer):
    shopping_cart = ShoppingCartSerializer()
    class Meta:
        model = Order
        fields = ('id', 'shopping_cart', 'shipping_address', 'billing_address', 'total_price')

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'quantity', 'discount')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'payment_method', 'payment_status')

class ShoppingCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ShoppingCartProduct
        fields = ('id', 'shopping_cart', 'product', 'quantity')



