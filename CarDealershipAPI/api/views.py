from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsManagerOrPostOnly

from .models import *
from .serializers import *

# Create your views here.
class CarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            make = request.GET.get('make')
            model = request.GET.get('model')
            year_min = request.GET.get('yearMin')
            year_max = request.GET.get('yearMax')
            milage_min = request.GET.get('milageMin')
            milage_max = request.GET.get('milageMax')
            engineType = request.GET.get('engineType')
            condition = request.GET.get('condition')
            color = request.GET.get('color')
            featured = request.GET.get('featured')
            newArrivals = request.GET.get('newArrivals')
            queryset = Car.objects.all()
            if make is not None:
                queryset = queryset.filter(carModel__carMake__name = make)
            if model is not None:
                queryset = queryset.filter(carModel__name = model)
            if year_min is not None:
                queryset = queryset.filter(year__gte = year_min)
            if year_max is not None:
                queryset = queryset.filter(year__lte = year_max)
            if milage_min is not None:
                queryset = queryset.filter(milage__gte = milage_min)
            if milage_max is not None:
                queryset = queryset.filter(milage__lte = milage_max)
            if engineType is not None:
                queryset = queryset.filter(engineType__name = engineType)
            if condition is not None:
                queryset = queryset.filter(condition__name = condition)
            if color is not None:
                queryset = queryset.filter(color__name = color)
            if featured is not None:
                queryset = queryset.filter(featured = featured)
            if newArrivals:
                queryset = queryset.order_by('-id')[:10]
            serializedQueryset = CarSerializer(queryset, many = True).data
            return Response(serializedQueryset, status = status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
    def post(self, request,*args, **kwargs):
        userGroups = request.user.groups.values_list('name',flat = True)
        if 'Manager' in userGroups:
            try:
                data = request.data
                carModelInstance = CarModel.objects.get(name = data['carModel'])
                engineTypeInstance = EngineType.objects.get(name = data['engineType'])
                conditionInstance = Condition.objects.get(name = data['condition'])
                colorInstance = Color.objects.get(name = data['color'])
                carInstance = Car.objects.create(
                    carModel = carModelInstance,
                    year = data['year'],
                    milage = data['milage'],
                    engineType = engineTypeInstance,
                    condition = conditionInstance,
                    color = colorInstance,
                    featured = data['featured']
                )
                return Response({'message': carInstance.id}, status = status.HTTP_201_CREATED)
            except Exception as e:
                    return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized User'}, status = status.HTTP_401_UNAUTHORIZED)

class CarMakesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        carMakes = CarMake.objects.all()
        serializedData = CarMakeSerializer(carMakes, many = True).data
        return Response(serializedData, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        userGroups = request.user.groups.values_list('name',flat = True)
        if 'Manager' in userGroups:
            user = request.user
            data = request.data
            try:
                carMakeInstance = CarMake.objects.create(name = data['name'])
                return Response({'message': carMakeInstance.id}, status = status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized User'}, status = status.HTTP_401_UNAUTHORIZED)
        
class CarModelsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        make = request.GET.get('make')
        carModels = CarModel.objects.all()
        if make is not None:
            carModels = carModels.filter(carMake__name = make)
        serializedData = CarModelSerializer(carModels, many = True).data
        return Response(serializedData, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        userGroups = request.user.groups.values_list('name',flat = True)
        if 'Manager' in userGroups:
            user = request.user
            data = request.data
            try:
                carMakeInstance = CarMake.objects.get(name = data['carMake'])
                carModelInstance = CarModel.objects.create(name = data['name'], carMake = carMakeInstance)
                return Response({'message': carModelInstance.id}, status = status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unauthorized User'}, status = status.HTTP_401_UNAUTHORIZED)
        
class MessagesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManagerOrPostOnly]

    def get(self, request, *args, **kwargs):
        try:
            carID = request.GET.get('car')
            queryset = Message.objects.all()
            if carID is not None:
                queryset = queryset.filter(car__id = carID)
            serializedData = MessageSerializer(queryset, many = True).data
            return Response(serializedData, status = status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'haha'}, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        carInstance = None
        try:
            if data['carID']:
                carInstance = Car.objects.get(pk = data['carID'])
            messageInstance = Message.objects.create(
                firstName = data['firstName'],
                lastName = data['lastName'],
                email = data['email'],
                subject = data['subject'],
                body = data['body'],
                car = carInstance
                )
            return Response({'message': messageInstance.id}, status = status.HTTP_201_CREATED)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            messageInstance = Message.objects.get(pk = data['id'])
            if data['addressed'] is not None:
                messageInstance.addressed = data['addressed']
            messageInstance.save()
            return Response({'message': f'message {messageInstance.id} successfully updated'}, status = status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
class ColorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            colors = Color.objects.all()
            serializedColors = ColorSerializer(colors, many = True).data
            return Response(serializedColors, status = status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
class ConditionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            conditions = Condition.objects.all()
            serializedConditions = ConditionSerializer(conditions, many = True).data
            return Response(serializedConditions, status = status.HTTP_200_OK)
        except Exception as e:
                return Response({'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)