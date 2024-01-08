from django.shortcuts import render
from django import forms
import pandas as pd


class UploadFileForm(forms.Form):
    file = forms.FileField()


def upload_schedule_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['file']
        data = pd.read_csv(file)
        # Process the data here, e.g., save it to your models
        return render(request, 'upload_success.html')  # Create this template
    # Create this template
    return render(request, 'upload.html', {'form': form})
