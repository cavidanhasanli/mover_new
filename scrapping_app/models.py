from django.db import models
   
#class OrderStatus(models.Model):
#    name = models.CharField(max_length=255)
#
#    def __str__(self):
#        return self.name
#    
#
#class SelectedProducts(models.Model):
#    name = models.CharField(max_length=255)
#    size = models.CharField( max_length=50)
#    color = models.CharField(max_length=50)
#    image = models.ImageField(upload_to='media')
#    price = models.DecimalField(max_digits=7, decimal_places=2)
#    url = models.URLField(max_length=255)
#    order = models.ForeignKey("SelectedOrders",  on_delete=models.CASCADE,null=True, blank=True)
#
#    def __str__(self):
#        return self.name
#
#    
#class SelectedOrders(models.Model):
#    tracking_number = models.IntegerField()
#    order_number = models.IntegerField()
#    price = models.DecimalField(max_digits=7, decimal_places=2)
#    invoice = models.IntegerField()
#    url = models.URLField(max_length=255)
#    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE, 
#                                null=True,blank=True)
# class ProductItem()

class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    url = models.URLField(max_length=500)
    
    

    def __str__(self):
        return "{} {} {}".format(self.name,self.price,self.size,self.image)

    

    
    
