from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from django.shortcuts import get_object_or_404
from main.models import Category, Product, ProductColor, ProductImage, ProductShop, Contact


class UserSerializers(ModelSerializer):
    confirm_password = CharField(max_length=50, read_only=True)

    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'username', 'password', 'confirm_password', 'email'

    def create(self, validated_data):
        password = validated_data['password']
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError('Invalid User')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.confirm_password = validated_data.get('confirm_password', instance.confirm_password)
        instance.name = validated_data.get('first_name', instance.name)
        instance.username = validated_data.get('last_name', instance.username)
        instance.email = validated_data.get('email', instance.email)

        new_password = validated_data.get('password')
        if new_password:
            instance.password = make_password(new_password)

        instance.save()
        return instance


class UserActiveSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'is_staff'


class ProductShopModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    sum_price = ReadOnlyField()

    class Meta:
        model = ProductShop
        fields = "id", "user", "product", "count", "color", "created_at", "sum_price"

    def create(self, validated_data):
        count = validated_data.get('count')
        product = validated_data['product']
        if not isinstance(product, Product):
            product = get_object_or_404(Product, pk=product)
        if count <= product.quantity:
            product.quantity -= count
            product.save()
            return super().create(validated_data)
        raise ValidationError("Buncha mahsulot yo'q")


class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class ProductColorModelSerializer(ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('color',)


class ProductModelSerializer(ModelSerializer):
    to_category = CategoryModelSerializer(many=True, read_only=True)
    to_color = ProductColorModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("to_product", 'image',)


class PostActiveSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("is_active",)
