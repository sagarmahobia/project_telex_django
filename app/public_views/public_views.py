import rest_framework.generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.models import Category, Entity, Icon
from app.my_serializers import CategorySerializer, EntitySerializer, IconSerializer
from my_user.jwt_user import JwtUser
from my_user.models import User
from my_user.my_authentication import NoAuthentication


@api_view(["POST"])
@authentication_classes([NoAuthentication])
@permission_classes([AllowAny])
def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        print(e)
        return Response(
            {
                "status": 0,
                "message": "Incorrect Email or Password"
            }
        )

    if user.check_password(password):
        user = user
        jwt_user = JwtUser()
        jwt_user.id = user.id
        jwt_user.role = user.role
        jwt_user.user_name = user.email

        return Response(
            {
                "token": jwt_user.to_token(),
                "status": 1,
                "message": "Success"
            }
        )
    else:
        return Response(
            {
                "status": 0,
                "message": "Incorrect Email or Password"
            }
        )


#
#
#
#
#
#


@api_view(['GET'])
@authentication_classes([NoAuthentication])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.order_by('name')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def get_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        serialized = CategorySerializer(category)
        return Response(data=serialized.data)

    except Category.DoesNotExist:
        return Response(data={"status": 0, "message": "Does Not Exists"})


#
#
#


@api_view(["GET", ])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def filter_entity(request):
    category = request.GET.get("category_id")
    entity_type = request.GET.get("type")

    entities = Entity.objects.filter(category_id=category, entity_type=entity_type)

    data = EntitySerializer(entities, many=True).data
    return Response(data=data)


class FilterAPIView(rest_framework.generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [NoAuthentication]

    serializer_class = EntitySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        category_id = self.request.GET.get("category_id")
        entity_type = self.request.GET.get("type")
        entities = Entity.objects.filter(category_id=category_id, entity_type=entity_type)
        return entities


@api_view(["GET", ])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def get_entity(request, entity_id):
    entities = Entity.objects.get(id=entity_id)

    data = EntitySerializer(entities).data
    return Response(data=data)


@api_view(["GET", ])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def for_you(request, entity_type):
    category_objects = []

    categories = Category.objects.all().order_by('name')
    for category in categories:
        entities = Entity.objects.filter(category=category,
                                         entity_type=entity_type,
                                         fetched=True).order_by('title')[:10]

        entities = EntitySerializer(entities, many=True).data

        category_object = {
            'category': category.friendly_name,
            'entities': entities
        }
        if len(entities) > 0:
            category_objects.append(category_object)

    return Response(data=category_objects)


@api_view(["GET", ])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def top_100(request, entity_type):
    entities = Entity.objects.filter(
        entity_type=entity_type,
        fetched=True).order_by('-subscribers')[:100]

    entities = EntitySerializer(entities, many=True).data

    return Response(data=entities)


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([NoAuthentication])
def get_icons(request):
    icons = Icon.objects.all()
    iconsData = IconSerializer(icons, many=True)
    return Response(data=iconsData.data)
