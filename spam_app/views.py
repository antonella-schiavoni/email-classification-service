from os import name
from typing import Generic
from .models import Predictions, UserQuota
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .apps import SpamAppConfig
from rest_framework.response import Response
import logging
from django.contrib.auth.models import User

class process_email(APIView):

    def post(self, request):
        # filter users from db by name
        user = User.objects.filter(username=request.user)[0]
        user_quota = UserQuota.objects.filter(user=user)[0]
        #if request.user == users[0].name: # Luego habria que ver como validar una vez que tengamos hecha la autenticacion
        if user_quota.quota_available >= 1:
            text =  [request.POST.get('text')]
            logging.info(f"Email text: {text}")
            # predict method used to get the prediction
            if text:
                prediction = SpamAppConfig.model.predict(text)[0]
                # parse prediction to True/False
                result = 'SPAM' if prediction == 1 else 'HAM'
                # save data into the DB
                prediction_obj = Predictions.objects.create(user=user,
                                                            text_email=text,
                                                            prediction=result)
                prediction_obj.save()
                
                user_quota.quota_available  = user_quota.quota_available - 1
                user_quota.save()
                user.save()
                # build response as dict
                response = {"result": result, 'status': 'ok'}
                # returning JSON response
                return JsonResponse(response)
            else:
                raise ValidationError("Text field is required")
        else: 
            response = {"status":"fail","message":"No quota left"}
            return JsonResponse(response)


class quota_info(APIView):
    def get(self, request):
        user = User.objects.filter(username=request.user)[0] # add check if list is empty
        user_quota = UserQuota.objects.filter(user=user)[0] # add check if list is empty
        quota_processed =  user_quota.quota_origin - user_quota.quota_available
        response = {'procesados': quota_processed, 'disponible': user_quota.quota_available}
        return JsonResponse(response)


class history(APIView):
    def get(self, request, n_emails: None):
        processed_emails = Predictions.objects.all().order_by('-created_at')
        results = []
        counter = 0
        for pred in processed_emails:
            if counter < int(n_emails):
                text = pred.text_email
                created_at = pred.created_at
                prediction = 'SPAM' if pred.prediction == 1 else 'HAM'
                results.append({'text': text, 'result': prediction, 'created_at': created_at})
                counter += 1
            else:
                break
        response = {'results': results}
        return JsonResponse(response)


class test_if_logged(APIView):

    def get(self, request):
        # en request.user tiene el objeto user de quien hizo el pedido
        return Response({'status':'ok!', 'user': str(request.user)})