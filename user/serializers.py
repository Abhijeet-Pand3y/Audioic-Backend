import imp
from pyexpat import model
from rest_framework import serializers
from .models import User


class UserSerializers(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        


    def update(self, instance, validated_data):
        for attr, value in validated_data:
            if attr == "password":
                instance.set_password(attr)
            else:
                setattr(instance, value, attr)
        instance.save()
        return instance

    class Meta:
        model = User
        #putting password in write only mode
        extra_kwargs = {"password": {"write_only": True}}
        
        fields = ("uname", "password", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "is_verified", "user_photo")