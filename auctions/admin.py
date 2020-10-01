from django.contrib import admin

from .models import Bid, Listing, User, Catergory, WatchList, Comment, WinningBid
# Register your models here.
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Catergory)
admin.site.register(WatchList)
admin.site.register(Comment)
admin.site.register(WinningBid)
