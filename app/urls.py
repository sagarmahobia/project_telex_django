from django.urls import path, include

urlpatterns = [
    path('protected/admin/', include("app.admin_views.admin_urls"), ),

    path('public/', include("app.public_views.public_urls", )),
]
