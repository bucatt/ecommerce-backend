

# from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product, OrderProduct, ShoppingCartProduct,ProductCategory, ShoppingCart, Payment, Order
from django.contrib.auth import authenticate, login

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        if self.request.user.is_staff or self.request.user == instance.user:
            instance.delete()
        else:
            raise PermissionDenied

        
@api_view(['GET', 'POST', "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_products_view(request):
    if request.method == 'GET':
        user_id = request.user.id
        # Obtener los productos del carrito del usuario actual
        cart_products = ShoppingCartProduct.objects.filter(shopping_cart__user_id=user_id)
        # Serializar los productos del carrito
        serializer = ShoppingCartProductSerializer(cart_products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        # Serializar el nuevo producto
        serializer = ShoppingCartProductSerializer(data=data)
        # Validar el serializador
    if serializer.is_valid():
        serializer.save(shopping_cart=ShoppingCart.objects.get(user=request.user))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
    try:
        # Obtener el producto a eliminar
        product = ShoppingCartProduct.objects.get(pk=request.data['id'])
    except ShoppingCartProduct.DoesNotExist:
        return JsonResponse({'message': 'The product does not exist in the cart', 'status': status.HTTP_404_NOT_FOUND


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def orders_view(request):
    if request.method == 'GET':
        data = list(Order.objects.values())
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        # Creamos un nuevo elemento con los datos proporcionados en la solicitud
        data = request.POST
        user_id = request.user.id
        shopping_cart = ShoppingCart.objects.get(user=request.user)
        item = Order.objects.create(shipping_address=data['shipping_address'], billing_address=data['billing_address'],
        total_price=data['total_price'], shopping_cart_id=shopping_cart.id)
        # Serializamos el elemento creado y lo devolvemos como respuesta
        serialized_item = {"shipping_address": item.shipping_address, "billing_address": item.billing_address, 
        "total_price": item.total_price, "shopping_cart_id": shopping_cart.id,}
        return JsonResponse(serialized_item, safe=False)
    elif request.method == 'DELETE':
        data = request.POST
        item = Order.objects.get(pk=data['id'])
        item.delete()
        return JsonResponse({'message': 'The order has been deleted', 'status': 204})
    elif request.method == 'PUT':
        data = request.POST
        item = Order.objects.get(pk=data['id'])
        item.shipping_address = data['shipping_address']
        item.billing_address = data['billing_address']
        item.total_price = data['total_price']
        shopping_cart = ShoppingCart.objects.get(pk=item.shopping_cart.id)
        item.shopping_cart = shopping_cart
        item.save()
        return JsonResponse({'message': 'The product has been updated', 'status': 200})

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def payments_view(request):
    if request.method == 'GET':
        data = list(Payment.objects.values())
        return JsonResponse(data, safe=False)
        # return HttpResponse("hello world", status=200)
    elif request.method == 'POST':
        # Creamos un nuevo elemento con los datos proporcionados en la solicitud
        data = request.POST
        item = Payment.objects.create(order_id=data['order_id'], payment_method=data['payment_method'],
        payment_status=data['payment_status'])
        # Serializamos el elemento creado y lo devolvemos como respuesta
        serialized_item = {"order_id": item.order.id, "payment_method": item.payment_method, 
        "payment_status": item.payment_status}
        return JsonResponse(serialized_item, safe=False)
    elif request.method == 'DELETE':
        data = request.POST
        item = Payment.objects.get(pk=data['id'])
        item.delete()
        return JsonResponse({'message': 'The payment has been deleted', 'status': 204})
    elif request.method == 'PUT':
        data = request.POST
        item = Payment.objects.get(pk=data['id'])
        item.payment_method = data['payment_method']
        item.payment_status = data['payment_status']
        # order = Order.objects.get(pk=item.id)
        # item.order = order
        item.save()
        return JsonResponse({'message': 'The product has been updated', 'status': 200})


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def orders_products_view(request):
    if request.method == 'GET':
        data = list(OrderProduct.objects.values())
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        # Creamos un nuevo elemento con los datos proporcionados en la solicitud
        data = request.POST

        order = Order.objects.get(pk=data["order_id"])
        product = Product.objects.get(pk=data["product_id"])

        item = OrderProduct.objects.create(quantity=data['quantity'], order=order,
        product=product)

        # Serializamos el elemento creado y lo devolvemos como respuesta
        serialized_item = {"quantity": item.quantity, "order_id": item.order.id, 
        "product_id": item.product.id}
        return JsonResponse(serialized_item, safe=False)
    elif request.method == 'DELETE':
        data = request.POST
        item = OrderProduct.objects.get(pk=data['id'])
        item.delete()
        return JsonResponse({'message': 'The order product has been deleted', 'status': 204})
    elif request.method == 'PUT':
        data = request.POST
        item = OrderProduct.objects.get(pk=data['id'])
        item.quantity = data['quantity']
        item.order_id = item.order.id
        item.product_id = item.product.id
        item.save()
        return JsonResponse({'message': 'The product has been updated', 'status': 200})

def generate_token(user):
    serializer = TokenObtainPairSerializer(user)
    return serializer.validate(user)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Usa el backend para autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
        # Si el usuario se autenticó correctamente, genera un token de autenticación
        # y lo devuelve en la respuesta
            token = generate_token(user)
            return JsonResponse({'success': True, 'token': token})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid login credentials'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
