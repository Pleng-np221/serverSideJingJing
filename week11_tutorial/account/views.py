# from django.http import HttpResponse
# from django.shortcuts import render

# from account.models import Account

# # Create your views here.
# def transfer(request):
#     from_account_no = request.GET.get("from_account_no")
#     to_account_no = request.GET.get("to_account_no")
#     amount = request.GET.get("amount")

#     from_acc = Account.objects.get(account_no=from_account_no)

#     from_acc.transfer_funds(to_account_no=to_account_no, amount=amount)

#     return HttpResponse("SUCCESS")

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from account.forms import DocumentForm

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })