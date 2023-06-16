from django.shortcuts import render ,HttpResponse,redirect
from django.utils import timezone
from .models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Ordeer, User


# Create your views here.



def HomePage(request):
    orders=Ordeer.objects.all()
    user = request.user

    is_supplier = user.is_authenticated and user.is_supplier
    is_customer = user.is_authenticated and user.is_customer
    is_manager = user.is_authenticated and user.is_manager
    
    is_supplier=bool(is_supplier)
    is_customer=bool(is_customer)
    is_manager=bool(is_manager)


    if is_manager:
       return render(request,"admin.html",{'orders':orders})
    if is_supplier:
        return render(request,"supplier.html",{'orders':orders})

    if is_customer:
        return render(request,"customer.html",{'orders':orders})
        
    return render(request,"home.html",{'orders':orders})



def SupplierPage(request):   
    user = request.user
    is_supplier = user.is_authenticated and user.is_supplier
    is_supplier=bool(is_supplier)
    print("is_supplier")
    print(is_supplier)
    if is_supplier:
        
        last_order = Ordeer.objects.order_by('-id').first()
        if request.method == 'POST':
            orders=Ordeer.objects.all()    
            available_qty = request.POST.get('available')
            last_order.available_Qty = available_qty
            last_order.save()

            # redirect to a success page or render a success message
            return render(request,"supplier.html",{'orders':orders})
        else:    
        
            orders=Ordeer.objects.all()    
            return render(request,"supplier.html",{'orders':orders})
    else:
        messages.error(request, 'this option onlly for supplier ')

        orders=Ordeer.objects.all()
        return redirect(HomePage)




def customer_page(request):
    last_order = Ordeer.objects.order_by('-id').first()

    if request.method == 'POST':
        orders=Ordeer.objects.all()    
        Requested_qty = request.POST.get('Requested')
        delivery_date = request.POST.get('time_date')
        
        
        last_order.Requested_Qty = Requested_qty
        last_order.date_delivery = delivery_date
        last_order.status="underprocessing"
        last_order.save()
        
        return render(request,"customer.html",{'orders':orders})    
    else:
        orders=Ordeer.objects.all()    
        return render(request,"customer.html",{'orders':orders})



def Manger_page(request):
    orders=Ordeer.objects.all()    
    return render(request,"admin.html",{'orders':orders})





def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            # Return an error message or form with errors
            messages.error(request, 'check password and your email' )

            return render(request, 'login.html')

    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect("Home")


def singup(request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            full_name = request.POST.get('full_name', '')
            sectors = request.POST.get('sectors')
            
            print("singup called")
            print(sectors)            
            
            if sectors == "customer":
                print("eniter here is")
                is_supplier=False
                is_customer=True
                is_manager=False
                group_name = 'Customer Group'
                
                
            if sectors == "supplier":
                is_supplier=True
                is_customer=False
                is_manager=False    
                group_name = 'Supplier Group'
                
                            

            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                is_supplier=is_supplier,
                is_customer=is_customer,
                is_manager=is_manager,
                date_joined=timezone.now(),
            )
            
            
            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                
            login(request, user)
            return redirect('Home')
        else:
            return render(request, 'singup.html')



def actual_date(request):
    if request.method == "POST":
        last_order = Ordeer.objects.order_by('-id').first()
        actual_date = request.POST['Actual_date']        
        last_order.date_delivery = actual_date
        last_order.status="Completed"
        last_order.save()
        return redirect('Manger_page')

        
