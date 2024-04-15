from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from .models import User,Restaurant,DeliveryPartner
from .serializers import UserSerializer,restaurantSerializer





@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        # 'avatar': request.user.get_avatar()
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    print(data)
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        'user_type': data.get('user_type')
    })

    if form.is_valid():
        user = form.save()
        user.is_active = True
        form.save()
        
        print("signup validated in api")


    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message})


@api_view(['GET'])
def show_restaurant_via_location(request,location):
    restaurants=Restaurant.objects.all().filter(city=location)
    serializer=restaurantSerializer(restaurants,many=True)
    return JsonResponse({'data':serializer.data})

@api_view(['GET'])
def restaurant_via_loc_and_rating(request,location,rating):
    restaurants=Restaurant.objects.all().filter(Q(address=location) | Q(rating>3))
    serializer=restaurantSerializer(restaurants,many=True)
    return JsonResponse({'data':serializer.data})

