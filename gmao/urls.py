from django.urls import path

from gmao import views

app_name = 'gmao'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/test-db/', views.test_db_connection, name='test_db_connection'),
    path('api/data/', views.api_data, name='api-data'),
    path('home/test-view/', views.test_view, name='test-view'),

    # path('home/getClient', views.getClient, name='get-client'),
    # path('home/getClient/<int:id>/', views.getStation, name='get-station'),

    path('home/getDoleanceEncours', views.getDoleanceEncours, name='get-doleance-encours'),
    path('home/get-equipes-data/', views.get_equipes_data, name='get_equipes_data'),
    path('home/create-doleance/', views.create_doleance, name='create_doleance'),
    path('home/get-doleance/<int:doleance_id>/', views.get_doleance, name='get_doleance'),
    path('home/update-doleance/<int:doleance_id>/', views.update_doleance, name='update_doleance'),
    path('home/search-stations/', views.search_stations, name='search_stations'),
    path('home/ajax/load-stations/', views.load_stations, name='load_stations'),
    path('home/ajax/load-appelants/', views.load_appelants, name='load_appelants'),
    path('home/load-elements/', views.load_elements, name='load_elements'),
    # urls.py
    path('home/doleance/<int:doleance_id>/declencher-intervention/', views.declencher_intervention,
         name='declencher_intervention'),
    path('home/affecter-techniciens/<int:doleance_id>/', views.affecter_techniciens, name='affecter_techniciens'),
    # urls.py
    path('home/get-techniciens-disponibles/', views.get_techniciens_disponibles, name='get_techniciens_disponibles'),
    path('home/declencher-intervention/<int:doleance_id>/', views.declencher_intervention,
         name='declencher_intervention'),
    path('home/commencer-intervention/<int:intervention_id>/', views.commencer_intervention,
         name='commencer_intervention'),
    path('home/intervention/<int:intervention_id>/annuler/', views.annuler_intervention, name='annuler_intervention'),
    # path('home/liste-interventions/', views.liste_interventions, name='liste_interventions'),
    path('home/intervention/<int:intervention_id>/', views.detail_intervention, name='detail_intervention'),
    path('home/interventions/', views.liste_interventions, name='liste_interventions'),

    path('home/intervention/<int:intervention_id>/terminer/', views.terminer_travail, name='terminer_travail'),
    path('get-clients/', views.get_clients, name='get_clients'),
    path('home/get-interventions-data/', views.get_interventions_data, name='get_interventions_data'),

    # path('home/intervention/creer/', views.creer_intervention, name='creer_intervention'),
    path('home/toutes-les-doleances/', views.toutes_les_doleances, name='toutes_les_doleances'),
    path('api/get-doleances-data/', views.get_doleances_data, name='get_doleances_data'),
    path('api/get-available-years/', views.get_available_years, name='get_available_years'),
    path('get-technicien-portfolio/', views.get_technicien_portfolio, name='get_technicien_portfolio'),
    path('home/prendre-en-charge/<int:doleance_id>/', views.prendre_en_charge, name='prendre_en_charge'),
    path('home/annuler-prise-en-charge/<int:intervention_id>/', views.annuler_prise_en_charge,
         name='annuler_prise_en_charge'),
    path('home/toutes-les-pieces/', views.toutes_les_pieces, name='toutes_les_pieces'),
    path('home/get-pieces-data/', views.get_pieces_data, name='get_pieces_data'),

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
