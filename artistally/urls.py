from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/user/newUser$', 'aa_app.api_user_views.newUser'),
    url(r'^api/user/login$', 'aa_app.api_user_views.login'),
    url(r'^api/user/logout$', 'aa_app.api_user_views.logout'),
    url(r'^api/user/setEmail$', 'aa_app.api_user_views.setEmail'),
    url(r'^api/user/setPassword$', 'aa_app.api_user_views.setPassword'),
    url(r'^api/user/setUsername$', 'aa_app.api_user_views.setUsername'),
    url(r'^api/item/newItem$', 'aa_app.api_item_views.newItem'),
    url(r'^api/item/setNumSold$', 'aa_app.api_item_views.setNumSold'),
    url(r'^api/item/setNumLeft$', 'aa_app.api_item_views.setNumLeft'),
]
