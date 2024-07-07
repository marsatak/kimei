from django.urls import path
from . import views

app_name = 'gmao_teams'

urlpatterns = [
    path('gestion-equipes', views.gestion_equipes, name='gestion_equipes'),
    path('creer/', views.creer_equipe, name='creer_equipe'),
    path('liste/', views.liste_equipes, name='liste_equipes'),
    path('<int:equipe_id>/details/', views.get_equipe_details, name='get_equipe_details'),
    path('<int:equipe_id>/affecter-technicien/', views.affecter_technicien, name='affecter_technicien'),
    path('<int:equipe_id>/attribuer-doleance/', views.attribuer_doleance, name='attribuer_doleance'),
    path('<int:equipe_id>/retirer-technicien/', views.retirer_technicien, name='retirer_technicien'),
    path('<int:equipe_id>/retirer-doleance/', views.retirer_doleance, name='retirer_doleance'),
    path('techniciens-disponibles/', views.get_techniciens_disponibles, name='get_techniciens_disponibles'),
    path('doleances-non-attribuees/', views.get_doleances_non_attribuees, name='get_doleances_non_attribuees'),
    path('get-pieces-non-attribuees/', views.get_pieces_non_attribuees, name='get_pieces_non_attribuees'),
    path('attribuer-piece/<int:equipe_id>/', views.attribuer_piece, name='attribuer_piece'),
    path('retirer-piece/<int:equipe_id>/', views.retirer_piece, name='retirer_piece'),
]
