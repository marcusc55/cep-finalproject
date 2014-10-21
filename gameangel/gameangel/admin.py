from django.contrib import admin

from gameangel.models import Game, UserProfile, Comment #importing UserProfile
#from bookmark.models import Category, Page, UserProfile #importing UserProfile

#admin.site.register(Category)
#admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Comment)