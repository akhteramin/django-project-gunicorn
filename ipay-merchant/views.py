from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect
import requests
import json
from ipaypos.settings import SERVICE_URL, HEADERS, IMAGE_BASE_URL,TRANSACTION_SERVICE_URL
from datetime import datetime
import subprocess
import os
import uuid

class IndexView(generic.ListView):
    template_name = 'ipay-merchant/index.html'

def login(request):
    return render(request, 'ipay-merchant/accounts.html')

def home(request):

    if 'token' in request.session:
        paramData = ''
        searchData= {}
        if request.POST:
            print(request.POST['dateRange'].split(' - '))
            dateRange = request.POST['dateRange'].split(' - ')
            start_datetime = datetime.strptime(dateRange[0], '%m/%d/%Y')
            end_datetime = datetime.strptime(dateRange[1], '%m/%d/%Y')
            # print(datetime_obj.date())
            print(str(unix_time_millis(start_datetime.date())))
            print(request.POST['searchText'])
            searchData = {
                            'dateRange': request.POST['dateRange'],
                            'searchText':request.POST['searchText']
            }
            startMs = str(int(unix_time_millis(start_datetime.date(),0)))
            endMs = str(int(unix_time_millis(end_datetime.date(),1)))
            searchText = request.POST['searchText']
            paramData = '&startMs='+startMs+'&endMs='+endMs+'&searchText='+searchText
        if 'dateRange' in request.GET or 'searchText' in request.GET:
            searchData = {
                'dateRange': request.GET['dateRange'],
                'searchText': request.GET.get('searchText','')
            }
            dateRange = request.GET['dateRange'].split(' - ')
            start_datetime = datetime.strptime(dateRange[0], '%m/%d/%Y')
            end_datetime = datetime.strptime(dateRange[1], '%m/%d/%Y')
            startMs = str(int(unix_time_millis(start_datetime.date(), 0)))
            endMs = str(int(unix_time_millis(end_datetime.date(), 1)))
            searchText = request.GET.get('searchText','')
            paramData = '&startMs=' + startMs + '&endMs=' + endMs + '&searchText=' + searchText

        outletDetails = request.session['outletDetails']
        HEADERS['token'] = request.session['token']
        limit=10
        pageNo = request.GET.get('page',1)
        print("page no",pageNo)
        limit= limit*int(pageNo)
        print("page no", limit)
        page = int(pageNo) + 1
        pageNo = str(page)
        response = requests.get(TRANSACTION_SERVICE_URL + 'money/pos/transaction-history?page=1&limit='+str(limit)+paramData, headers=HEADERS)
        print(response.text)
        print(response.status_code)
        if response.status_code == 401:
            redirect('/accounts/logout')
        transactionData = response.json()

        return render(request, 'ipay-merchant/home.html',
                      {"outletDetails":outletDetails,
                       "mobileNumber": request.session['mobileNumber'],
                       "transactionData":transactionData,
                       "imageBaseURL":IMAGE_BASE_URL,
                       "pageNo": str(pageNo),
                       "searchData": searchData})
    else:
        return render(request, 'ipay-merchant/accounts.html')

def accounts(request):
    if request.POST and 'token' not in request.session:
        try:
            post_data = {'outletUserName': request.POST['merchantUsername'], 'password': request.POST['password'],
                         'merchantMobileNumber': '+88'+request.POST['mobileNumber']};
            response = requests.post(SERVICE_URL + 'outlet/sign-in', headers=HEADERS, data=json.dumps(post_data))
            print(response.text)
            print(response.status_code)
            print(response.headers.get('token'))
            if response.headers.get('token'):
                request.session['token']=response.headers.get('token')
                request.session['outletDetails'] = response.json()
                request.session['mobileNumber'] = '+88'+request.POST['mobileNumber']

            response.raise_for_status()
        except requests.exceptions.Timeout:
            return render(request, 'ipay-merchant/accounts.html', {"error": "Request Timeout. Please Try Again"})

        except requests.exceptions.TooManyRedirects:
            return render(request, 'ipay-merchant/accounts.html', {"error": "Too Many Redirection"})
        except requests.exceptions.HTTPError as err:
            responseMsg= response.json()
            return render(request, 'ipay-merchant/accounts.html', {"error": responseMsg['message']+".Please Try Again."})
    if 'token' in request.session:
        return redirect('/home')

    return render(request, 'ipay-merchant/accounts.html')

def details(request):
    if 'token' in request.session:

        return render(request, 'ipay-merchant/details.html')

def qrcode(request):
    if 'token' in request.session:
        return render(request, 'ipay-merchant/qrcode.html',
                  {"outletDetails": request.session['outletDetails'],
                   "mobileNumber": request.session['mobileNumber']})
    else:
        redirect('/accounts/logout')

def accountslogout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    request.session.modified = True
    return render(request, 'ipay-merchant/accounts.html')


def logout(request):
    return render(request, 'ipay-merchant/accounts.html')

def get_device_id():
    if 'nt' in os.name:
        return subprocess.Popen('dmidecode.exe -s system-uuid'.split())
    else:
        return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

# def check_service_permission(request,serviceID):
#     for permission in request.session['permissionList']:
#         if permission['serviceID']==serviceID:
#             return True
#     return False
epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt,dateStat=0):
    print(str(datetime.combine(dt, datetime.min.time())))
    print(str(datetime.combine(dt, datetime.max.time())))

    if dateStat == 1:
        dt = datetime.combine(dt, datetime.max.time())
    else:
        dt = datetime.combine(dt, datetime.min.time())
    check = dt.timestamp() * 1000
    print(str(check))

    cl= (dt - epoch).total_seconds() * 1000.0
    print(str(cl))
    #here 21600 has been subtracted since dev db is behind 6 hrs but for live it must retrieved

    return ((dt - epoch).total_seconds()-21600) * 1000.0