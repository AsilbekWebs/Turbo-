from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.views import get_user_cart
from catalog.models import Product
from .models import Order, OrderItem
from .serializer import OrderSerializer, CheckoutSerializer, OrderStatusSerializer


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_user_cart(request.user)
        cart_items = list(cart.items.all())
        if not cart_items:
            return Response({'detail': "Savat bo'sh."}, status=status.HTTP_400_BAD_REQUEST)


        products = Product.objects.select_for_update().in_bulk([i.product_id for i in cart_items])

        for item in cart_items:
            product = products[item.product_id]
            if product.stock < item.quantity:
                raise ValidationError(
                    {'detail': f"'{product.name}' omborda yetarli emas. Qoldiq: {product.stock} ta."}
                )

        total = sum((products[i.product_id].price * i.quantity for i in cart_items), Decimal('0'))
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            shipping_address=serializer.validated_data['shipping_address'],
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=products[i.product_id],
                product_name=products[i.product_id].name,
                quantity=i.quantity,
                price_at_that_time=products[i.product_id].price,
            )
            for i in cart_items
        ])

        for item in cart_items:
            Product.objects.filter(id=item.product_id).update(stock=F('stock') - item.quantity)

        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.select_related('user').prefetch_related('items')
    filterset_fields = ['status']


class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    lookup_field = 'id'
    http_method_names = ['patch']