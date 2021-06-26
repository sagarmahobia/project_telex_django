from django.urls import path
from app.admin_views import views

urlpatterns = [
    path('category/add', views.add_category),
    path('category/edit/<category_id>', views.edit_category),
    path('category/delete/<category_id>', views.delete_category),

    path('entity/add', views.add_entity),
    path('entity/edit/<entity_id>', views.edit_entity),
    path('entity/delete/<entity_id>', views.delete_entity),

    path('entity/add_bulk', views.add_bulk_entity),

    path('entities/channels', views.get_channels),
    path('entities/bots', views.get_bots),
    path('entities/groups', views.get_groups),

]
