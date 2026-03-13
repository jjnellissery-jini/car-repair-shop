from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import User,Services,Booking,Payment,Status
from django.contrib import messages

def index(request):
    if 'email' in request.session:
       current_user=request.session['email']
       print(current_user)
       return render(request,'index.html',{'cuser':current_user})
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def gallery(request):
    return render(request,'gallery.html')

def promo(request):
    return render(request,'promo.html')

def testimonials(request):
    return render(request,'testimonials.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
       

        try:
            
            user=User.objects.filter(email=email,password=password)
            if user is not None:
                
                request.session['email']=email
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request,'login.html') 

def register(request):
    
    if request.method=='POST':
        
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            User.objects.create(name=name,email=email,password=password)
            return redirect('login')
    return render(request,'register.html')

def logout(request):
    auth_logout(request) 
    return redirect('index') 

def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})
    



def booking(request):
    if  'email' not in request.session:
        return redirect('login')
    services = Services.objects.all()
    
    current_email = request.session['email']
    try:
        user = User.objects.get(email=current_email)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.method == 'POST':
        user1=user

        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        date = request.POST.get('date')
        concerns = request.POST.get('concerns')
        selected_service_ids = request.POST.getlist('services')

        if not all([user1, phone, email, date]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('booking')

        if Booking.objects.filter(email=email, date=date).exists():
            messages.error(request, 'You have already booked for this date.')
        else:
            booking = Booking.objects.create(
                user=user1,
                phone=phone,
                email=email,
                address=address,
                brand=brand,
                model=model,
                year=year,
                date=date,
                concerns=concerns
            )
            if selected_service_ids:
                services_qs = Services.objects.filter(id__in=selected_service_ids)
                booking.services.set(services_qs)
                for service in booking.services.all():
                    Status.objects.create(booking=booking, service=service)
            messages.success(request, "Slot booked successfully!")
            return redirect('payment')

    return render(request, 'booking.html', {'cuser':current_email,'services': services,'user':user})




def payment(request):
    if 'email' not in request.session:
        messages.error(request, "Please log in to proceed with payment.")
        return redirect('login')

    user_email = request.session['email']

    # Fetch the latest booking using email, NOT request.user
    booking = Booking.objects.filter(email=user_email).order_by('-id').first()
    if not booking:
        messages.error(request, "No booking found for this email.")
        return redirect('booking')

    services = booking.services.all()
    total_price = sum(service.price for service in services)

    if request.method == "POST":
        method = request.POST.get('method')
        if not method:
            messages.error(request, "Please select a payment method.")
        else:
            Payment.objects.create(
                booking=booking,
                amount=total_price,
                method=method,
                status="SUCCESS"
            )
            messages.success(request, "Payment successful!")
            return redirect('index') 

    return render(request, "payment.html", {
        'total_price': total_price,
        'booking': booking,
        'services': services,
    })

def servicestatus(request):
    if 'email' not in request.session:
        messages.error(request, "Please log in to view service status.")
        return redirect('login')

    # Get current logged-in user
    current_email = request.session['email']
    try:
        user = User.objects.get(email=current_email)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # If form is submitted (filtering by another user, maybe admin use?)
    if request.method == 'POST':
        user_id = request.POST.get('name')  # assuming this is user ID
        try:
            selected_user = User.objects.get(id=int(user_id))
            statuses = Status.objects.filter(booking__user=selected_user)
        except (User.DoesNotExist, ValueError):
            return HttpResponse("Invalid user", status=400)
    else:
        # Default: show statuses of current user
        statuses = Status.objects.filter(booking__user=user)

    return render(request, 'status.html', {'cuser':current_email,'statuses': statuses, 'user': user})
  