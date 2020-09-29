from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:item_id>",views.displayListing,name="listing"),
    path("watchlist", views.toggleWL, name="watchlist"),
    path("place_bid/<int:item_id>", views.place_bid, name="place_bid"),
    path("close_bid/<int:item_id>", views.close_bid, name="close_bid")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
