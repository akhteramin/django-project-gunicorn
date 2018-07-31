from django.conf.urls import url

from . import views

app_name = 'ipay-merchant'
urlpatterns = [
    # url(r'^login/$', views.LoginView.as_view,name='login'),
    url(r'^$', views.accounts, name='accounts'),
    url(r'^home/$', views.home, name='home'),
    url(r'^qrcode/$', views.qrcode, name='qrcode'),
    url(r'^accounts/login/$', views.accounts, name='accounts'),
    url(r'^accounts/logout/$', views.accountslogout, name='accountslogout'),
    # url(r'^details/transaction/(?P<trnID>\w+)/$', views.details, name='details'),
    #

]
