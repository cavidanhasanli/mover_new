from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import status
from bs4 import BeautifulSoup
from lxml import html
from .models import *
from .serializers import *
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



class ApiIndexView(APIView):

    def get(self,request,*args, **kwargs):
        return JsonResponse({'status':"OK"})

    def clean_data(self):

        data = {}
        for k, v in self.request.data.items():
            clean = re.compile('>.*?<')
            texts = re.sub(clean,'><',v)
            data.update({k:texts})
        return data

    def get_attribute_from_html(self, data):
        result = {}
        for key, value in data.items():
            if "url" != key:
                pars = BeautifulSoup(value, "html.parser").find()
                if pars.get("id", False):
                    parsed_data = "#" + pars.get("id")
                    result[key] = parsed_data
                elif pars.get("src", False):
                    parsed_data = "@" + pars.get("src")
                    result[key] = parsed_data
                elif pars.get("class", False):
                    parsed_data = "." + " ".join(pars.get("class"))
                    result[key] = parsed_data
            else:
                result[key] = value
        return result

    def post(self, request, *args, **kwargs):
        
        clean_data = self.clean_data()
        data = self.get_attribute_from_html(clean_data)
        print(data)
        serializer = DataInfo(data=data)
        if serializer.is_valid():
            if serializer.is_valid():
                detail = ProductTag(**serializer.data)
                detail.save()
            
            return JsonResponse({'data': serializer.data})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScraperView(generic.View):

    def scrapper(self, url, data):
        result = {}
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        for key, value in data.items():
            if value.startswith("."):
                result[key] = driver.find_element_by_class_name(value[1:]).text
            elif value.startswith("@"):
                result[key] = driver.find_element_by_xpath('//img[@src="{}"]'.format(value[1:])).get_attribute("src")

            elif value.startswith("#"):
                result[key] = driver.find_element_by_id(value[1:]).text
        driver.quit()
        return result

    def get(self, request, *args, **kwargs):
        data = ProductTag.objects.all().last()
        obj = model_to_dict(data, fields=["name","size","price","url","image"])
        latest_result = self.scrapper(data.url, obj)
        return JsonResponse({"status":"OK", "data": latest_result})

