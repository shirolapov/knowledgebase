from django.conf.urls import url
from accounts.views import (logout_page, login_page,
                            operators_list, add_operator,
                            change_operator)


app_name = "accounts"
urlpatterns = [
    url(r'^logout/', logout_page, name="logout"),
    url(r'^login/', login_page, name="login"),
    url(r'^operatorslist/', operators_list, name="operatorslist"),
    url(r'^add/', add_operator, name="add"),
    url(r'^change/(?P<id>[0-9]+)/', change_operator, name="change"),
]
