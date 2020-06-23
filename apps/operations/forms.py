import re

from django import forms
from apps.operations.models import UserFavorite


class UserFavForm(forms.Form):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]
