from django.shortcuts import render,HttpResponse,redirect
from .models import Product,CartItem,Order
from .forms import CreateUserForm,AddProduct
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
import random
import razorpay
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def index(req):
    products = Product.objects.all()
    context = {}
    context['products']=products
    return render(req,"index.html",context)

def productDetail(req,pid):
    products = Product.objects.get(product_id=pid)
    context = {}
    context['products']=products
    return render(req,"productDetail.html",context)

def viewCart(req):
    if req.user.is_authenticated:
       cart_item = CartItem.objects.filter(user = req.user)
    else:
        cart_item = CartItem.objects.filter(user = None)
        messages.warning(req,"Login to add to cart")
    context = {}
    context['items'] = cart_item
    total_price = 0
    for x in cart_item:
        #print(x.product.price,x.quantity)
        total_price += (x.product.price * x.quantity)
        #print(total_price)
    context['total'] = total_price
    length = len(cart_item)
    context["length"] = length
    return render(req,"cart.html",context)

def addCart(req,pid):
    products = Product.objects.get(product_id = pid)
    user = req.user if req.user.is_authenticated else None
    if user:
        cart_items,created = CartItem.objects.get_or_create(product = products, user = user)
    else:
        return redirect("/login")
    print(cart_items,created) 
    if not created:
        cart_items.quantity += 1
    else:
        cart_items.quantity = 1
    cart_items.save()
    return redirect("/viewCart")

def remove(req,pid):
    products = Product.objects.get(product_id = pid)
    cart_items = CartItem.objects.filter(product = products, user = req.user)
    cart_items.delete()
    return redirect("/viewCart") 

def search(req):
    search = req.GET['search']
    products=Product.objects.filter(product_name__icontains=search)
    context={'products':products}
    return render(req,"search.html",context)

def range(req):
    if req.method == "GET":
        return redirect("/")
    else:
        min = req.POST["min"]
        max = req.POST["max"]
        if min !="" and max !="" and min is not None and max is not None:
            queryset = Product.prod.get_price_range(min,max) #Using Custom Manager
            #queryset = Product.objects.filter(price__range = (min,max))
            context = {}
            context['products'] = queryset
            return render(req,"index.html",context)
        else:
            return redirect("/")
    
def watchlist(req):
    if req.method == "GET":
        queryset = Product.prod.watchlist() #Using Custom Manager
        #queryset = Product.objects.filter(price__range = (min,max))
        context = {}
        context['products'] = queryset
        return render(req,"index.html",context)
    
def mobilelist(req):
    if req.method == "GET":
        queryset = Product.prod.mobilelist() #Using Custom Manager
        #queryset = Product.objects.filter(price__range = (min,max))
        context = {}
        context['products'] = queryset
        return render(req,"index.html",context)
    
def laptoplist(req):
    if req.method == "GET":
        queryset = Product.prod.laptoplist() #Using Custom Manager
        #queryset = Product.objects.filter(price__range = (min,max))
        context = {}
        context['products'] = queryset
        return render(req,"index.html",context)
    
def priceOrder(req):
    queryset = Product.objects.all().order_by('price')
    context = {}
    context['products'] = queryset
    return render(req,"index.html",context)

def descpriceOrder(req):
    queryset = Product.objects.all().order_by('-price')
    context = {}
    context['products'] = queryset
    return render(req,"index.html",context)

def updateqty(req,uval,pid):
    products = Product.objects.get(product_id = pid)
    a = CartItem.objects.filter(product = products)
    print(a)
    print(a[0])
    print(a[0].quantity)
    if uval == 1:
        temp = a[0].quantity + 1
        a.update(quantity = temp)
    else:
        temp = a[0].quantity - 1
        a.update(quantity = temp)
    return redirect("viewCart") 

def viewOrder(req):
    cart_item = CartItem.objects.filter(user = req.user)
    print(cart_item)
    oid = random.randrange(1000,9999)
    """ for x in cart_item:
        Order.objects.create(order_id = oid, product_id = x.product.product_id,quantity = x.quantity,user = req.user)
        x.delete() 
    orders = Order.objects.filter(user=req.user,is_completed = False) """
    context = {}
    context['items'] = cart_item
    total_price = 0
    for x in cart_item:
        #print(x.product.price,x.quantity)
        total_price += (x.product.price * x.quantity)
        #print(total_price)
    context['total'] = total_price
    length = len(cart_item)
    context["length"] = length
    return render(req,"viewOrder.html",context)

def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,"User Created Successfully")
            return redirect("/")
        else:
            messages.error(req,"Incorrect Username or Password Format")
    context = {'form':form}
    return render(req,"register.html",context)

def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,("Logged in Successfully"))
            return redirect("/")
        else:
            messages.error(req,("There was an error. Try Again!!!"))
            return redirect("/login")
    else:
        return render(req,"login.html")

def logout_user(req):
    logout(req)
    messages.success(req,("Logged Out Successfully"))
    return redirect("/") 

def makePayment(req):
    uemail = req.user.email
    print(uemail)
    c = CartItem.objects.filter(user = req.user)
    oid = random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id = oid, product_id = x.product.product_id,quantity = x.quantity,user = req.user)
        x.delete() 
    orders = Order.objects.filter(user = req.user,is_completed = False)
    total_price = 0
    for x in orders:
        total_price += (x.product.price * x.quantity)
        oid = x.order_id
    print(total_price)
    orderdetails = Order.objects.filter(user = req.user,is_completed = False)
    order_details = [
        {'product_name':order.product.product_name,'quantity':order.quantity,'price':order.product.price}
        for order in  orderdetails
    ]
    client = razorpay.Client(auth=("rzp_test_gN9cugzg8G8MAf", "O8AcpBUuJ3VX7sCGRKlQ0hNi"))
    data ={"amount": total_price * 100,
           "currency": "INR",
           "receipt": "oid",}
    payment = client.order.create(data = data)
    context = {}
    context['data'] = payment
    context['amount'] = payment["amount"]
    
    c.delete()
    orders.update(is_completed = True)
    sendUserMail(req,orderdetails,req.user.email,total_price)
    return render(req,"payment.html",context) 

def MyOrders(req):
    orders = Order.objects.filter(user=req.user)
    context = {}
    context['items'] = orders
    return render(req,"MyOrders.html",context)

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)

def insertProduct(req):
    if req.user.is_authenticated:
        user = req.user
        if req.method == "GET":
            form = AddProduct()
            return render(req,"insertProd.html",{'form':form,'username':user})
        else:
            form = AddProduct(req.POST,req.FILES or None)
            if form.is_valid():
                form.save()
                return redirect("/")
            else:
                return render(req,"insertProd.html",{'form':form,'username':user})
    else:
        return redirect("/login") 

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
def sendUserMail(req,od,recipient_email,tp):
    email_body = render_to_string("order_placed.html",
    {"order_details": od, "total_price":tp})
    """ send_mail(
        "order placed successfully",
        "Order Details are: ",
        "nehagaikwad367@gmail.com",
        ["to@example.com"],
        fail_silently=False,
    ) """
    message = EmailMultiAlternatives(
        subject = "Order placed successfully",
        body = email_body,
        from_email = None,
        to= [recipient_email]
    )
    message.attach_alternative(email_body, "text/html")
    message.send()
    return HttpResponse("Mail sent successfully")
   
   
   
   
    # Django:- xebb wqxe qtlt ulml