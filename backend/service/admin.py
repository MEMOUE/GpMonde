from django.contrib import admin
from .models import CompagnieTransport, TransporteurColis, AgenceVenteBillet, ProgrammeVoyage

@admin.register(CompagnieTransport)
class CompagnieTransportAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'telephone', 'email', 'pays', 'user')
    search_fields = ('nom', 'email', 'pays')
    list_filter = ('pays',)
    ordering = ('nom',)


@admin.register(TransporteurColis)
class TransporteurColisAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'telephone', 'email', 'pays', 'type_transport', 'user')
    search_fields = ('nom', 'email', 'pays')
    list_filter = ('type_transport', 'pays')
    ordering = ('nom',)


@admin.register(AgenceVenteBillet)
class AgenceVenteBilletAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'telephone', 'email', 'pays', 'user')
    search_fields = ('nom', 'email', 'pays')
    list_filter = ('pays',)
    ordering = ('nom',)


@admin.register(ProgrammeVoyage)
class ProgrammeVoyageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_depart', 'date_arrivee', 'pays_depart', 'pays_arrivee', 'telephone', 'user')
    search_fields = ('titre', 'pays_depart', 'pays_arrivee')
    list_filter = ('pays_depart', 'pays_arrivee')
    ordering = ('date_depart',)

    # Pour personnaliser la vue d'édition
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'logo', 'telephone', 'user')
        }),
        ('Dates', {
            'fields': ('date_depart', 'date_arrivee')
        }),
        ('Localisation', {
            'fields': ('pays_depart', 'pays_arrivee')
        }),
    )
