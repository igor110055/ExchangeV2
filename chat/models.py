from django.db import models

from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def deserialize_user(user):
    """Deserialize user instance to JSON."""
    return {
        'id': user.id, 'username': user.username, 'email': user.email,
        'first_name': user.first_name, 'last_name': user.last_name
    }


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def _generate_unique_uri():
    """Generates a unique uri for the chat session."""
    return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
    """ A Chat Session. The uri's are generated by taking the first 15 characters from a UUID """

    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    uri = models.URLField(default=_generate_unique_uri)

    def get_user(self):
        if self.owner:
            return self.owner.username
        return ''
    def get_seen(self):
        notseen = 0
        for item in self.messages.all():
            if not item.aseen:
                notseen = notseen + 1
        return notseen

class ChatSessionMessage(TrackableDateModel):
    """Store messages for a session."""

    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete=models.CASCADE
    )
    message = models.TextField(max_length=2000)
    seen = models.BooleanField(default=False)
    aseen = models.BooleanField(default=False)

    def to_json(self):
        """deserialize message to JSON."""
        if self.email :
            return {'user': self.email, 'message': self.message}
        return {'user': deserialize_user(self.user), 'message': self.message}