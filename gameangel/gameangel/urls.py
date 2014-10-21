from django.conf.urls import patterns, url
from gameangel import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^Game/(?P<game_id>\w+)/$', views.GameDetail, name='gamedetail'),
        url(r'^add_game/$', views.add_game, name='add_game'), # NEW MAPPING!
        # url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'), 
        url(r'^register/$', views.register, name='register'),
        url(r'^restricted/', views.restricted, name='restricted'), #View that requires users to login
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^suggest_game/$', views.suggest_game, name='suggest_game'),
        url(r'^add_comment/$',views.add_comment,name='add_comment'),
)
