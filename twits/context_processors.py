def likes_context(request):
    """
    Adds like status information to template context.
    """
    if request.user.is_authenticated:
        return {"user_liked_twits": request.user.liked_twits.values_list("id", flat=True)}
    return {"user_liked_twits": []}
