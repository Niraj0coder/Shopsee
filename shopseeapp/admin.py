from django.contrib import admin
from .models import *
# Register your models here.



class Adminsubcategory(admin.ModelAdmin):
    list_display=('category','name')
    search_fields = ['name']
admin.site.register(Category)


admin.site.register(Product)

admin.site.register(Subcategory,Adminsubcategory)

admin.site.register(Cart)




admin.site.register(Favourite)

admin.site.register(Contact)





admin.site.register(Profile)

admin.site.register(Order)
admin.site.register(Review)