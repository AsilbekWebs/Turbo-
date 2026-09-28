from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Product
from .models import Cart, CartItem
from .serializer import (
    CartSerializer, AddToCartSerializer, RemoveFromCartSerializer, UpdateQuantitySerializer,
)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(CartSerializer(get_user_cart(request.user)).data)


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = generics.get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        cart = get_user_cart(request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()
        new_quantity = quantity + (item.quantity if item else 0)

        if new_quantity > product.stock:
            return Response(
                {'detail': f"Omborda yetarli emas. Qoldiq: {product.stock} ta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if item:
            item.quantity = new_quantity
            item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_user_cart(request.user)
        item = generics.get_object_or_404(CartItem, cart=cart, product_id=serializer.validated_data['product_id'])
        item.delete()
        return Response(CartSerializer(cart).data)


class CartItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_item(self, request, id):
        return generics.get_object_or_404(CartItem, id=id, cart=get_user_cart(request.user))

    def patch(self, request, id):
        item = self.get_item(request, id)
        serializer = UpdateQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
        if quantity > item.product.stock:
            return Response({'detail': f"Omborda yetarli emas. Qoldiq: {item.product.stock} ta."},
                            status=status.HTTP_400_BAD_REQUEST)
        item.quantity = quantity
        item.save()
        return Response(CartSerializer(item.cart).data)

    def delete(self, request, id):
        item = self.get_item(request, id)
        cart = item.cart
        item.delete()
        return Response(CartSerializer(cart).data)


class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        get_user_cart(request.user).items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)