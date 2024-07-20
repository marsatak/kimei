# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Air(models.Model):
    compresseur = models.ForeignKey('Compresseur', models.DO_NOTHING)
    type = models.ForeignKey('TypeAir', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleAir', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'air'

    def __str__(self):
        return self.compresseur

    pass


class AppareilDistribution(models.Model):
    piste = models.ForeignKey('Piste', models.DO_NOTHING)
    modele_ad = models.ForeignKey('ModeleAd', models.DO_NOTHING)
    num_serie = models.CharField(max_length=50)
    type_contrat = models.CharField(max_length=10)
    annee_installation = models.IntegerField(blank=True, null=True)
    face_principal = models.IntegerField(blank=True, null=True)
    face_secondaire = models.IntegerField(blank=True, null=True)
    is_face_unique = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appareil_distribution'

    def __str__(self):
        return f"${self.modele_ad}     ${self.num_serie}"


class Appelant(models.Model):
    client = models.ForeignKey('Client', models.DO_NOTHING)
    nom_appelant = models.CharField(max_length=50)
    prenom_appelant = models.CharField(max_length=255)
    email_appelant = models.CharField(max_length=50)
    num_appelant = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appelant'

    def __str__(self):
        return f"${self.nom_appelant} ${self.prenom_appelant}"


class Auvent(models.Model):
    piste = models.ForeignKey('Piste', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleAuvent', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'auvent'

    def __str__(self):
        return self.modele


class BonEntree(models.Model):
    num_be = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bon_entree'


class BonSortie(models.Model):
    num_bs = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bon_sortie'


class Boutique(models.Model):
    station = models.OneToOneField('Station', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'boutique'

    def __str__(self):
        return self.station


class Client(models.Model):
    nom_client = models.CharField(unique=True, max_length=191)
    num_prefix = models.SmallIntegerField(unique=True)

    class Meta:
        managed = False
        app_label = 'gmao'
        db_table = 'client'

    def __str__(self):
        return self.nom_client

    def get_data_client(self):
        return {
            'id': self.id,
            'nom_client': self.nom_client,
            'num_prefix': self.num_prefix
        }


class Compresseur(models.Model):
    servicing = models.ForeignKey('Servicing', models.DO_NOTHING)
    marque = models.ForeignKey('MarqueCompresseur', models.DO_NOTHING)
    pression = models.IntegerField()
    debit = models.IntegerField()
    puissance = models.IntegerField()
    annee = models.IntegerField()
    type_contrat = models.CharField(max_length=50)
    capacite = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'compresseur'

    def __str__(self):
        return self.servicing


class Cuve(models.Model):
    piste = models.ForeignKey('Piste', models.DO_NOTHING)
    produit = models.ForeignKey('Produit', models.DO_NOTHING)
    libelle = models.CharField(max_length=50)
    type_contrat = models.CharField(max_length=10)
    capacite = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cuve'

    def __str__(self):
        return self.libelle


class Doleance(models.Model):
    STATUT_CHOICES = [
        ('NEW', 'Nouvelle'),
        ('ATT', 'En attente'),
        ('INT', 'En intervention'),
        ('ATP', 'Attente pièces'),
        ('ATD', 'Attente devis'),
        ('TER', 'Terminée'),
    ]
    station = models.ForeignKey('Station', models.DO_NOTHING)
    appelant = models.ForeignKey(Appelant, models.DO_NOTHING, blank=True, null=True)
    date_transmission = models.DateTimeField(blank=True, null=True)
    ndi = models.CharField(max_length=255)
    date_deadline = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='NEW')
    type_transmission = models.CharField(max_length=50)
    panne_declarer = models.TextField()
    commentaire = models.TextField(blank=True, null=True)
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    element = models.CharField(max_length=255, blank=True, null=True)
    bt = models.CharField(max_length=11, blank=True, null=True)
    type_contrat = models.CharField(max_length=10)
    is_facture = models.IntegerField(blank=True, null=True)
    num_facture = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doleance'

    def __str__(self):
        return f"{self.station} - {self.ndi}"


class EclairageAuvent(models.Model):
    auvent = models.ForeignKey(Auvent, models.DO_NOTHING)
    type = models.ForeignKey('TypeEclairageAuvent', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleEclairageAuvent', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'eclairage_auvent'

    def __str__(self):
        return self.auvent


class EclairageBoutique(models.Model):
    boutique = models.ForeignKey(Boutique, models.DO_NOTHING)
    type = models.ForeignKey('TypeEclairageBoutique', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleEclairageBoutique', models.DO_NOTHING, blank=True, null=True)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'eclairage_boutique'

    def __str__(self):
        return self.boutique


class EclairageElectricite(models.Model):
    electricite = models.ForeignKey('Elec', models.DO_NOTHING)
    type = models.ForeignKey('TypeEclairageElectricite', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleEclairageElectricite', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'eclairage_electricite'


class EclairageServicing(models.Model):
    servicing = models.ForeignKey('Servicing', models.DO_NOTHING)
    type = models.ForeignKey('TypeEclairageServicing', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleEclairageServicing', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'eclairage_servicing'


class EclairageTotem(models.Model):
    type = models.ForeignKey('TypeEclairageTotem', models.DO_NOTHING)
    totem = models.ForeignKey('Totem', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleEclairageTotem', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'eclairage_totem'


class Elec(models.Model):
    station = models.OneToOneField('Station', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'elec'

    def __str__(self):
        return self.station


class Fournisseur(models.Model):
    fournissseur = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'fournisseur'


class Froid(models.Model):
    boutique = models.ForeignKey(Boutique, models.DO_NOTHING)
    type = models.ForeignKey('TypeFroid', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleFroid', models.DO_NOTHING, blank=True, null=True)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'froid'


class GroupeElectrogene(models.Model):
    electricite = models.ForeignKey(Elec, models.DO_NOTHING)
    type = models.ForeignKey('TypeGroupeElectrogene', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'groupe_electrogene'


class Intervention(models.Model):
    doleance = models.ForeignKey(Doleance, models.DO_NOTHING, blank=True, null=True)
    top_depart = models.DateTimeField(blank=True, null=True)
    top_debut = models.DateTimeField(blank=True, null=True)
    top_terminer = models.DateTimeField(blank=True, null=True)
    duree_intervention = models.BigIntegerField(blank=True, null=True)
    kilometrage_depart_debut = models.IntegerField(blank=True, null=True)
    kilometrage_home = models.IntegerField(blank=True, null=True)
    is_done = models.IntegerField()
    is_half_done = models.IntegerField()
    is_going_home = models.IntegerField()
    etat_doleance = models.CharField(max_length=20, blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    numero_fiche = models.CharField(unique=True, max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intervention'

    def __str__(self):
        return self.doleance.ndi


class InterventionPersonnel(models.Model):
    intervention = models.OneToOneField(Intervention, models.DO_NOTHING,
                                        primary_key=True)  # The composite primary key (intervention_id, personnel_id) found, that is not supported. The first column is selected.
    personnel = models.ForeignKey('Personnel', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intervention_personnel'
        unique_together = (('intervention', 'personnel'),)


class InterventionVehicule(models.Model):
    intervention = models.OneToOneField(Intervention, models.DO_NOTHING,
                                        primary_key=True)
    vehicule = models.ForeignKey('Vehicule', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intervention_vehicule'
        unique_together = (('intervention', 'vehicule'),)


class Lavage(models.Model):
    compresseur = models.ForeignKey(Compresseur, models.DO_NOTHING)
    type = models.ForeignKey('TypeLavage', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleLavage', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'lavage'


class Lub(models.Model):
    compresseur = models.ForeignKey(Compresseur, models.DO_NOTHING)
    type = models.ForeignKey('TypeLub', models.DO_NOTHING)
    modele = models.ForeignKey('ModeleLub', models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'lub'


class MarqueAd(models.Model):
    libelle_marque = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'marque_ad'

    def __str__(self):
        return self.libelle_marque


class MarqueCompresseur(models.Model):
    libelle_marque = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'marque_compresseur'


class MarqueGroupeElectrogene(models.Model):
    libelle_marque = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'marque_groupe_electrogene'


class MarquePistoletCompresseur(models.Model):
    type_pistolet_compresseur = models.ForeignKey('TypePistoletCompresseur', models.DO_NOTHING)
    libelle_marque = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'marque_pistolet_compresseur'


class MigrationVersions(models.Model):
    version = models.CharField(primary_key=True, max_length=14)
    executed_at = models.DateTimeField(db_comment='(DC2Type:datetime_immutable)')

    class Meta:
        managed = False
        db_table = 'migration_versions'


class Modele(models.Model):
    class Meta:
        managed = False
        db_table = 'modele'

    def __str__(self):
        return self.libelle_modele


class ModeleAd(models.Model):
    libelle_modele = models.CharField(max_length=255)
    marque_ad = models.ForeignKey(MarqueAd, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'modele_ad'

    def __str__(self):
        return f"{self.libelle_modele} - {self.marque_ad}"


class ModeleAir(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_air'


class ModeleAuvent(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_auvent'


class ModeleCompresseur(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_compresseur'


class ModeleEclairageAuvent(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_eclairage_auvent'


class ModeleEclairageBoutique(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_eclairage_boutique'


class ModeleEclairageElectricite(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_eclairage_electricite'


class ModeleEclairageServicing(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_eclairage_servicing'


class ModeleEclairageTotem(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_eclairage_totem'


class ModeleFroid(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_froid'


class ModeleGroupeElectrogene(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_groupe_electrogene'


class ModeleLavage(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_lavage'


class ModeleLub(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_lub'


class ModelePrise(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_prise'


class ModeleTgbt(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_tgbt'


class ModeleTotem(models.Model):
    libelle_modele = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'modele_totem'


class Personnel(models.Model):
    poste = models.ForeignKey('Poste', models.DO_NOTHING)
    nom_personnel = models.CharField(max_length=255)
    prenom_personnel = models.CharField(max_length=255)
    matricule = models.CharField(unique=True, max_length=10)
    statut = models.CharField(max_length=3, choices=[
        ('PRS', 'Présent'),
        ('ABS', 'Absent'),
        ('ATT', 'Tâche Attribuée'),
        ('INT', 'En intervention'),
        # ('CNG', 'Congé'),
        # ('MIS', 'Mission'),
        # ('MAL', 'Maladie'),
        # ('VAC', 'Vacance'),
    ], default='ABS')
    num1 = models.CharField(max_length=13, blank=True, null=True)
    num2 = models.CharField(max_length=13, blank=True, null=True)
    num3 = models.CharField(max_length=13, blank=True, null=True)
    adresse = models.CharField(max_length=50, blank=True, null=True)
    last_visite_medical = models.DateTimeField(blank=True, null=True)
    cin = models.CharField(max_length=12, blank=True, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'personnel'

    pass


class Piece(models.Model):
    piece_libelle = models.CharField(max_length=255)
    piece_reference = models.CharField(max_length=255)
    constructeur_reference = models.CharField(max_length=255, blank=True, null=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.ForeignKey('UnitePiece', models.DO_NOTHING)
    entree = models.DecimalField(max_digits=10, decimal_places=2)
    sortie = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actuelle = models.DecimalField(max_digits=10, decimal_places=2)
    seuil = models.CharField(max_length=255)
    type = models.ForeignKey('TypePiece', models.DO_NOTHING)
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    stock_securite = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'piece'


class PieceDevis(models.Model):
    unite = models.ForeignKey('UnitePiece', models.DO_NOTHING)
    intervention = models.ForeignKey(Intervention, models.DO_NOTHING)
    designations = models.CharField(max_length=255)
    quantite = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'piece_devis'


class PieceEntree(models.Model):
    num_be = models.ForeignKey(BonEntree, models.DO_NOTHING, blank=True, null=True)
    fournisseur = models.ForeignKey(Fournisseur, models.DO_NOTHING, blank=True, null=True)
    piece = models.OneToOneField(Piece, models.DO_NOTHING)
    responsable = models.ForeignKey(Personnel, models.DO_NOTHING)
    date_entree = models.DateField()
    quantite = models.DecimalField(max_digits=12, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)
    valeur = models.DecimalField(max_digits=12, decimal_places=2)
    num_facture = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'piece_entree'


class PieceIntervention(models.Model):
    piece = models.ForeignKey(Piece, models.DO_NOTHING)
    intervention = models.ForeignKey(Intervention, models.DO_NOTHING)
    num_bs = models.ForeignKey(BonSortie, models.DO_NOTHING)
    responsable = models.OneToOneField(Personnel, models.DO_NOTHING)
    date_sortie = models.DateField()
    num_bt = models.CharField(max_length=100, blank=True, null=True)
    num_bc = models.CharField(max_length=100, blank=True, null=True)
    sortie_provisoire = models.DecimalField(max_digits=5, decimal_places=2)
    retour = models.DecimalField(max_digits=5, decimal_places=2)
    sortie_reelle = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'piece_intervention'


class Piste(models.Model):
    station = models.OneToOneField('Station', models.DO_NOTHING)
    nombre_ilot = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'piste'

    def __str__(self):
        return self.station


class Pistolet(models.Model):
    produit = models.ForeignKey('Produit', models.DO_NOTHING)
    appareil_distribution = models.ForeignKey(AppareilDistribution, models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)
    date_flexible = models.CharField(max_length=4, blank=True, null=True)
    orientation = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'pistolet'

    def __str__(self):
        return str(self.appareil_distribution)


class PistoletCompresseur(models.Model):
    compresseur = models.ForeignKey(Compresseur, models.DO_NOTHING)
    marque_pistolet = models.ForeignKey(MarquePistoletCompresseur, models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'pistolet_compresseur'


class Pointage(models.Model):
    personnel = models.ForeignKey(Personnel, models.DO_NOTHING)
    date_heure_arrive = models.DateTimeField(blank=True, null=True)
    date_heure_sortie = models.DateTimeField(blank=True, null=True)
    seconde_actif = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointage'

    def __str__(self):
        return str(self.date_heure_arrive)


class Poste(models.Model):
    nom_poste = models.CharField(max_length=100)
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'poste'

    def __str__(self):
        return self.nom_poste

    def __unicode__(self):
        return self.nom_poste


class Prise(models.Model):
    boutique = models.ForeignKey(Boutique, models.DO_NOTHING)
    type = models.ForeignKey('TypePrise', models.DO_NOTHING)
    modele = models.ForeignKey(ModelePrise, models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'prise'


class Produit(models.Model):
    nom_produit = models.CharField(max_length=50)
    code_produit = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'produit'

    def __str__(self):
        return self.nom_produit


class Servicing(models.Model):
    station = models.OneToOneField('Station', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'servicing'


class Station(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING)
    lieu_station = models.CharField(max_length=50)
    province_station = models.CharField(max_length=50)
    libelle_station = models.CharField(max_length=50)
    type_contrat = models.CharField(max_length=10)
    have_servicing = models.IntegerField()
    have_boutique = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'station'

    def __str__(self):
        return self.libelle_station

    def get_data_station(self):
        return {
            'libelle_station': self.libelle_station,
        }


class Tgbt(models.Model):
    electricite = models.ForeignKey(Elec, models.DO_NOTHING)
    type = models.ForeignKey('TypeTgbt', models.DO_NOTHING)
    modele = models.ForeignKey(ModeleTgbt, models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tgbt'


class Totem(models.Model):
    piste = models.ForeignKey(Piste, models.DO_NOTHING)
    modele = models.ForeignKey(ModeleTotem, models.DO_NOTHING)
    type_contrat = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'totem'


class TypeAir(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_air'


class TypeCompresseur(models.Model):
    marque_compresseur = models.ForeignKey(MarqueCompresseur, models.DO_NOTHING)
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_compresseur'


class TypeEclairageAuvent(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_eclairage_auvent'


class TypeEclairageBoutique(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_eclairage_boutique'


class TypeEclairageElectricite(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_eclairage_electricite'


class TypeEclairageServicing(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_eclairage_servicing'


class TypeEclairageTotem(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_eclairage_totem'


class TypeFroid(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_froid'


class TypeGroupeElectrogene(models.Model):
    libelle_type = models.CharField(max_length=255)
    marque_groupe_electrogene = models.ForeignKey(MarqueGroupeElectrogene, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_groupe_electrogene'


class TypeLavage(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_lavage'


class TypeLub(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_lub'


class TypePiece(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_piece'


class TypePistoletCompresseur(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_pistolet_compresseur'


class TypePrise(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_prise'


class TypeTgbt(models.Model):
    libelle_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type_tgbt'


class UnitePiece(models.Model):
    unite = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'unite_piece'


class User(models.Model):
    username = models.CharField(unique=True, max_length=180)
    roles = models.TextField()
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'


class Vehicule(models.Model):
    libelle_vehicule = models.CharField(max_length=255)
    marque_vehicule = models.CharField(max_length=50)
    numero_vehicule = models.CharField(max_length=50)
    kilometrage_vehicule = models.IntegerField(blank=True, null=True)
    limit_assurance = models.DateTimeField(blank=True, null=True)
    last_visite_technique = models.DateTimeField(blank=True, null=True)
    last_vidange = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'vehicule'

# ... (autres imports et classes existantes)


# ... (autres classes existantes)
