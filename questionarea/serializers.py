from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["last_login", "username", "first_name", "last_name", "date_joined"]

class QuestionSerializer(serializers.ModelSerializer):
    ask_byy = serializers.SerializerMethodField()

    def get_ask_byy(self, instance):
        usr = User.objects.all().filter(id=instance.ask_by.id).last()
        ser = UserSerializer(usr)
        return ser.data

    class Meta:
        model = Question
        fields = ["title", "description", "created", "last_modified", "ask_by"]

class QuesSerializer(serializers.ModelSerializer):
    ask_by = serializers.SerializerMethodField()

    def get_ask_by(self, instance):
        usr = User.objects.all().filter(id=instance.ask_by.id).last()
        ser = UserSerializer(usr)
        return ser.data

    class Meta:
        model = Question
        fields = ["title", "description", "created", "last_modified", "ask_by"]