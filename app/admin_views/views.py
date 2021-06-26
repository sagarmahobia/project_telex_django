# Create your views here.

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from app.models import Entity, Category
from app.my_serializers import EntitySerializer
from my_user.my_authentication import JwtAuthentication
from my_user.user_permissions import IsAdmin


@api_view(['PUT', ])
@permission_classes([IsAdmin])
@authentication_classes([JwtAuthentication])
def add_category(request):
    try:

        friendly_name = request.POST.get("name")
        icon = request.POST.get("icon_id")

        name = friendly_name.replace(" ", "_").lower()

        Category.objects.create(name=name,
                                friendly_name=friendly_name,
                                app_icon_id=icon)

        return JsonResponse(data={"status": 1, "message": "Added"})

    except IntegrityError:
        return Response(data={"status": 0, "message": "Already Exists"})


@api_view(['POST', ])
@permission_classes([IsAdmin])
@authentication_classes([JwtAuthentication])
def edit_category(request, category_id):
    try:

        friendly_name = request.POST.get("name")
        icon = request.POST.get("icon_id")

        category = Category.objects.get(id=category_id)
        category.friendly_name = friendly_name
        category.app_icon_id = icon
        category.save()

        return JsonResponse(data={"status": 1, "message": "Successfully Updated"})

    except Category.DoesNotExist:
        return Response(data={"status": 0, "message": "Does Not Exists"})


@api_view(['DELETE', ])
@permission_classes([IsAdmin])
@authentication_classes([JwtAuthentication])
def delete_category(request, category_id):
    try:

        Category.objects.get(id=category_id).delete()

        return Response(data={"status": 1, "message": "Deleted"})

    except Category.DoesNotExist:
        return Response(data={"status": 0, "message": "Does Not Exists"})


@api_view(['PUT', ])
@permission_classes([IsAdmin])
def add_entity(request):
    entity_id = request.POST.get('entity_id')
    entity_type = request.POST.get('entity_type')
    category_id = request.POST.get('category_id')
    category = Category.objects.get(id=category_id)
    Entity.objects.create(entity_id=entity_id,
                          entity_type=entity_type,
                          category=category)

    return Response(data={"status": 1, "message": "Success"})


@api_view(['POST', ])
@permission_classes([IsAdmin])
def edit_entity(request, entity_id):

    category_id = request.POST.get('category_id')
    category = Category.objects.get(id=category_id)
    entity = Entity.objects.get(id=entity_id)

    entity.category = category
    entity.save()
    return Response(data={"status": 1, "message": "Success"})


@api_view(['DELETE', ])
@permission_classes([IsAdmin])
def delete_entity(request, entity_id):

    Entity.objects.get(id=entity_id).delete()

    return Response(data={"status": 1, "message": "Success"})


@api_view(['POST', ])
@permission_classes([IsAdmin])
def add_bulk_entity(request):
    ids = request.POST.get("ids")
    category_id = request.POST.get("category_id")
    entity_type = request.POST.get("entity_type")

    id_list = ids.replace(" ", "").split(",")

    category = Category.objects.get(id=category_id)
    for eid in id_list:
        Entity.objects.create(entity_id=eid, category=category, entity_type=entity_type)

    return Response(data={"status": 1, "message": "Success"})


def get_entities(entity_type):
    return Entity.objects.filter(entity_type=entity_type)


@api_view(['GET', ])
@permission_classes([IsAdmin])
def get_channels(request):
    entities = EntitySerializer(get_entities("channels"), many=True).data
    return Response(data=entities)


@api_view(['GET', ])
@permission_classes([IsAdmin])
def get_bots(request):
    entities = EntitySerializer(get_entities("bots"), many=True).data
    return Response(data=entities)


@api_view(['GET', ])
@permission_classes([IsAdmin])
def get_groups(request):
    entities = EntitySerializer(get_entities("groups"), many=True)

    return Response(data=entities.data)
