from .user_urls import urlpatterns as user_urlpatterns
from .class_loader_urls import urlpatterns as class_loader_urlpatterns

urlpatterns = []
urlpatterns += user_urlpatterns
# ... and so on for other urlpatterns imports
