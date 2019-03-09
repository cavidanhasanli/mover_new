from rest_framework import serializers
from .models import *

class DataInfo(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["name","size","price","url","image"]
