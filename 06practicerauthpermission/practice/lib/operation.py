from datetime import datetime, timezone


# Update only the fields that are provided in the request
# customFields = ["phone", "firstname", "lastname", "email"]
def updateOp(instance, request, customFields=None):
    if customFields:
        for field in customFields:
            if hasattr(request, field):
                value = getattr(request, field)
                if value is not None:
                    setattr(instance, field, value)
    else:
        data = request.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(instance, key, value)
    if hasattr(instance, "updated_at"):
        instance.updated_at = datetime.now(timezone.utc)
    return instance
