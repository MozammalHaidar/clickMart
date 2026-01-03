from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, CartItem
from rest_framework.response import Response
from .models import Order,OrderItem
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_order_notification
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Create your views here.

class PlaceOrderView(APIView):
    # User must be logged in
    permissin_classes = [IsAuthenticated]

    def post(self,request):

        # Check if the cart is empty
        cart = Cart.objects.get(user=request.user)
        shipping_address = request.data.get("shippingAddress")
        if not cart or cart.items.count()==0:
            return Response({"errors":"Cart is empty."})
        
        # Create the order
        order = Order.objects.create(
            user = request.user,
            subtotal = cart.subtotal,
            tax_amount = cart.tax_amount,
            grand_total = cart.grand_total,
            address = shipping_address.get("address"),
            phone = shipping_address.get("phone"),
            city = shipping_address.get("city"),
            state = shipping_address.get("state"),
            zip_code = shipping_address.get("zipCode")
        )

        # loop through the cart items

        for item in cart.items.all():
            product = item.product

            # check quqntity
            if product.stock < item.quantity:
                return Response ({"details":f'Only {product.stock} is left for {product.name}'},
                                 status = status.HTTP_400_BAD_REQUEST)
            
            # Decrease the stock

            product.stock -= item.quantity # product.stock = product.stock-item.quantity
            product.save()


        # Create order item
        for item in cart.items.all():
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price,
                total_price = item.total_price
            )


        # Clear the cart items
        
        cart.items.all().delete()
        cart.save()

        # Send notification email

        send_order_notification(order)
        # Send the response to frontend

        serializer = OrderSerializer(order)
        return Response(serializer.data, status = status.HTTP_201_created)

class MyOrderView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order,pk=pk,user=self.request.user)
        return order