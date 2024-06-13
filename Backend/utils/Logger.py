from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from users.models import CustomUser


class Logger():
    def logger(self):
        content_type = ContentType.objects.get_for_model(CustomUser)  # Replace MyModel with your model
        LogEntry.objects.create(
            content_type=content_type,
            object_id="fetch_kyc",  # Replace obj.id with the object's ID you want to log
            object_repr=str("kyc"),  # Replace str(obj) with the representation of the object
            action_flag=ADDITION,  # Change this flag based on the action: ADDITION, CHANGE, DELETION
            change_message='Fetch a kyc Records',  # Description or message for the log
            user=CustomUser.objects.first(),  # User responsible for the action
            action_time=timezone.now()  # Timestamp of the action
        )