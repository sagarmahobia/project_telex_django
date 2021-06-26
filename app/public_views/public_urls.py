from django.urls import path

from app.public_views import public_views

urlpatterns = [

    path('login', public_views.login),

    # entity
    path('categories', public_views.get_categories),
    path('category/<category_id>', public_views.get_category),

    # entity
    path('entity/<entity_id>', public_views.get_entity),
    path('filter_entity', public_views.FilterAPIView.as_view()),

    # home
    path('for_you/<entity_type>', public_views.for_you),
    path('top_100/<entity_type>', public_views.top_100),
    path('icons', public_views.get_icons),
]
