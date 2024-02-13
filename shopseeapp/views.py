from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .form import *
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from shopsee.settings import *

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.template.loader import render_to_string
import os
import json


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# authorize razorpay client with API Keys.
client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
# Create your views here.
def index(request):

    prod=Product.objects.filter(offers=0)
    pro=Product.objects.filter(trending=0)
   
    return render(request,'index.html',{'product':prod,'pro':pro})




def loginuser(request):
        
        
        if request.method=='POST':
            uname=request.POST.get('uname')
            pas=request.POST.get('pass1')
            myuser =authenticate(username = uname, password = pas)
            if myuser is not None:
                login(request,myuser)
                
                return redirect('/')
            else:
                messages.info(request, 'Username or password is incorrect')
                return redirect('/login')

                

        return render(request,'accounts/login.html')
def logoutuser(request):

    logout(request)
    messages.info(request, 'Logout Sucessfully')
    return redirect('/login')

def registeruser(request):


    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
           
        if password != confirmpassword:
           messages.success(request,"Password Doesnot Match")
           return redirect('/register')
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/register')
        elif User.objects.filter(email = email).first():
            messages.error(request, "This email is already register Go to login page")
            return redirect('/register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            User.first_name=firstname
            User.last_name=lastname
            user.save()
            messages.error(request, "Account Registered SucessFully")   
    return render(request,'accounts/register.html')


def category(request):
    cat=Category.objects.filter(status=0)
    return render(request,'shop.html',{'cat':cat})


class subcategoryView(View):
    def get(self,request,val):
        cat=Category.objects.filter(status=0)
        subcat =Subcategory.objects.filter(category=val)
        return render(request,'subcategory.html' ,{'cat':cat,'subcat':subcat})


class productView(View):
    def get(self,request,val):
        cat=Category.objects.filter(status=0)
        product =Product.objects.filter(category=val)
        return render(request,'product.html' ,{'pro':product,'cat':cat})

def productdetail(request,val):
    product =Product.objects.filter(id=val,status=0)
    pro=Product.objects.filter(id=val).first()
    cat=Category.objects.filter(status=0)
    review=Review.objects.filter(products=val)
    
    
    if request.method=="POST":
        
        user=request.user
        email=request.user.email   
        desc=request.POST.get('desc')
        rate=request.POST.get('rate')
        Review(user=user,products=pro,Desc=desc,rate=rate,email=email).save()
        messages.success(request, "Sucesssfully posted your review")   
        return HttpResponseRedirect(request.path_info)
    return render(request,'shop-detail.html',{  'pro':product,'cat':cat,'review':review} )






def add_to_cart(request):
            if request.user.is_authenticated:
                pro=request.POST.get('prod')


                
                cart = Cart.objects.filter(user=request.user, products_id=pro).first()

                if cart:
                    cart.quantity += 1
                    cart.save()
                    messages.success(request, "Item added to your cart.")
                else:
                    Cart.objects.create(user=request.user, products_id=pro)
                    messages.success(request, "Item added to your cart.")
                
        

            

            
                return redirect('/cart')
            else:
                messages.warning(request, "Login To See Cart")
                return redirect('/login')




def show_cart(request):
        if request.user.is_authenticated:
            user=request.user
            cart=Cart.objects.filter(user=user)


            amount=0.0
            shipping_amount=60.0
            total_amount=0.0
            
            cart_product=[p for p in Cart.objects.all() if p.user ==user]

            if cart_product:
                for p in cart_product:
                    
                    tempamount=(p.quantity *p.products.discount_price)
                    amount +=tempamount
                    totalamount=amount+shipping_amount
                return render(request,'cart.html',{'cart':cart,'total_amount':totalamount,'amount':amount,})
            else:
                return render(request,'404.html')
        else:
             messages.warning(request, "Login To See Cart")
             return redirect('/login')
        

def plus_cart(request):
     if request.method=="GET":
          
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q (user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=60.0
        
        cart_product=[p for p in Cart.objects.all() if p.user ==request.user]

        if cart_product:
            for p in cart_product:
                  
                tempamount=(p.quantity *p.products.discount_price)
                amount +=tempamount
               

                data={
                     'quantity':c.quantity,
                     'amount':amount,
                    
                     'totalamount':amount+shipping_amount

                }
                return JsonResponse(data)
        
             
       



def minus_cart(request):
     if request.method=="GET":
          
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q (user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=60.0
        
        cart_product=[p for p in Cart.objects.all() if p.user ==request.user]

        if cart_product:
            for p in cart_product:
                  
                tempamount=(p.quantity *p.products.discount_price)
                amount +=tempamount
                totalamount=amount

                data={
                     'quantity':c.quantity,
                   'amount':amount,
                     'totalamount':totalamount+shipping_amount

                }
                return JsonResponse(data)
    
def remove_cart(request):
     if request.method=="GET":
          
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q (user=request.user))
       
        c.delete()
        amount=0.0
        shipping_amount=60.0
        
        cart_product=[p for p in Cart.objects.all() if p.user ==request.user]

        if cart_product:
            for p in cart_product:
                  
                tempamount=(p.quantity *p.products.discount_price)
                amount +=tempamount
               

                data={
                      'amount':amount,
                  
                     'totalamount':amount+shipping_amount

                }
                return JsonResponse(data)



def add_to_fav(request):
            pro=request.POST.get('prod')


            
            fav = Favourite.objects.filter(user=request.user, products_id=pro).first()

            if fav:
              
                fav.delete()
                messages.success(request, "Item removed from your cart.")
            else:
                Favourite.objects.create(user=request.user, products_id=pro)
                messages.success(request, "Item added to your cart.")
            
    

        

        
            return redirect('/fav')






def fav(request):
    if request.user.is_authenticated:
        user=request.user
        fav=Favourite.objects.filter(user=user)
        if fav:
            return render(request,'fav.html',{'fav':fav})
        else:
            return render(request,'404.html')
    else:   
        messages.warning(request, "Login To See WishList")
        return redirect('/login')
 



    
def aboutus(request):
    return render(request,'testimonial.html')




def contact(request):
    if request.user.is_authenticated:
    
        if request.method=="POST":
            myuser=request.user


            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            comment=request.POST.get('comment')
            
            contact=Contact(user=myuser,fname=fname,lname=lname,email=email,comment=comment)
            
            contact.save()
            return HttpResponseRedirect(request.path_info)
    
        return render(request,'contact.html')
    else:   
        messages.warning(request, "Login To Contact us")
        return redirect('/login')
    




def checkout(request):  
         
         user=request.user
         cart=Cart.objects.filter(user=user)
         amount=0.0
         shipping_amount=60.0
         total_amount=0.0
        
         cart_product=[p for p in Cart.objects.all() if p.user ==user]

         if cart_product:
            for p in cart_product:
                  
                  tempamount=(p.quantity *p.products.discount_price)
                  amount +=tempamount
                  totalamount=amount+shipping_amount

              
            return render(request,'chackout.html',{'cart':cart,'total_amount':totalamount,'amount':amount,})














class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'



    
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'accounts/update-profile.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None
      

        user_form = UserForm(post_data, instance=request.user)
       
        profile_form = ProfileForm(post_data, file_data,instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect('/profile')
     

        context = self.get_context_data(
             
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    







# orderrrrrrrr-------------------------



@csrf_exempt
def order(request):
    if request.user.is_authenticated:
        ord=Order.objects.filter(user=request.user)
        
    

        
        if request.method =="POST":
                user=request.user

        
                firstname=request.POST.get('fname')
                lastname=request.POST.get('lname')
                phonenumber=request.POST.get('phone')
                email=request.POST.get('email')
                
                amount=request.POST.get('amounts')
                address=request.POST.get('address')
                city=request.POST.get('city')
                pincode=request.POST.get('pincode')
                cart=Cart.objects.filter(user=user)
                amount_d=float(amount)
                for c in cart:
                    
                    order=Order(user=user,firstname=firstname,lastname=lastname,phonenumber=phonenumber,email=email,address=address,city=city,pincode=pincode,products=c.products,quantity=c.quantity)
                    order.save()
                    c.delete()
                
        
                
                    order_amount=int(float(amount))*100
                    order_currency='INR'
                    
                    callback_url = 'http://'+ str(get_current_site(request))+"/razorpay_callback" 
                    notes={'order-type':"basic order from website"}
                    razorpay_order= client.order.create(dict(amount=order_amount,notes = notes,currency=order_currency,payment_capture=1))
                    order.razorpay_order_id=razorpay_order['id']
                    order.save( )
                    
                    
            
            
            
            
            
            
                
                return render(request, 'payment/paymentsummaryrazorpay.html', {'ord':ord,'am':amount_d,'amount':order_amount,'api_key':RAZORPAY_API_KEY,'order':order, 'order_id': razorpay_order['id'], 'orderId':order.orderid, 'callback_url':callback_url})

            

                
                
        return render(request,'order.html', {'ord':ord})
    else:   
        messages.warning(request, "Login To manage Order")
        return redirect('/login')
    
   
 
class CallbackView(APIView):
    
    """
    APIView for Verifying Razorpay Order.
    :return: Success and failure response messages
    """

    @staticmethod
    def post(request, *args, **kwargs):

        # getting data form request
        response = request.data.dict()

        """
            if razorpay_signature is present in the request 
            it will try to verify
            else throw error_reason
        """
        if "razorpay_signature" in response:

            # Verifying Payment Signature
            data = client.utility.verify_payment_signature(response)

            # if we get here True signature
            if data:
                order = Order.objects.get(razorpay_order_id = response['razorpay_order_id'])                # razorpay_payment = RazorpayPayment.objects.get(order_id=response['razorpay_order_id'])
                order.payment_status = payment_choices.SUCCESS
                order.razorpay_payment_id = response['razorpay_payment_id']
                order.razorpay_signature = response['razorpay_signature']          
                order.save()
                
                
          

                
                
                

                return render(request,'payment/paymentsucess.html',{'status': 'SUCCESS','order':order},status=status.HTTP_200_OK)
            else:
                return render(request,'payment/paymentfail.html',{'status': 'Signature Mismatch','order':order},status=status.HTTP_400_BAD_REQUEST)

        # Handling failed payments
        else:
            error_code = response['error[code]']
            error_description = response['error[description]']
            error_source = response['error[source]']
            error_reason = response['error[reason]']
            error_metadata = json.loads(response['error[metadata]'])
            razorpay_payment =   Order.objects.get(razorpay_order_id=error_metadata['order_id'])
            razorpay_payment.razorpay_payment_id = error_metadata['payment_id']
            razorpay_payment.razorpay_signature = "None"
            razorpay_payment.payment_status = payment_choices.FAILURE
            razorpay_payment.save()

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }
            
            return render(request,'payment/paymentfail.html',{'status': error_status,'order':razorpay_payment}, status=status.HTTP_401_UNAUTHORIZED)