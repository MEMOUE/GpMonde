from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, UpdateUserSerializer
from rest_framework.permissions import IsAdminUser
from .models import VisitorActivityLog
from .serializers import VisitorActivityLogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permet à tout le monde de s'inscrire

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Authentifier et connecter l'utilisateur
            login(request, user)

            # Générer le token JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Utilisateur créé avec succès. Veuillez vérifier votre email.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "sessionid": request.session.session_key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)

        user.is_active = True
        user.email_verified = True
        user.verification_token = None
        user.save()

        return Response({"message": "Votre email a été vérifié avec succès !"}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "Ce lien de vérification est invalide ou a expiré."},
                        status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Afficher l'erreur dans les logs pour le débogage
        import traceback
        print(f"Erreur lors de la vérification de l'email: {str(e)}")
        print(traceback.format_exc())
        return Response({"error": "Une erreur est survenue lors de la vérification de l'email."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except CustomUser.DoesNotExist:
        # Si l'utilisateur n'existe pas, renvoyer une réponse appropriée
        return Response({"error": "Ce lien de vérification est invalide ou a expiré."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Afficher l'erreur dans les logs pour le débogage
        import traceback
        print(f"Erreur lors de la vérification de l'email: {str(e)}")  # Log de l'erreur
        print(traceback.format_exc())  # Afficher la trace de la pile
        return Response({"error": "Une erreur est survenue lors de la vérification de l'email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil mis à jour avec succès"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklister le refresh token JWT
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Supprimer la session
            logout(request)

            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class VisitorActivityLogView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = VisitorActivityLog.objects.all().order_by('-timestamp')
        serializer = VisitorActivityLogSerializer(logs, many=True)
        return Response(serializer.data)