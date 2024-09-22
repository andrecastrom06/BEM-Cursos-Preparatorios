from django.contrib import admin
from django.urls import include, path
from cadastros import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('cadastros/', include('cadastros.urls'))
]