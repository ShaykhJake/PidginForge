from django.contrib import admin
from events.models import (
                     CalendarEvent, 
                     UserInvite, 
                     EventRSVP, 
                     EventAttendee, 
                     EventComment, 
                     CommentReply,
                     )


admin.site.register(CalendarEvent)
admin.site.register(UserInvite)
admin.site.register(EventRSVP)
admin.site.register(EventAttendee)
admin.site.register(EventComment)
admin.site.register(CommentReply)