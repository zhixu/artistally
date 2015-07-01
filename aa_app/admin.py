from django.contrib import admin

from aa_app import models

admin.site.register(models.Convention)
admin.site.register(models.User)
admin.site.register(models.Item)
admin.site.register(models.Fandom)
admin.site.register(models.Kind)
admin.site.register(models.Writeup)

from django.template.base import add_to_builtins

add_to_builtins("aa_app.templatetags.aa_filters")
