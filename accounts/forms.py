from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username','description','photo', 'github_url')
        help_texts = {
            'username': None,
        }
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3})}
