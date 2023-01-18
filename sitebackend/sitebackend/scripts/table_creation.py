from django.contrib.auth.models import User
from ..models import ProductCategory, Product, ShoppingCart, Order, Payment, ShoppingCartProduct

def agregar_registros():
    # Creamos una categoría de productos
    category = ProductCategory.objects.create(name='Celulares', description='Dispositivos móviles')

    # Creamos algunos productos
    Product.objects.create(name='iPhone 11', price='799.99', description='El último celular de Apple', image='https://example.com/iphone11.jpg', category=category)
    Product.objects.create(name='Galaxy S20', price='799.99', description='El último celular de Samsung', image='https://example.com/galaxys20.jpg', category=category)
    Product.objects.create(name='Pixel 4', price='799.99', description='El último celular de Google', image='https://example.com/pixel4.jpg', category=category)

    # Creamos un usuario y un carrito de compras para él
    user = User.objects.create_user(username='johndoe', password='password')
    shopping_cart = ShoppingCart.objects.create(user=user)

    # Añadimos algunos productos al carrito de compras
    ShoppingCartProduct.objects.create(shopping_cart=shopping_cart, product=Product.objects.get(name='iPhone 11'))
    ShoppingCartProduct.objects.create(shopping_cart=shopping_cart, product=Product.objects.get(name='Galaxy S20'))

    # Creamos un pedido y un pago
    order = Order.objects.create(shopping_cart=shopping_cart, shipping_address='123 Main St', billing_address='456 Main St', total_price='1599.98')
    payment = Payment.objects.create(order=order, payment_method='tarjeta de crédito', payment_status='aprobado')

# Llamamos a la función para agregar los registros
agregar_registros()