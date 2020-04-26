from django.db import models
from django.conf import settings


REASON_CHOICES = (
    ('Copyright', 'Copyright'),
    ('Obscene', 'Obscene'),
    ('Offensive', 'Offensive'),
)


# Create your models here.
class Flag(models.Model):
    # flagger
    flagger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="flag_flagger")
    # flagdate
    flagdate = models.DateTimeField(auto_now_add=True, editable=False)

    reason = models.CharField(max_length=10, choices = REASON_CHOICES, default = 'Copyright')
    justification = models.CharField(max_length=305, default="")

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="flag_reviewer")
    reviewercomment = models.CharField(max_length=305, default="", null=True, blank=True)
    overturned = models.BooleanField(default=False)
    updated = models.DateField(auto_now=True, editable=False)

    def __str__(self):
        if self.flagger:
            return str(self.pk) + " - " + self.flagger.username + " - " + self.reason + ": " + self.justification
        else:
            return str(self.pk) + " - widowed - " + self.reason + ": " + self.justification

