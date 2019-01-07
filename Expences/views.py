from django.views.generic import View
from django.shortcuts import render
from rest_framework import viewsets
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
import io

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer

class NewClaimViewSet(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin
                        ):

    serializer_class = NewClaimSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ClaimDetails.objects.filter(employee=self.request.user)

    authentication_classes=[TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def perform_create(self,serializer):
        serializer.save(employee=self.request.user)

    def put(self,request,id=None):
        claim = ClaimDetails.objects.get(id=id)
        if claim.employee != self.request.user:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        if claim.status == 'Requested' or claim.status == 'Rejected':
            return self.partial_update(request)
        else:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
    
    def delete(self,request,id=None):
        claim = ClaimDetails.objects.get(id=id)
        if claim.employee != self.request.user:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        if claim.status == 'Requested' or claim.status == 'Rejected':
            return self.destroy(request,id)
        else:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
    
#Claim Types - List
class ClaimTypesViewSet(generics.GenericAPIView,
                        mixins.ListModelMixin
                        ):
    queryset = ThirdClaimTypes.objects.all()
    serializer_class = ClaimTypesSerializer
    lookup_field = 'claim_types3'

    def get(self,request):
        return self.list(request)    