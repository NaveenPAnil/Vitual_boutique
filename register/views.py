from allauth.account.utils import send_email_confirmation
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib import messages
from .forms import CustomerRegisterForm, ProfileImageForm, VendorRegisterForm, RoleSelectionForm
from .models import User, Vendor
from vendor.models import Address, Order, Product
from .cmate import blend_images


def home(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def product_list(request):
    all_product = Product.objects.all()
    return render(request,'product_list.html',{'all_product':all_product})




def upload_images(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        profile_form = ProfileImageForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_image = profile_form.save()
            try:
                # Define directories where images are stored
                profile_image_path  = product.image.path
                product_image_path = profile_image.image.path
                profile_dir = 'media/profile_images/'
                source_dir = 'media/product/'
                dest_dir = 'result_images/'
                
                # Call blend_images function with path to the product image and the profile image
                result_filename, errors = blend_images(
                    product_image_path,
                    profile_image_path,
                    dest_dir,
                    source_dir,
                    profile_dir
                )
                response_data = {
                    'result_filename': '/' + result_filename.replace('\\', '/'),  # Ensure correct URL format
                    'errors': errors
                }
                return JsonResponse(response_data)
            except Exception as e:
                errors = str(e)
                return JsonResponse({'error': errors}, status=400)
    else:
        profile_form = ProfileImageForm()
    return render(request, 'upload_images.html', {'product': product, 'profile_form': profile_form})

class CustomSignupView(SignupView):
    def get_role(self):
        return self.request.session.get('role')

    def form_valid(self, form):
        role = self.get_role()
        user = form.save(self.request)
        user.role = role
        user.save()
        send_email_confirmation(self.request, user)
        messages.success(self.request, 'Registration successful. Please check your email for account activation instructions.')
        return redirect('login')

def register_choice_view(request):
    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            request.session['role'] = role
            if role == str(User.CUSTOMER):
                return redirect('customer_register')
            elif role == str(User.VENDOR):
                return redirect('vendor_register')
    else:
        form = RoleSelectionForm()
    return render(request, 'register_choice.html', {'form': form})

def customer_register_view(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.username = user.email
            user.save()
            send_email_confirmation(request, user)
            messages.success(request, 'Registration successful. Please check your email for account activation instructions.')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'customer_register.html', {'form': form})

def vendor_register_view(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.VENDOR
            user.username = user.email
            user.save()

            vendor = Vendor.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                vendor_license=form.cleaned_data['vendor_license']
            )

            send_email_confirmation(request, user)
            messages.success(request, 'Registration successful. Please check your email for account activation instructions.')
            return redirect('login')
    else:
        form = VendorRegisterForm()
    return render(request, 'vendor_register.html', {'form': form})

@login_required
def success_view(request):
    if request.user.role == User.CUSTOMER:
        return render(request, 'index.html')
    elif request.user.role == User.VENDOR:
        return render(request, 'vendor/vendor_dashboard.html')
    else:
        return render(request, 'default_success.html')



@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    address = Address.objects.filter(user=user, is_active=True).first()

    context = {
        'user': user,
        'orders': orders,
        'address': address
    }

    return render(request, 'index/user_profile.html', context)