from django.db import models
from gmao.models import Piece


class DoleanceEquipe(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    doleance_id = models.IntegerField()
    pieces = models.ManyToManyField(Piece, through='PieceDoleanceEquipe')

    class Meta:
        db_table = 'doleance_equipe'
        unique_together = (('equipe', 'doleance_id'),)


class PieceDoleanceEquipe(models.Model):
    doleance_equipe = models.ForeignKey(DoleanceEquipe, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    class Meta:
        db_table = 'piece_doleance_equipe'
        unique_together = (('doleance_equipe', 'piece'),)
