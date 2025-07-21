from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
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


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer