def updateOp(instance, request):
    data = request.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(instance, key, value)
    return instance
