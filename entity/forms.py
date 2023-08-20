from django import forms

from .models import Person


##########
# Person #
##########
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "other_names",
            "birth_date",
            "birth_place",
            "death_date",
            "death_place",
            "wikipedia",
            "website",
            "note",
        ]
        help_texts = {
            "name": "Enter the person's most-used name in their original language. ",
            "other_names": "Enter any other names the person is known by, separated by slashes (`/`).",
            "birth_date": "Recommended formats: `YYYY`, `YYYY.MM` or `YYYY.MM.DD`.",
            "birth_place": "Enter the place of birth in its original language.",
            "wikipedia": "Enter the person's Wikipedia URL.",
            "website": "Enter the person's website URL.",
            "note": "Enter any additional information about the person.",
        }
        widgets = {
            "other_names": forms.TextInput(),  # Use TextInput to make it a single line input
        }
