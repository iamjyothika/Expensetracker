from rest_framework import serializers
from .models import UserModel,ExpenseModel,CategoryModel

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserModel 
        fields=["email","password","username"] 

        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user 


class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    class Meta:
        model=UserModel
        fields=['username','password']

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all())

    class Meta:
        model = ExpenseModel
        fields = ['id', 'user', 'amount', 'category', 'date', 'description']

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name']        