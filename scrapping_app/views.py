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
        tag_name = []
        for key, value in data.items():
            print("line 37", key, value)
            if "url" != key:
                pars = BeautifulSoup(value, "html.parser").find()
                if pars.get("id", False):
                    parsed_data = "#" + pars.get("id")
                    result[key] = parsed_data + "|" + pars.name
                elif pars.get("src", False):
                    parsed_data = "@" + pars.get("src")
                    result[key] = parsed_data  + "|" + pars.name
                elif pars.get("class", False):
                    parsed_data = "." + " ".join(pars.get("class"))
                    result[key] = parsed_data + "|" + pars.name
                elif pars.get('itemprop', False):
                    parsed_data = "&" + pars.get("itemprop")
                    result[key] = parsed_data + "|" + pars.name
                else:
                    print("line 50", key, tag_name)
                    tag_name.append(key)
            else:
                print("line 53", key, value, result)
                result[key] = value
        if tag_name:
            return [result, tag_name]
        return result

    def post(self, request, *args, **kwargs):
        
        clean_data = self.clean_data()
        data = self.get_attribute_from_html(clean_data)
        print("line 63", data)
        if isinstance(data, dict):
            
            product = ProductTag.objects.create()
            product.name = data.get("url")
            product.bulk_insert(**data)
            product.save()
            return JsonResponse({'data': data})
            # return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = data[0]
            print("ELEMENT",data[1])
            for tag in data[1]:
                result[tag] = self.request.data[tag]
            product = ProductTag.objects.create()
            print(result.get("url"))
            product.name = result.get("url")
            product.bulk_insert(**result)
            product.save()
            return JsonResponse({'data': result})
            


class ScraperView(generic.View):

    def scrapper(self, url, data):
        result = {}
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        # print("HTML_SOURCE: ", driver.page_source)
        pars = BeautifulSoup(driver.page_source, "html.parser")
        #print(dir(pars))
        for obj in data:
            key, value, tag_name = obj.get("field"), obj.get("value"), obj.get("tag_name")
            # print(key, value, tag_name)
            #print(pars)
            if value.startswith("."):
                print("line 102", key, value, tag_name)
                # print("PARS TYPE: ", pars)
                #result[key] = pars.find_all(tag_name, {"class":value[1:]})[0].text
                result[key] = pars.find_all(tag_name, {"class": value[1:]})[0].text if pars.find_all(tag_name, {"class": value[1:]}) else "yoxdu"
                # print("//{}[{}]".format(tag_name," or ".join(["@class='{}'".format(item) for item in value[1:].split(" ")])))
                #result[key] = driver.find_elements_by_xpath("//{}[{}]".format(tag_name," or ".join(["@class='{}'".format(item) for item in value[1:].split(" ")])))[0].text
                
            elif value.startswith("@"):
                print("line 110", key, value, tag_name)
                result[key] = driver.find_element_by_xpath('//*[@src="{}"]'.format(value[1:])).get_attribute("src")
            elif value.startswith("&"):
                print("line 116", key, value, tag_name)
                result[key] = driver.find_element_by_xpath('//*[@itemprop="{}"]'.format(value[1:])).text

            elif value.startswith("<"):
                print("line 114", key, value, tag_name)
                pars = BeautifulSoup(value, "html.parser").find()
                print(pars.text)

                # sozler = list(filter(lambda x: x.strip(), pars.text.split(" ")))
                # print(driver.find_elements_by_xpath("//*[contains(text(), 'Dik') and contains(text(), 'Yakali') and]".format(pars.text))[0].text)

            
                result[key] = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(pars.text))[0].text if driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(pars.text))[0] else "yoxdu"
                
                # <h1 itemprop="name">Dik Yakalı Suni Deri Ceket</h1>
                
    
            elif value.startswith("#"):
                print("line 121", key, value, tag_name)
                result[key] = pars.find_all(tag_name, {"id": value[1:]})[0].text if pars.find_all(tag_name, {"id": value[1:]}) else "yoxdu"
                #result[key] = driver.find_element_by_id(value[1:]).text
        driver.quit()
        return result

    def get(self, request, *args, **kwargs):
        data = ProductTag.objects.all().last()
        obj = ProductSerializers(data)
        latest_result = self.scrapper(data.name, obj.data.get("product_tags"))
        return JsonResponse({"status":"OK", "data": latest_result})

