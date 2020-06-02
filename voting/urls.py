from django.urls import path                                              
from voting import views            # always make templates folder in folder where manage.py is
urlpatterns = [
    path('',views.choose,name='choose'),
    path('votingpage/',views.votingpage,name='votingpage'),
    # path('logout/',views.logout,name='logout'),
    path('votingpage/thanks/',views.thanks,name='thank'),
    path('result/',views.result,name='result'),
    
]
