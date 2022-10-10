"""AuctionBits URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('banned/', views.BannedView.as_view(), name='banned'),
    path('stop/', views.StopView.as_view(), name='stop'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('view-products/', views.ViewProducts.as_view(), name='view-prods'),
    path('2fa/', views.TwoFA.as_view(), name='2fa'),
    path('add-products/', views.AddProduct.as_view(), name='add-prods'),
    path('bid/<int:pk>', views.NewBid.as_view(), name='bid'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('approval-page/', views.AdminApproval.as_view(), name='approval-page'),
    path('approve/<int:pk>', views.ApproveOrDeny.as_view(), name='approve'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)