from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.db.models import Avg
from django.contrib.auth import get_user_model

from apps.profiles.serializers import ShippingAddressSerializer
from apps.shop.models import Category, Product, Review


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = Category
        fields = ['name', 'image']  # image обязательно ImageField!



class SellerShopSerializer(serializers.Serializer):
    name = serializers.CharField(source="business_name")
    slug = serializers.SlugField()
    avatar = serializers.CharField(source="user.avatar")


class ProductSerializer(serializers.Serializer):
    seller = SellerShopSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    desc = serializers.CharField()
    price_old = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = CategorySerializer()
    in_stock = serializers.IntegerField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)

    average_rating = serializers.FloatField(read_only=True)


class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    desc = serializers.CharField()
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_slug = serializers.SlugField()
    in_stock = serializers.IntegerField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)


class OrderItemProductSerializer(serializers.Serializer):
    seller = SellerShopSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price_current"
    )


class OrderItemSerializer(serializers.Serializer):
    product = OrderItemProductSerializer()
    quantity = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, source="get_total")


class ToggleCartItemSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    quantity = serializers.IntegerField(min_value=0)


class CheckoutSerializer(serializers.Serializer):
    shipping_id = serializers.UUIDField()


class OrderSerializer(serializers.Serializer):
    tx_ref = serializers.CharField()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    delivery_status = serializers.CharField()
    payment_status = serializers.CharField()
    date_delivered = serializers.DateTimeField()
    shipping_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        max_digits=100, decimal_places=2, source="get_cart_subtotal"
    )
    total = serializers.DecimalField(
        max_digits=100, decimal_places=2, source="get_cart_total"
    )

    @extend_schema_field(ShippingAddressSerializer)
    def get_shipping_details(self, obj):
        return ShippingAddressSerializer(obj).data


class CheckItemOrderSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total = serializers.FloatField(source="get_total")


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "text"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        view = self.context.get("view")
        product = None
        if view and hasattr(view, "kwargs"):
            slug = view.kwargs.get("slug")
            if slug:
                product = Product.objects.get_or_none(slug=slug)

        if self.instance is None:
            if product and Review.objects.filter(user=user, product=product).exists():
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв на этот товар."
                )
        else:
            if self.instance.user != user:
                raise serializers.ValidationError(
                    "Нельзя изменять чужой отзыв."
                )

        return attrs





