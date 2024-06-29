from django.urls import path

from gmao import views

app_name = 'gmao'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('api/data/', views.api_data, name='api-data'),

    # path('home/getClient', views.getClient, name='get-client'),
    # path('home/getClient/<int:id>/', views.getStation, name='get-station'),

    path('home/getDoleanceEncours', views.getDoleanceEncours, name='get-doleance-encours'),
    path('home/create-doleance/', views.create_doleance, name='create_doleance'),
    path('home/ajax/load-stations/', views.load_stations, name='load_stations'),
    path('home/ajax/load-appelants/', views.load_appelants, name='load_appelants'),
    path('home/load-elements/', views.load_elements, name='load_elements'),
    # urls.py
    path('home/doleance/<int:doleance_id>/declencher-intervention/', views.declencher_intervention,
         name='declencher_intervention'),
    # urls.py
    path('home/get-techniciens-disponibles/', views.get_techniciens_disponibles, name='get_techniciens_disponibles'),
    path('home/declencher-intervention/<int:doleance_id>/', views.declencher_intervention,
         name='declencher_intervention'),
    path('home/commencer-intervention/<int:intervention_id>/', views.commencer_intervention,
         name='commencer_intervention'),
    path('home/liste-interventions/', views.liste_interventions, name='liste_interventions'),
    path('home/intervention/<int:intervention_id>/', views.detail_intervention, name='detail_intervention'),
    path('home/intervention/<int:intervention_id>/commencer/', views.commencer_travail, name='commencer_travail'),
    path('home/intervention/<int:intervention_id>/terminer/', views.terminer_travail, name='terminer_travail'),
    # path('home/intervention/creer/', views.creer_intervention, name='creer_intervention'),
    path('home/interventions/', views.liste_interventions, name='liste_interventions'),
    # path('home/doleanceencours', views.doleanceencours, name='doleanceencours'),
    # Json des doléances / Toutes les doléances terminées
    # path('home/doleanceListTer', views.doleanceListTer, name='doleanceListTer'),
    # path('home/doleanceTER', views.doleanceTER, name='doleanceTER'),
    # Json des doléances / Toutes les doléances confondues
    # path('home/doleanceAll', views.doleanceAll, name='doleanceAll'),
    # Json de toutes les interventions
    # path('home/getElement', views.getAppareilDistribution, name='get-appareil-distribution'),
    # path('home/getIntervention', views.getIntervention, name='get-intervention'),
    # path('home/exportdemandeencours', views.export_users, name='export_users'),
    # Json des personnels
    path('home/getPoste', views.getPoste, name='get-poste'),
    path('home/getPersonnel/', views.getPersonnel, name='get-personnel'),
    path('home/reset-pointage/', views.resetPointage, name='reset-pointage'),
    path('home/getPointage', views.getPointage, name='get-pointage'),

    path('home/postPointage/', views.postPointage, name='get-pointage'),
    path('home/postPointage/<int:id>/', views.putPointage, name='put-pointage'),
    path('mark-arrivee/<int:personnel_id>/', views.mark_arrivee, name='mark_arrivee'),
    path('mark-depart/<int:personnel_id>/', views.mark_depart, name='mark_depart'),
    path('home/getPersonnel/<int:id>/', views.updatePersonnel, name='update-personnel'),

    # path('home/doleanceEdit2/<int:id>', views.doleanceEdit2, name='doleanceEdit2'),
    # path('home/doleanceEdit/<int:id>/', views.doleanceEdit, name='doleanceEdit'),

    # path('test/', views.test, name='test')

]
