"""
URL configuration for EcommProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="index"),
    path("productDetail/<int:pid>",views.productDetail,name="productDetails"),
    path("viewCart/",views.viewCart,name="viewCart"),
    path("addCart/<int:pid>",views.addCart,name="addCart"),
    path("remove/<int:pid>",views.remove,name="remove"),
    path("search/",views.search,name="search"),
    path("range",views.range,name="range"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("mobilelist",views.mobilelist,name="mobilelist"),
    path("laptoplist",views.laptoplist,name="laptoplist"),
    path("priceOrder",views.priceOrder,name="priceOrder"),
    path("descpriceOrder",views.descpriceOrder,name="descpriceOrder"),
    path("updateqty/<int:uval>/<int:pid>/",views.updateqty,name="updateqty"),
    path("viewOrder/",views.viewOrder,name="viewOrder"),
    path("register_user/",views.register_user,name="register_user"),
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("payment/",views.makePayment,name="payment"),
    path("myorders/",views.MyOrders,name="myorders"),
    path("insertProduct/",views.insertProduct,name="insertProduct"),
    path("sendmail/",views.sendUserMail,name="sendmail"),
]
