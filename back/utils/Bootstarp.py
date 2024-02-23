from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.forms import widgets
from back import models


class BootstarpForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class']="form-control"
                field.widget.attrs['placeholder']=field.label
            else:
                field.widget.attrs = {
                    "class":"form-control",
                    "placeholder":field.label
                }