from django import forms
from DoctorsApp.calendar.models import Member

# Create Add Record Form
class AddRecordForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.widgets.TextInput(attrs={"placeholder":"Name", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.EmailInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    age = forms.CharField(required=True,widget=forms.widgets.NumberInput(attrs={"placeholder": "Age", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
    state = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
    zipcode = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")

    class Meta:
        model = Member
        exclude = ("doctor",)