from django.shortcuts import render
from Analyze.forms import UploadFileForm
from Analyze.models import UploadedFile
import pandas as pd
def upload_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            df = pd.read_excel(uploaded_file.file.path)
            column_types = {
                'numeric': df.select_dtypes(include=['number']).columns.tolist(),
                'categorical': df.select_dtypes(include=['object']).columns.tolist(),
                'datetime': df.select_dtypes(include=['datetime']).columns.tolist(),
            }

            return render(request, 'file.html', {
                'column_types': column_types,
                'filename': uploaded_file.file.name,
                'df_head': df.head().to_html()
            })
    else:
        form = UploadFileForm()

    return render(request, 'file.html', {'form': form})
