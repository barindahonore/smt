from authentication.models import CustomUser
from django import forms

from citizen.models import Citizens, Kwimuka, Messages

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'province', 'district', 'sector', 'cell', 'village')

class NewMemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)

    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter name',
        'type': 'date'
    }))
    class Meta:
        model=Citizens
        fields = '__all__'
    
    def check_profile(self):
        picture = self.cleaned_data.get('profile_picture')

        if not picture:
            raise forms.ValidationError("Profile picture is required")
        return picture
    
    def save(self, commit=True):
        member = super(NewMemberForm, self).save(commit=False)
        if commit:
            member.save()
        return member
    

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['topic'].label = 'Impamvu'
        self.fields['message'].label = 'Ubutumwa'
        self.fields['urgent'].label = 'Birihutirwa'
        self.fields['purpose'].label = 'Ubwoko'
    class Meta:
        model=Messages
        fields = '__all__'
        exclude = ('sender', 'reply')
    
    def save(self, commit=True):
        message_obj = super(MessageForm, self).save(commit=False)
        if commit:
            message_obj.save()
        return message_obj
    
class KwimukaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
    class Meta:
        model=Kwimuka
        fields = ('isibo',)
    
    def save(self, commit=True):
        kwimuka_obj = super(KwimukaForm, self).save(commit=False)
        if commit:
            kwimuka_obj.save()
        return kwimuka_obj