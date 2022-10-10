from math import prod
from urllib.request import Request
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
import smtplib, ssl
import re
from datetime import datetime
from django.utils import timezone
from .utils import check_ip
from django.contrib.auth import logout
import pytz

class IndexView(TemplateView):
    template_name = "index.html"
class BannedView(TemplateView):
    template_name = "banned.html"
class StopView(TemplateView):
    template_name = "stop.html"


class SignUpView(CreateView):
    template_name = "signup.html"
    model = User

    def password_check(self, password):
            """
            Verify the strength of 'password'
            Returns a dict indicating the wrong criteria
            A password is considered strong if:
                8 characters length or more
                1 digit or more
                1 symbol or more
                1 uppercase letter or more
                1 lowercase letter or more
            """

            # calculating the length
            length_error = len(password) < 8

            # searching for digits
            digit_error = re.search(r"\d", password) is None

            # searching for uppercase
            uppercase_error = re.search(r"[A-Z]", password) is None

            # searching for lowercase
            lowercase_error = re.search(r"[a-z]", password) is None

            # searching for symbols
            symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

            # overall result
            password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

            return password_ok


    def post(self, request, *args, **kwargs):

        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        val = dict(request.POST)
        val_dict = {key: value[0] for key, value in val.items()}
        print(val_dict)
        del val_dict['csrfmiddlewaretoken']
        del val_dict['signup']

        isPassStrong = self.password_check(val_dict['password'])
        if not isPassStrong:
            return render(request, template_name=self.template_name, context={"passweak" : True})

        hashed_pass = make_password(val_dict['password'])
        val_dict['password'] = hashed_pass
        self.model.objects.create(**val_dict)
        

        return HttpResponseRedirect(reverse('login'))

    def get(self, request, *args, **kwargs):

        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        return render(request, template_name=self.template_name, context={"passweak" : False})


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/view-products'

class UserLogoutView(LogoutView):
    template_name = 'login.html'



@method_decorator(login_required, name='dispatch')
class ViewProducts(View):
    template_name = "view_products.html"
    def get(self, request, *args, **kwargs):
        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        products = Product.objects.filter(approved=True)
        product_context_data = []
        for product in products:
            bids = Bid.objects.filter(bid_product=product)
            max_bid = Bid(bid_price=0)
            if len(bids) > 0:
                max_bid = bids.order_by('bid_price')[0]

            print(product.event_dt)
            print(timezone.localtime())
            print(product.event_dt < timezone.localtime())
            
            product_context_data.append({
                'product' : product,
                'max_bid' : max_bid,
                'expired' : product.event_dt<timezone.localtime()
            })

        context_data = {
            'products' : product_context_data
        }

        return render(request, template_name=self.template_name, context=context_data)


class TwoFA(View):
    template_name = "2fa.html"

    def post(self, request, *args, **kwargs):
        val = dict(request.POST)
        val_dict = {key: value[0] for key, value in val.items()}
        print(val_dict)
        del val_dict['csrfmiddlewaretoken']

        code = val_dict['2facode']


    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


@method_decorator(login_required, name='dispatch')
class AddProduct(CreateView):
    template_name = "add_prod.html"
    model = Product

    def post(self, request, *args, **kwargs):
        val = dict(request.POST)
        val_dict = {key: value[0] for key, value in val.items()}
        print(val_dict)
        del val_dict['csrfmiddlewaretoken']
        del val_dict['submit']

        val_dict['image'] = request.FILES['image']
        val_dict['owned_by'] = User.objects.get(id=request.user.id)

        val_dict['event_dt']=timezone.make_aware(datetime.strptime(val_dict['event_dt'], '%Y-%m-%dT%H:%M'))


        self.model.objects.create(**val_dict)
        return HttpResponseRedirect(reverse('view-prods'))

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


@method_decorator(login_required, name='dispatch')
class NewBid(CreateView):
    template_name = "bid.html"
    model = Bid

    def post(self, request, *args, **kwargs):

        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        val = dict(request.POST)
        val_dict = {key: value[0] for key, value in val.items()}
        print(val_dict)
        del val_dict['csrfmiddlewaretoken']
        new_bid = int(val_dict['bidp'])

        pk = kwargs["pk"]
        product = Product.objects.get(id=pk)

        bids = Bid.objects.filter(bid_product=product)

        max_bid = Bid(bid_price=0)
        if len(bids) > 0:
            max_bid = bids.order_by('bid_price')[0]
        
        b: Bid
        bid_by = User.objects.get(id=request.user.id)
        if max_bid.bid_price < new_bid and product.price < new_bid:
            b = Bid.objects.create(bid_price=new_bid, bid_by=bid_by, bid_product=product)
        else:
            b = max_bid


        return render(request, template_name=self.template_name, context={'product' : product, 'max_bid' : b, 'expired' : product.event_dt<timezone.localtime()})
        


    def get(self, request, *args, **kwargs):

        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        pk = kwargs["pk"]
        product = Product.objects.get(id=pk)

        bids = Bid.objects.filter(bid_product=product)
        max_bid = Bid(bid_price=0)

        if len(bids) > 0:
            max_bid = bids.order_by('bid_price')[0]

        return render(request, template_name=self.template_name, context={'product' : product, 'max_bid' : max_bid, 'expired' : product.event_dt<timezone.localtime() })

@method_decorator(login_required, name='dispatch')
class AdminApproval(View):
    template_name = "admin-approval.html"
    def get(self, request, *args, **kwargs):
        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))

        user = User.objects.get(id=request.user.id)
        if not user.isAdmin:
            return HttpResponseRedirect(reverse('stop'))

        products = Product.objects.filter(approved=False, banned=False)
        return render(request, template_name=self.template_name, context={'products': products})

    

class ApproveOrDeny(View):
    def post(self, request, *args, **kwargs):
        isBanned = check_ip(request)
        if isBanned:
            logout(request)
            return HttpResponseRedirect(reverse('banned'))
        
        val = dict(request.POST)
        val_dict = {key: value[0] for key, value in val.items()}

        product = Product.objects.get(id=kwargs['pk'])

        if val_dict.get('deny') is None:
            product.approved = True
            product.save()
        else:
            product.banned = True
            product.save()
        return HttpResponseRedirect(reverse('approval-page'))
