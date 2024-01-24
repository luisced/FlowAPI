from .user_urls import urlpatterns as user_urlpatterns
from .class_loader_urls import urlpatterns as class_loader_urlpatterns
from .schedule_generator_urls import urlpatterns as schedule_generator_urlpatterns

urlpatterns = []
urlpatterns += user_urlpatterns
urlpatterns += class_loader_urlpatterns
urlpatterns += schedule_generator_urlpatterns
# ... and so on for other urlpatterns imports
