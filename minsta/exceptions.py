import django.db

class MinstaError(Exception):
    pass


class LoginRequiredError(MinstaError):
    pass


class ValidationError(MinstaError):
    def __init__(self, form):
        self.form = form


class FormError(MinstaError):
    def __init__(self, form):
        self.form = form


