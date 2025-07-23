from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from .models import  MenuItem
from .models import Category

import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(
    #     max_length=255,
    #     validators=[UniqueValidator(queryset=MenuItem.objects.all())],    
    # )
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    # def validate_title(self, value):
    #     return bleach.clean(value, strip=False)

    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     return value
    
    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     return value

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        # extra_kwargs = {
        #     'price':{'min_value': 2},
        #     'stock':{'source':'inventory', 'min_value': 0},
        #     # 'title': {
        #     #     'validators': [
        #     #         UniqueValidator(
        #     #             queryset=MenuItem.objects.all()
        #     #         )
        #     #     ]
        #     # }
        # }
    
    def calculate_tax(self, Product:MenuItem):
        return Product.price * Decimal('1.1')