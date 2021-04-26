from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',views.process ,name='home'),
    path('contact',views.contact,name='contact'),
    path('create-model/',csrf_exempt(views.create_model)),
    path('upload-image/',csrf_exempt(views.upload_image)),
    path('process-image/',csrf_exempt(views.process_image)),
    path('hprocess-image/',csrf_exempt(views.process_image)),
]