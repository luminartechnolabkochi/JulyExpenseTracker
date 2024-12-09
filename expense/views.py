
from django.views.generic import View

from expense.forms import ExpenseCreateForm,SignUpForm,LoginForm
from expense.models import Transaction

from django.shortcuts import render,redirect

from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from expense.decorators import signin_required

from django.utils.decorators import method_decorator

from django.contrib import messages
# messageframework


@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    template_name="expense_add.html"

    form_class=ExpenseCreateForm

    def get(self,request,*args,**kwargs):

        # step1 create form_instance

       
       

        form=self.form_class()

        return render(request,self.template_name,{"form":form})
    

    def post(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

            return redirect("signin")

        # step1 initialize form with request.POST

        form_instance=self.form_class(request.POST)

        # chk form has no errors

        if form_instance.is_valid():

            # data=form_instance.cleaned_data #{}

            # Transaction.objects.create(**data)
            
            form_instance.instance.owner=request.user

            form_instance.save()

            messages.success(request,"Expense has been added")


        return redirect("listexpense")

# render(request,template_name,context)
# redirect("view_name")
# path(route,view,name)


# url> localhost:8000/expense/all/
# method:GET

# render(request,template_name,context)
# redirect(name in)

# model relations (ONetoone,ForiegnKey)
# 

@method_decorator(signin_required,name="dispatch")
class ExpenseListView(View):

    template_name="expense_list.html"

    def get(self,request,*args,**kwargs): 

    

        selected_category=request.GET.get("category","all") #Bills

        if selected_category == "all":

            qs=Transaction.objects.filter(owner=request.user)
        else:
            qs=Transaction.objects.filter(category=selected_category,owner=request.user)#bills

         

        categories=Transaction.objects.all().values_list("category",flat=True).distinct()

        print(categories)

        return render(request,self.template_name,{"data":qs,"categories":categories,"selected_category":selected_category})



@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    template_name="expense_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")#3

        qs=Transaction.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

        
# localhost:8000/expense/3/remove

@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Transaction.objects.get(id=id).delete()

        messages.success(request,"expense has been  removed ")
        return redirect("listexpense")




# url:localhost:8000/expense/<int:pk>/change/

# method:GET,POST

@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

    template_name="expense_update.html"

    form_class=ExpenseCreateForm


    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transaction.objects.get(id=id)

        # instance_dictionary={
        #     "title":instance.title,
        #     "amount":instance.amount,
        #     "category":instance.category,
        #     "payment_method":instance.payment_method,
        #     "priority":instance.priority
        # }                 

        form_instance=self.form_class(instance=trans_obj)
       

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        transaction_object=Transaction.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=transaction_object)

        if form_instance.is_valid():

            form_instance.save()#update 

            messages.success(request,"expense has been cahnged ")

            return redirect("listexpense")
        
        messages.error(request,"failed to change expense")
        return render(request,self.template_name,{"form":form_instance})




@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):


    template_name="expense_summary.html"

    def get(self,request,*args,**kwargs):

        expense_total=Transaction.objects.all().aggregate(total=Sum("amount"))#{"total":4567}

        category_summary=Transaction.objects.all().values("category").annotate(total=Sum("amount"))

        payment_summary=Transaction.objects.all().values("payment_method").annotate(total=Sum("amount"))

        priority_summary=Transaction.objects.all().values("priority").annotate(total=Sum("amount"))

        

        context={
            "total_expense":expense_total.get("total"),

            "category_summary":category_summary,

            "payment_summary":payment_summary,

            "priority_summary":priority_summary

        }

        return render(request,self.template_name,context)




class SignUpView(View):

    template_name="register.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()#username,email,password

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("signup")
        return render(request,self.template_name,{"form":form_instance})

        

class SignInView(View):

    template_name="login.html"

    form_class=LoginForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
   
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                print(request.user)

                return redirect("expensesummary")
            
        return render(request,self.template_name,{"form":form_instance})
            

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
                








    

       










    


