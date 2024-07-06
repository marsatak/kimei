from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import Employee
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from gmao.models import Doleance, Intervention, Personnel
from gmao.serializers import DoleanceSerializer, InterventionSerializer, PersonnelSerializer


class LoginView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'matricule': user.matricule
                }
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'matricule': user.matricule
        })


class TechnicienViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def portfolio(self, request):
        technicien = Personnel.objects.get(matricule=request.user.matricule)
        equipe = EquipePersonnel.objects.filter(personnel_id=technicien.id).first()

        if not equipe:
            return Response({'message': 'Aucune équipe assignée'}, status=400)

        doleance_ids = DoleanceEquipe.objects.filter(equipe=equipe.equipe).values_list('doleance_id', flat=True)
        doleances = Doleance.objects.filter(id__in=doleance_ids).exclude(statut='TER')

        serializer = DoleanceSerializer(doleances, many=True)
        return Response({
            'doleances': serializer.data,
            'equipe': equipe.equipe.nom,
        })

    @action(detail=True, methods=['POST'])
    def prendre_en_charge(self, request, pk=None):
        doleance = Doleance.objects.get(pk=pk)
        technicien = Personnel.objects.get(matricule=request.user.matricule)

        # Logique de prise en charge...

        intervention = Intervention.objects.create(
            doleance=doleance,
            top_depart=timezone.now(),
            etat_doleance='ATT'
        )

        return Response({'success': True, 'intervention_id': intervention.id})

    @action(detail=True, methods=['POST'])
    def commencer_intervention(self, request, pk=None):
        intervention = Intervention.objects.get(pk=pk)
        kilometrage = request.data.get('kilometrage')

        # Logique pour commencer l'intervention...

        return Response({'success': True, 'top_debut': intervention.top_debut})

    @action(detail=True, methods=['POST'])
    def terminer_intervention(self, request, pk=None):
        intervention = Intervention.objects.get(pk=pk)

        # Logique pour terminer l'intervention...

        return Response({'success': True, 'message': 'Intervention terminée avec succès'})
