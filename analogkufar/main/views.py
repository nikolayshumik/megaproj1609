from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import AdForm
from .models import Ad
from .models import Basket
from .models import BasketItem
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
from .forms import AdFilterForm

from django.views.generic import CreateView
from .models import Contact
from .forms import ContactForm
from .service import send
# from .tasks import write_file

from .models import Order
from .tasks import send_order_confirmation_email


from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm

def compose_message(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            form = MessageForm()
    else:
        form = MessageForm()

    messages = Message.objects.filter(
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient]
    ).order_by('created_at')

    return render(request, 'main/compose.html', {'form': form, 'messages': messages, 'recipient': recipient})

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'main/user_list.html', {'users': users})

def seller_profile(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    ads = Ad.objects.filter(user_id=user_id)

    filter_form = AdFilterForm(
        request.GET)  # Создайте экземпляр формы, используйте переданные GET-параметры для фильтрации (если есть)
    if filter_form.is_valid():
        title = filter_form.cleaned_data.get('title')
        # category = filter_form.cleaned_data.get('category')
        location = filter_form.cleaned_data.get('location')
        price_min = filter_form.cleaned_data.get('price_min')
        price_max = filter_form.cleaned_data.get('price_max')

        if title:
            ads = ads.filter(title__icontains=title)
        # if category:
        #     ads = ads.filter(category=category)
        if location:
            ads = ads.filter(location=location)
        if price_min is not None and price_max is not None:
            ads = ads.filter(price__range=(price_min, price_max))
        elif price_min is not None:
            ads = ads.filter(price__gte=price_min)
        elif price_max is not None:
            ads = ads.filter(price__lte=price_max)

    # Добавьте вызов метода order_by() для сортировки объявлений по возрастанию цены
    ads = ads.order_by('price')

    return render(request, 'main/seller_profile.html', {'profile': profile, 'ads': ads, 'filter_form': filter_form})
# def seller_profile(request, user_id):
#     profile = get_object_or_404(Profile, user_id=user_id)
#     ads = Ad.objects.filter(user_id=user_id) # Добавьте эту строку
#     return render(request, 'main/seller_profile.html', {'profile': profile, 'ads': ads}) # Дополните "ads": ads


# def seller_profile(request, seller_id):
#     seller = get_object_or_404(User, id=seller_id)  # Retrieve the seller's profile using their ID
#     profile = Profile.objects.get(user=seller)  # Retrieve the profile associated with the seller
#
#     return render(request, 'main/seller_profile.html', {'seller': seller, 'profile': profile})


def create_order(request):
    if request.method == 'POST':
        email = request.POST['email']
        order = Order.objects.create(email=email)
        send_order_confirmation_email.delay(email)
        return redirect('orders:confirmation')
    return render(request, 'main/create_order.html')


def order_confirmation(request):
    return render(request, 'main/order_confirmation.html')



class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'main/contact.html'

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        return super().form_valid(form)

def delete_from_basket(request):
    if request.method == 'POST':
        ad_ids = request.POST.getlist('ad_id')
        for ad_id in ad_ids:
            basket_items = BasketItem.objects.filter(ad_id=ad_id)
            basket_items.delete()
        return redirect('basket')
    return redirect('basket')


def details(request):
    ads = Ad.objects.all()
    ad_id = request.GET.get('ad_id')  # Получаем id объявления из параметра GET-запроса
    ad = None
    if ad_id:
        ad = Ad.objects.get(id=ad_id)  # Получаем объявление по id

    return render(request, 'main/details.html', {'ad': ad, 'ads': ads})
# def details(request):
#     ads = Ad.objects.all()
#     ad_id = request.GET.get('ad_id')  # Получаем id объявления из параметра GET-запроса
#     ad = None
#     if ad_id:
#         ad = Ad.objects.filter(id=ad_id).first()  # Получаем объявление по id
#
#     return render(request, 'main/details.html', {'ad': ad, 'ads': ads})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/registration.html', {'form': form})


def index(request):
    ads = Ad.objects.all()

    from_price = request.GET.get('from')
    to_price = request.GET.get('to')
    category = request.GET.get('category')
    location = request.GET.get('location')

    if from_price and to_price:
        ads = ads.filter(price__range=(from_price, to_price))
    elif from_price:
        ads = ads.filter(price__gte=from_price)
    elif to_price:
        ads = ads.filter(price__lte=to_price)

    if category:
        ads = ads.filter(category=category)

    if location:
        ads = ads.filter(location=location)

    ads = ads.order_by('price')

    context = {
        'ads': ads
    }
    return render(request, 'main/index.html', context)


def logout(request):
    return render(request, 'main/logout.html')

def test(request):
    return render(request, 'main/test.html')


@login_required
def basket(request):
    user_basket, created = Basket.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        quantity = int(request.POST.get('quantity', '1'))  # Default to 1 if quantity is not provided

        ad = Ad.objects.get(id=ad_id)

        basket_item, created = BasketItem.objects.update_or_create(basket=user_basket, ad=ad, defaults={'quantity': 0})
        basket_item.quantity += quantity
        basket_item.save()

        return redirect('home')
    else:
        basket_items = BasketItem.objects.filter(basket=user_basket)
        ads = Ad.objects.filter(basketitem__in=basket_items)

        total_quantity = 0
        total_price = 0

        for item in basket_items:
            total_quantity += item.quantity
            total_price += item.ad.price * item.quantity

        return render(request, 'main/basket.html', {'ads': ads, 'total_quantity': total_quantity, 'total_price': total_price})
@login_required
def postads(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, request=request)  # Pass the request object to the form
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace 'home' with the URL of your homepage
    else:
        form = AdForm(request=request)  # Pass the request object to the form
    return render(request, 'main/postads.html', {'form': form})
# def postads(request):
#
#     if request.method == 'POST':
#         form = AdForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Замените 'home' на URL вашей домашней страницы
#     else:
#         form = AdForm()
#     return render(request, 'main/postads.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile = user.profile

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'main/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def profiles(request):
    return render(request, 'main/profiles.html')


def myads(request):
    ads = Ad.objects.all()
    ad_id = request.GET.get('ad_id')
    equal_ad_id = int(ad_id) if ad_id else None
    return render(request, 'main/myads.html', {'ads': ads, 'equal_ad_id': equal_ad_id})

def ad_details(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    return render(request, 'main/myads.html', {'ads': Ad.objects.all(), 'equal_ad_id': ad_id})

def celery(request):
    return render(request, 'main/hometusk.html')

def edit_ad(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('myads')
    else:
        form = AdForm(instance=ad)
    return render(request, 'main/edit_ad.html', {'form': form, 'ad': ad})


def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if request.method == 'POST':
        ad.delete()
        return redirect('myads')

    return HttpResponseNotAllowed(['POST'])


def buy(request):
    return render(request, 'main/buy.html')

