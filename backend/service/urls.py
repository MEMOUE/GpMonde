from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'compagnies', views.CompagnieTransportViewSet)
router.register(r'transporteurs', views.TransporteurColisViewSet)
router.register(r'agences', views.AgenceVenteBilletViewSet)
router.register(r'programmes', views.ProgrammeVoyageViewSet)
router.register(r'emballages', views.AgenceEmballageViewSet)
router.register(r'offres', views.OffreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit_besoin/', views.submit_besoin, name='submit_besoin'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('mark_notification_as_read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('offres-actives/', views.offres_actives, name='offres_actives'),
    path('besoins-actives/', views.besoins_actives, name='besions_actives'),
]
