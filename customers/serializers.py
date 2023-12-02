from rest_framework import serializers
from .models import Customer
from django.contrib.auth import get_user_model

class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'first_name', 'last_name', 'image_url', 'phone', 'id', 'user', 'address',
        )
        read_only_fields = ('id', 'email',)

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else ""

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else ""
    
    def get_address(self, obj):
        return obj.user.get_user_address() if obj.user else ""