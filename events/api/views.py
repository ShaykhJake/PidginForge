from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action
from django.db.models import Q
from events.api.serializers import (
                           CalendarEventSerializer,
                           # EventSnippetSerializer,
                           RSVPSerializer,
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from events.models import (
                           CalendarEvent,
                           EventRSVP,
                           )

# ISINVITED CLASS?
# class IsCuratorOrReadOnly(permissions.BasePermission):
    
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.curator == request.user


class IsCuratorOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.curator == request.user

class IsInviteeOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.invited_user == request.user


class IsPublishedOrAuthorOnly(permissions.BasePermission):
    
   def has_object_permission(self, request, view, obj):
      if obj.curator == request.user:
         return True
      if obj.published == False and obj.curator is not request.user:
         return False

class RSVPViewSet(viewsets.ModelViewSet):
   queryset = EventRSVP.objects.all().order_by("-curationdate")
   lookup_field = "pk"
   serializer_class = RSVPSerializer
   permission_classes = [IsAuthenticated, IsInviteeOrReadOnly]

   # def create(self, serializer):
   #    serializer.save(invited_user=self.request.user)
   #    return Response(serializer.data, status=status.HTTP_200_OK)

   def perform_create(self, serializer):
      serializer.save(invited_user=self.request.user)
      if self.request.data.get('Attending') == 'Yes':
         self.request.user.user_profile.points += 3
         self.request.user.user_profile.save()
      else:
         self.request.user.user_profile.points += 1
         self.request.user.user_profile.save()
      return Response(serializer.data, status=status.HTTP_200_OK)


###### CALENDAR EVENT VIEWS #######
class CalendarEventViewSet(viewsets.ModelViewSet):

   queryset = CalendarEvent.objects.all().order_by("-curationdate")
   lookup_field = "slug"
   serializer_class = CalendarEventSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   def perform_create(self, serializer):
      serializer.save(curator=self.request.user)
      if self.request.data.get('parent_event') is None:
         self.request.user.user_profile.points += 10
         self.request.user.user_profile.save()
      else:
         self.request.user.user_profile.points += 2
         self.request.user.user_profile.save()
      # instance = serializer.data.get('slug')
      # for i in serializer.data.get('invited_users'):
      #    print(i)
      #    instance.invited_users.add(i)
      return Response(serializer.data, status=status.HTTP_200_OK)


   def partial_update(self, request, slug):
      print(request.data)
      event = get_object_or_404(CalendarEvent, slug=slug)
      serializer_context = {"request": request}
      serializer=CalendarEventSerializer(event, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
      updatedserializer=CalendarEventSerializer(event, context=serializer_context)
      return Response(updatedserializer.data)


   def list(self, request):
      """The first list will bring back all events for which the user
      is either invited for the event is listed as public, or..."""
      # userinvites = request.user.event_invited_user.all()
      queryset = CalendarEvent.objects.filter(Q(public = True) |
                                    Q(guest_list = request.user) |
                                    Q(curator = request.user)
                                    ).select_related(
                                       'curator__user_profile',
                                       'native_language',
                                       'target_language',
                                    ).prefetch_related(
                                       'guest_list',
                                       'rsvp'
                                    ).order_by("-start_datetime")

      serializer_context = { "request": request}
      
      serializer = CalendarEventSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)

   


