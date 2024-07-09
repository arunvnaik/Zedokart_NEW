from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from appff.models import Registration_Data
import uuid
from django.http import JsonResponse

def registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        password = request.POST.get('pswd')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        referral = request.POST.get('referral')

        if Registration_Data.objects.filter(email=email).exists():
            error_message = 'Email is already registered.'
            return render(request, 'index.html', {'error_message': error_message})
        
        if Registration_Data.objects.filter(mobile_number=mobile_number).exists():
            error_message = 'Mobile number is already registered.'
            return render(request, 'index.html', {'error_message': error_message})
        
        if referral and Registration_Data.objects.filter(referral=referral).count() >= 2:
            error_message = 'Referral ID has already been used twice. Please use another referral ID.'
            return render(request, 'index.html', {'error_message': error_message})

        user_id = f'ZK{str(uuid.uuid4().int)[:4]}'  

        registration_data = Registration_Data.objects.create(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            referral=referral,
            user_id=user_id,
            password=password  
        )

        if referral:
            registration_data.referral = referral
            registration_data.save()

        send_mail(
            'Welcome to Our Website',
            f'Your user ID is: {user_id}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect('index')

    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        next_page = request.POST.get('next', 'index')  

        registration_data = Registration_Data.objects.filter(user_id=user_id).first()

        if registration_data and password == registration_data.password: 
            request.session['logged_in'] = True
            request.session['user_id'] = user_id
            return redirect(next_page)
        else:
            error_message = 'Invalid Credentials.'
            return render(request, 'index.html', {'error_message': error_message})
        
def index(request):
    if request.method == 'POST' and request.session.get('logged_in', False):
        return JsonResponse({'message': 'Login successful!'})
    
    logged_in = request.session.get('logged_in', False)
    user_id = request.session.get('user_id', None)
    
    # Fetch full name based on the user_id
    full_name = None
    if logged_in and user_id:
        registration_data = Registration_Data.objects.filter(user_id=user_id).first()
        if registration_data:
            full_name = registration_data.full_name
    
    return render(request, 'index.html', {'logged_in': logged_in, 'user_id': user_id, 'full_name': full_name})


def shop(request):
    logged_in = request.session.get('logged_in', False)
    user_id = request.session.get('user_id', None)

    # Fetch full name based on the user_id
    full_name = None
    if logged_in and user_id:
        registration_data = Registration_Data.objects.filter(user_id=user_id).first()
        if registration_data:
            full_name = registration_data.full_name
    return render(request, "shop.html", {'logged_in': logged_in, 'user_id': user_id, 'full_name': full_name})

def get_referral_tree_data(user):
    def build_tree(user):
        children = Registration_Data.objects.filter(referral=user.user_id)
        return [{'user_id': child.user_id, 'children': build_tree(child)} for child in children]

    return {'user_id': user.user_id, 'children': build_tree(user)}

def tree(request):
    first_registered_user = Registration_Data.objects.first()
    referral_tree_data = get_referral_tree_data(first_registered_user)

    logged_in = request.session.get('logged_in', False)
    user_id = request.session.get('user_id', None)
    
    # Fetch full name based on the user_id
    full_name = None
    if logged_in and user_id:
        registration_data = Registration_Data.objects.filter(user_id=user_id).first()
        if registration_data:
            full_name = registration_data.full_name

    return render(request, 'tree.html', {'referral_tree_data': referral_tree_data, 'logged_in': logged_in, 'user_id': user_id, 'full_name': full_name})

def logout(request):
    # Clear session variables
    request.session.clear()
    # Redirect to the index page after logout
    return redirect('index')

def aboutus(request):
    logged_in = request.session.get('logged_in', False)
    user_id = request.session.get('user_id', None)

    # Fetch full name based on the user_id
    full_name = None
    if logged_in and user_id:
        registration_data = Registration_Data.objects.filter(user_id=user_id).first()
        if registration_data:
            full_name = registration_data.full_name
    return render(request, "aboutus.html", {'logged_in': logged_in, 'user_id': user_id, 'full_name': full_name})

def contactus(request):
    logged_in = request.session.get('logged_in', False)
    user_id = request.session.get('user_id', None)

    # Fetch full name based on the user_id
    full_name = None
    if logged_in and user_id:
        registration_data = Registration_Data.objects.filter(user_id=user_id).first()
        if registration_data:
            full_name = registration_data.full_name
    return render(request, "contactus.html", {'logged_in': logged_in, 'user_id': user_id, 'full_name': full_name})
