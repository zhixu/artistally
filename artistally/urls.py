from django.conf.urls import include, url
from django.contrib import admin

from aa_app import models

import datetime

if models.Convention.objects.filter(name = "INV_CON").exists():
    models.INV_CON = models.Convention.objects.get(name = "INV_CON")
else:
    models.INV_CON = models.newConvention("INV_CON", datetime.datetime(1, 1, 1), datetime.datetime(1, 1, 1), 1, "artistally", "https://artistal.ly")
    
urlpatterns = [
    url(r"^$", "aa_app.views.site.root"),
    url(r"^404$", "django.views.defaults.page_not_found"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^signup$", "aa_app.views.site.signup"),
    url(r"^login$", "aa_app.views.site.login"),
    url(r"^inventory$", "aa_app.views.site.inventory"),
    url(r"^myconventions$", "aa_app.views.site.myconventions"),
    url(r"^mywriteups$", "aa_app.views.site.mywriteups"),
    url(r"^addconvention$", "aa_app.views.site.addconvention"),
    url(r"^addkind$", "aa_app.views.site.addkind"),
    url(r"^addfandom$", "aa_app.views.site.addfandom"),
    url(r"^additem$", "aa_app.views.site.additem"),
    url(r"^additem/([0-9]+)?$", "aa_app.views.site.additem"),
    url(r"^addwriteup$", "aa_app.views.site.addwriteup"),
    url(r"^addwriteup/([0-9]+)?$", "aa_app.views.site.addwriteup"),
    url(r"^user/([0-9A-Za-z_\-]+)$", "aa_app.views.site.user"),
    url(r"^convention/([0-9]+)$", "aa_app.views.site.convention"),
    url(r"^item/([0-9]+)$", "aa_app.views.site.item"),
    url(r"^writeup/([0-9]+)$", "aa_app.views.site.writeup"),
    url(r"^api/user/newUser$", "aa_app.views.api.user.newUser"),
    url(r"^api/user/login$", "aa_app.views.api.user.login"),
    url(r"^api/user/logout$", "aa_app.views.api.user.logout"),
    url(r"^api/user/setEmail$", "aa_app.views.api.user.setEmail"),
    url(r"^api/user/setPassword$", "aa_app.views.api.user.setPassword"),
    url(r"^api/user/setStartYear$", "aa_app.views.api.user.setStartYear"),
    url(r"^api/user/setImage$", "aa_app.views.api.user.setImage"),
    url(r"^api/user/setDescription$", "aa_app.views.api.user.setDescription"),
    url(r"^api/user/setWebsite1$", "aa_app.views.api.user.setWebsite1"),
    url(r"^api/user/setWebsite2$", "aa_app.views.api.user.setWebsite2"),
    url(r"^api/user/setWebsite3$", "aa_app.views.api.user.setWebsite3"),
    url(r"^api/item/newItem$", "aa_app.views.api.item.newItem"),
    url(r"^api/item/deleteItem$", "aa_app.views.api.item.deleteItem"),
    url(r"^api/item/setNumSold$", "aa_app.views.api.item.setNumSold"),
    url(r"^api/item/setNumLeft$", "aa_app.views.api.item.setNumLeft"),
    url(r"^api/item/setName$", "aa_app.views.api.item.setName"),
    url(r"^api/item/setImage$", "aa_app.views.api.item.setImage"),
    url(r"^api/item/setPrice$", "aa_app.views.api.item.setPrice"),
    url(r"^api/item/setCost$", "aa_app.views.api.item.setCost"),
    url(r"^api/item/setFandom$", "aa_app.views.api.item.setFandom"),
    url(r"^api/item/setKind$", "aa_app.views.api.item.setKind"),
    url(r"^api/writeup/newWriteup$", "aa_app.views.api.writeup.newWriteup"),
    url(r"^api/writeup/setRating$", "aa_app.views.api.writeup.setRating"),
    url(r"^api/writeup/setReview$", "aa_app.views.api.writeup.setReview"),
    url(r"^api/miscCost/newMiscCost$", "aa_app.views.api.miscCost.newMiscCost"),
    url(r"^api/miscCost/setAmount$", "aa_app.views.api.miscCost.setAmount"),
    url(r"^api/fandom/newFandom$", "aa_app.views.api.fandom.newFandom"),
    url(r"^api/fandom/setName$", "aa_app.views.api.fandom.setName"),
    url(r"^api/kind/newKind$", "aa_app.views.api.kind.newKind"),
    url(r"^api/kind/setName$", "aa_app.views.api.kind.setName"),
    url(r"^api/convention/newConvention$", "aa_app.views.api.convention.newConvention"),
    url(r"^api/convention/setName$", "aa_app.views.api.convention.setName"),
    url(r"^api/convention/setNumAttenders$", "aa_app.views.api.convention.setNumAttenders"),
    url(r"^api/convention/setLocation$", "aa_app.views.api.convention.setLocation"),
    url(r"^api/convention/setStartDate$", "aa_app.views.api.convention.setStartDate"),
    url(r"^api/convention/setEndDate$", "aa_app.views.api.convention.setEndDate"),
    url(r"^api/convention/setImage$", "aa_app.views.api.convention.setImage"),
    url(r"^api/util/uploadFile$", "aa_app.views.api.util.uploadFile"),
]
