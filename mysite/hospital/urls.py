from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('doctor_login',views.doctor_login,name='doctor_login'),
    path('logout',views.logout,name='logout'),
    path('patient_register',views.patient_register,name='patient_register'),
    path('doctor_after_login',views.doctor_after_login,name='doctor_after_login'),
    path('appointment_booking',views.appointment_booking,name='appointment_booking'),
    path('staff_admin',views.staff_admin,name='staff_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)