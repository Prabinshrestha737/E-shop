from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from django.views import View

from .models.product import * 
from .models.category import * 
from .models.customer import *

# Create your views here.


class Index(View):

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        categories = Category.get_all_categories()

        categoryID = request.GET.get('category')
    
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        
        else:
            products = Product.get_all_products()

        data  = {}


        data['products'] = products
        data['categories'] = categories 
        print('you are: ', request.session.get('email'))

        return render(request, 'index.html', data)


    def post(self, request):
        product = request.POST.get('product')
        # request.session.get('cart').clear()
        cart = request.session.get('cart')

        remove = request.POST.get('remove')  
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart
        print(request.session['cart'])


        return redirect('index')




class SignUp(View):
    a = "edkas"

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('number')
        email = postData.get('email')
        password = postData.get('password')

        #validation 

        value = {
            'first_name' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email
        }

        error_message = None

        customer = Customer(first_name = first_name, 
            last_name = last_name,
            phone = phone,
            email=email,
            password = password )

        if(not first_name):
            error_message = "first name required"
        elif len(first_name) < 4 :
            error_message = "First name must be greater than 4"
        
        elif customer.isExists():
            error_message = "Email Already Registered"

        #Saving 

        if not error_message:
            customer.password = make_password(customer.password)
            customer.save()
        else:
            data = {
                'error': error_message,
                'values': value,
            }
            return render(request, 'signup.html', data)

        return redirect('index')






class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer.get_customer_by_email(email)
        
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                # request.session['email'] = customer.email
                return redirect('index')
            else:
                error_message = "Email or Password Invalid"
        else:
            error_message = "Email or Password Invalid"
        print(customer)
        print(email, password)
        return render(request, 'login.html', {'error': error_message})



def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})







# def index(request):
    
#     products = None
#     categories = Category.get_all_categories()

#     categoryID = request.GET.get('category')
    
#     if categoryID:
#         products = Product.get_all_products_by_categoryid(categoryID)
        
#     else:
#         products = Product.get_all_products()

#     data  = {}


#     data['products'] = products
#     data['categories'] = categories 
#     print('you are: ', request.session.get('email'))

#     return render(request, 'index.html', data)

# def signup(request):

#     if request.method == "GET":
#         return render(request, 'signup.html')
    
#     else: 
#         postData = request.POST
#         first_name = postData.get('firstname')
#         last_name = postData.get('lastname')
#         phone = postData.get('number')
#         email = postData.get('email')
#         password = postData.get('password')

#         #validation 

#         value = {
#             'first_name' : first_name,
#             'last_name' : last_name,
#             'phone' : phone,
#             'email' : email
#         }

#         error_message = None

#         customer = Customer(first_name = first_name, 
#             last_name = last_name,
#             phone = phone,
#             email=email,
#             password = password )

#         if(not first_name):
#             error_message = "first name required"
#         elif len(first_name) < 4 :
#             error_message = "First name must be greater than 4"
        
#         elif customer.isExists():
#             error_message = "Email Already Registered"

#         #Saving 

#         if not error_message:
#             customer.password = make_password(customer.password)
#             customer.save()
#         else:
#             data = {
#                 'error': error_message,
#                 'values': value,
#             }
#             return render(request, 'signup.html', data)

#         return redirect('index')



# def login(request):
#     if request.method == "GET":
#         return render(request, 'login.html')

#     else:
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         customer = Customer.get_customer_by_email(email)
        
#         error_message = None
#         if customer:
#             flag = check_password(password, customer.password)
#             if flag:
#                 return redirect('index')
#             else:
#                 error_message = "Email or Password Invalid"

        
#         else:
#             error_message = "Email or Password Invalid"

#         print(customer)
#         print(email, password)
#         return render(request, 'login.html', {'error': error_message})


