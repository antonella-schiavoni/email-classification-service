from .models import Predictions, UserQuota
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .apps import SpamAppConfig
from rest_framework.response import Response
import logging
from django.contrib.auth.models import User
import json
from django.core.serializers import serialize
from rest_framework import status

class process_email(APIView):

    def post(self, request):
        # filter users from db by name
        user = User.objects.filter(username=request.user)[0]
        user_quota = UserQuota.objects.filter(user=user)[0]
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
        user = User.objects.filter(username=request.user)[0]
        user_quota = UserQuota.objects.filter(user=user)[0]
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
        return Response({'status':'ok!', 'user': str(request.user)})


class get_data(APIView):

    def _serialize(self, db_object):
        object_serialized = json.loads(serialize('json', db_object))
        if object_serialized:
            return object_serialized[0]

    def get(self, request):
        user = User.objects.filter(username=request.user)[0]
        if user.is_superuser == True:
            users_param = request.query_params.get('users')
            if users_param:
                users_list = users_param.split('|')
                users_data = []
                prediction_data = []
                user_quota_data = []
                for user in users_list:
                    user_db = User.objects.filter(username=user)
                    user_serialize = self._serialize(user_db)

                    predictions_db = Predictions.objects.filter(user=user_db[0])
                    predictions_serialize = self._serialize(predictions_db)

                    user_quota = UserQuota.objects.filter(user=user_db[0])
                    user_quota_serialize = self._serialize(user_quota)

                    users_data.append(user_serialize)
                    prediction_data.append(predictions_serialize)
                    user_quota_data.append(user_quota_serialize)

                response = {'users': users_data, 'predictions': prediction_data, 'user_quota': user_quota_data}
            else:
                user_db = User.objects.all()
                user_serialize = self._serialize(user_db)

                predictions_db = Predictions.objects.all()
                predictions_serialize = self._serialize(predictions_db)

                user_quota = UserQuota.objects.all()
                user_quota_serialize = self._serialize(user_quota)

                response = {
                            'users': user_serialize, 
                            'predictions': predictions_serialize,
                            'user_quota': user_quota_serialize
                            }       
                return JsonResponse(response)
        else:
            return JsonResponse({'staus': 'fail', 'message': 'User does not have enough permissions'}, status=status.HTTP_403_FORBIDDEN)

class get_users(APIView):

    def get(self, request):
        user = User.objects.filter(username=request.user)[0]
        if user.is_superuser == True:
            user_all = User.objects.all()
            all_username = [user.username for user in user_all]
            return JsonResponse({'usernames': all_username})
        else:
            return JsonResponse({'staus': 'fail', 'message': 'User does not have enough permissions'}, status=status.HTTP_403_FORBIDDEN)
