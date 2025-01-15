from django.contrib import admin
from . models import ClientLocInfo,DataPriceAC,Addon,DataCostElecAC,Payment,CalcostAc

admin.site.register(ClientLocInfo)


class StatementAdmin(admin.ModelAdmin):
    list_display =[
        "priceHV","pricetr100","pricetr160","pricetr250","pricetr315",
        "priceTRtoMDB","priceMDBtoEV","priceEV7","priceEV22"    
    ]

admin.site.register(DataPriceAC,StatementAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display =[
        "addon1","addon2","addon3","addon4","addon5","addon6","addon7","addon8","addon9","addon10"
        ,"addon11","addon12","addon13","addon14","addon15"
      
    ]
admin.site.register(Addon,StatementAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display =[
        "fee","unnitperhour","dayserviceperyear","price22onpeak","priceless22onpeak","price22offpeak",
        "priceless22offpeak" 
    ]
admin.site.register(DataCostElecAC,StatementAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display =[
        "customer","email","tel","amount","created_at"
      
    ]
admin.site.register(Payment,StatementAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display =[
        "created_at_cost","size_tr","disthvtotr","numev","price_ev_7kw","packageadd","distrtomdb",
        "distmdbtoev","costtotal","addon_total","cal_costtotal_addon"
      
    ]
admin.site.register(CalcostAc,StatementAdmin)