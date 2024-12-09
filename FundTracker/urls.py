"""
URL configuration for FundTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from expense import views
# def path(route,view,name)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("expense/add/",views.ExpenseCreateView.as_view(),name="addexpense"),

    path("expense/all/",views.ExpenseListView.as_view(),name="listexpense"),

    path("expense/<int:pk>/",views.ExpenseDetailView.as_view(),name="detailexpense"),

    path("expense/<int:pk>/remove/",views.ExpenseDeleteView.as_view(),name="deleteexpense"),

    path("expense/<int:pk>/change/",views.ExpenseUpdateView.as_view(),name="editexpense"),

    path("expense/summary/",views.ExpenseSummaryView.as_view(),name="expensesummary"),

    path("register/",views.SignUpView.as_view(),name="signup"),

    path("",views.SignInView.as_view(),name="signin"),

    path("signout/",views.SignOutView.as_view(),name="signout")





   
]
