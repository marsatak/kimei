from django.db import models


class Equipe(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'equipe'

    def __str__(self):
        return self.nom

    def get_personnel_ids(self):
        return list(self.equipepersonnel_set.values_list('personnel_id', flat=True))

    def get_doleance_ids(self):
        return list(self.doleanceequipe_set.values_list('doleance_id', flat=True))


class EquipePersonnel(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    personnel_id = models.IntegerField()

    class Meta:
        db_table = 'equipe_personnel'
        unique_together = (('equipe', 'personnel_id'),)


class DoleanceEquipe(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    doleance_id = models.IntegerField()

    class Meta:
        db_table = 'doleance_equipe'
        unique_together = (('equipe', 'doleance_id'),)
