from django.contrib import admin
from mainapp.models import Media, Food, Dish, CookInfo
from mainapp.models import Order,Session


class MediaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'showimage']


class SessionAdmin(admin.ModelAdmin):
    pass


class FoodAdmin(admin.ModelAdmin):
    pass


class DishAdmin(admin.ModelAdmin):
    pass


class CookInfoAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Media, MediaAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(CookInfo, CookInfoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Session, SessionAdmin)
