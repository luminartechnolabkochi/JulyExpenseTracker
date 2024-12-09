
from django import forms

from expense.models import Transaction

from django.contrib.auth.models import User

# create ,update =>ModelForm

# 

class ExpenseCreateForm(forms.ModelForm):

    class Meta:

        model=Transaction

        exclude=("created_date","owner")

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),
            
            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),

            "category":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "priority":forms.Select(attrs={"class":"form-control form-select mb-2"})

        }        



class SignUpForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]


class LoginForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()


    