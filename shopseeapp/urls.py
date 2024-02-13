
from django.contrib import admin
from django.urls import path,include
from shopseeapp import views
from django.conf.urls.static import static 
from django.conf import settings 

app_name = 'ecomapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('login',views.loginuser,name="login"),
    path('logout',views.logoutuser,name="logout"),
    
     path('register',views.registeruser,name="Register"),




     path('category',views.category,name="category"),
     
     path('subcategory/<slug:val>',views.subcategoryView.as_view(), name='subcategory'),

        path('product/<slug:val>',views.productView.as_view(), name='product'),

      path('prod-details/<slug:val>',views.productdetail, name='productdetails'),
      
      

      path('add_to_cart',views.add_to_cart,name="add to cart"),
      path('cart',views.show_cart,name="show cart"),
       path('pluscart/',views.plus_cart,name="plus cart"),
       path('minuscart/',views.minus_cart,name="minus cart"),
       path('removecart/',views.remove_cart,name="minus cart"),


       path('add_to_fav',views.add_to_fav,name="add fav"),
       path('fav',views.fav,name="fav"),
       path('contact',views.contact,name="contact"),

       


       path('aboutus',views.aboutus,name="aboutus"),

        path('checkout',views.checkout,name="checkout"),
     
            path('profile-update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('order', views.order, name='order'),
    path('razorpay_callback', views.CallbackView.as_view(), name='razorpay_callback'),

       
     

   
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
