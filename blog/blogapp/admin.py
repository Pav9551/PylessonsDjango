from django.contrib import admin
from .models import Category, Post, Tag, Good, Shop, Merchandise,Coincidence, Post_for_Coincidence

#admin.site.register(Category)
#admin.site.register(Post)
#admin.site.register(Tag)
admin.site.register(Good)
admin.site.register(Shop)
admin.site.register(Merchandise)
admin.site.register(Coincidence)
admin.site.register(Post_for_Coincidence)