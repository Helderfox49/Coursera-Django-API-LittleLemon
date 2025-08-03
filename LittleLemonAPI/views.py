from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework import viewsets

from .throttles import TenCallsPerMinute

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']
    filterset_fields = ['category__title']  
    

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            choices = ordering.split(",")
            items = items.order_by(*choices)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except:
            items = []
        serializer_items = MenuItemSerializer(items, many=True)
        return Response(serializer_items.data)
    if request.method == 'POST':
        serializer_item = MenuItemSerializer(data=request.data)
        serializer_item.is_valid(raise_exception=True)
        serializer_item.save()
        return Response(serializer_item.data)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer_item = MenuItemSerializer(item)
    return Response(serializer_item.data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "only manager can see this"})
    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Succesful"})


@api_view()
@throttle_classes([TenCallsPerMinute])
@permission_classes([IsAuthenticated])
def throttle_check_auth(request):
    return Response({"message": "Message for the logged in users only"})

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer