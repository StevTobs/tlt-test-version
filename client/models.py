from django.db import models
from account.models import CustomUser

# class ClientReport(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     province = models.CharField(max_length=100)
#     amphure = models.CharField(max_length=100, null=True, blank=True)
#     tambon = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Report for {self.user.username} - {self.province}"


class ClientLocInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    size_charger = models.CharField(max_length=100)
    num_charger = models.IntegerField()
    budget = models.FloatField()
    POI = models.CharField(max_length=100)  # Place of Interest
    ROI = models.FloatField()  # Return on Investment

    is_premium = models.BooleanField(default=False, verbose_name="Is this a premium location?")

    user = models.ForeignKey(CustomUser, max_length=10, on_delete=models.CASCADE, null=True)


class DataPriceAC (models.Model):
    priceHV = models.FloatField(default=47621.48)
    pricetr100 = models.FloatField(default=494589.76)
    pricetr160 = models.FloatField(default=594384.00)
    pricetr250 = models.FloatField(default=705095.10)
    pricetr315 = models.FloatField(default=1192509.79)
    priceTRtoMDB = models.FloatField(default=280.0)
    priceMDBtoEV = models.FloatField(default=280.0)
    priceEV7 = models.FloatField(default=21900.0)
    priceEV22 = models.FloatField(default=0.0)
    pricePackage = models.FloatField(default=16100.0)
    choices =(
        ("addpackage" , "รวม"),
        ("nonpackage" , "ไม่รวม")
    )

    package = models.CharField(max_length=100,choices=choices,default=1)

class DataCostElecAC(models.Model):
       fee = models.FloatField(default=0.20)
       unnitperhour = models.FloatField(default=7.0)
       dayserviceperyear = models.IntegerField(default=120)
       price22onpeak = models.FloatField(default=4.1839)
       priceless22onpeak = models.FloatField(default=4.3297)
       price22offpeak = models.FloatField(default=2.6037)
       priceless22offpeak = models.FloatField(default=2.6369)
    

class Payment(models.Model):
    customer = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')
    tel = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=2590 )
    created_at = models.DateTimeField(auto_now_add=True)


class Addon(models.Model):
    addon1 = models.IntegerField(default=330)    
    addon2 = models.IntegerField(default=550)
    addon3 = models.IntegerField(default=220)  
    addon4 = models.IntegerField(default=330) 
    addon5 = models.IntegerField(default=810) 
    addon6 = models.IntegerField(default=1300) 
    addon7 = models.IntegerField(default=1400) 
    addon8 = models.IntegerField(default=1650) 
    addon9 = models.IntegerField(default=3750) 
    addon10 = models.IntegerField(default=6450) 
    addon11 = models.IntegerField(default=5350) 
    addon12 = models.IntegerField(default=1650)
    addon13 = models.IntegerField(default=23600)
    addon14 = models.IntegerField(default=23600)
    addon15 = models.IntegerField(default=6450) 


class Payment(models.Model):
    customer = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')
    tel = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=2590 )
    created_at = models.DateTimeField(auto_now_add=True)

class CalcostAc(models.Model):
     created_at_cost = models.DateTimeField(auto_now_add=True)
     size_tr = models.CharField(max_length=10, blank=True, null=True)
     disthvtotr = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     numev = models.IntegerField(blank=True, null=True)
     price_ev_7kw = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     packageadd = models.CharField(max_length=10, blank=True, null=True)
     distrtomdb = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     distmdbtoev = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     costtotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     addon_total = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
     cal_costtotal_addon = models.DecimalField(max_digits=10, decimal_places=2,default=0)