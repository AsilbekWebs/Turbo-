from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def to_internal_value(self, data):
        if 'product_id' not in data and 'product' in data:
            data = data.copy()
            data['product_id'] = data['product']
        return super().to_internal_value(data)


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class UpdateQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)