from django.utils import timezone
from django.db.models import Q


def filter_active_doleances(queryset):
    today = timezone.localtime(timezone.now()).date()
    return queryset.exclude(
        Q(statut='TER') |
        (Q(statut__in=['ATP', 'ATD']) & Q(intervention__top_terminer__date=today))
    )
