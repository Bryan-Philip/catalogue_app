from datetime import datetime, date
from email.headerregistry import ContentTypeHeader
from turtle import update
from django.http import HttpResponse
from h11 import Data
from main.models import Auctions, MarksOrder
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .main import *
import os
import json
from django.core.files.storage import FileSystemStorage
from django.utils.dateformat import DateFormat
from django.views.generic import DetailView
from main.catalogue.invoice import INVOICEGENERATOR
from main.catalogue.interpret import GENERATECATALOGUE
from main.catalogue.account_sale import ACCOUNTSALEGENERATOR
import zipfile
import os
import zipfile
from io import StringIO, BytesIO
from django.http import HttpResponse
import random

@ensure_csrf_cookie
def upload_allocations(request):
    file_list = list()
    if request.method == "GET":
        return render(request, 'auctions/upload_allocations.html', )
    if request.method == 'POST':
        values = request.POST
        files = request.FILES.getlist('files[]', None)
        counter = 0
        for f in files:
            fname = ( str(int(datetime.timestamp(datetime.now()))) + '_' + f.name )
            handle_uploaded_allocations(f, fname)
            file_list.append({
                'name': fname,
                'data_layer': 4,
                'left_bound': 3,
                'id': str(counter) + '_' + str(int(datetime.timestamp(datetime.now()))),
                'timestamp': int(datetime.timestamp(datetime.now())),
                'date': DateFormat(date.today()).format("jS M, Y"),
                'date_slash': DateFormat(date.today()).format("j/m/Y"),
            })
            counter += 1
            print(updateAllocations(values['auction-id'], file_list))
        return JsonResponse({'msg_allocations': '''
                                <span id="message-allocations" style="color: green;">File(s) successfully uploaded</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-allocations').slideUp("swing")
                                        }, 2000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/upload_allocations.html', )

@ensure_csrf_cookie
def upload_sale(request):
    if request.method == "GET":
        return render(request, 'auctions/upload_sale.html', )
    if request.method == 'POST':
        values = request.POST
        file = request.FILES['file']
        fname = ( str(int(datetime.timestamp(datetime.now()))) + '_' + file.name )
        handle_uploaded_sale(file, fname)
        file_data = {
            'name': fname,
            'data_layer': 4,
            'left_bound': 1,
            'id': '0_' + str(int(datetime.timestamp(datetime.now()))),
            'timestamp': int(datetime.timestamp(datetime.now())),
            'date': DateFormat(date.today()).format("jS M, Y"),
            'date_slash': DateFormat(date.today()).format("j/m/Y"),
        }
        print(updateSales(values['auction-id'], [file_data,]))
        return JsonResponse({'msg_sale': '''
                                <span id="message-sale" style="color: green;">File successfully uploaded</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-sale').slideUp("swing")
                                        }, 2000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/upload_sale.html', )
    
@ensure_csrf_cookie
def update_allocation(request):
    if request.method == "GET":
        return render(request, 'auctions/update_allocation.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = {
            'data_layer': values['data_layer'],
            'left_bound': values['left_bound'],
            'id': values['id'],
        }
        print(updateSingleAllocation(values['auction-id'], [file_data,]))
        return JsonResponse({'msg_allocation': '''
                                <span id="message-allocation" style="color: green;">File data successfully updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-allocation').slideUp("swing")
                                        }, 2000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/update_allocation.html', )
    
@ensure_csrf_cookie
def update_sale(request):
    if request.method == "GET":
        return render(request, 'auctions/update_sale.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = {
            'data_layer': values['data_layer'],
            'left_bound': values['left_bound'],
            'id': values['id'],
        }
        print(updateSingleSale(values['auction-id'], [file_data,]))
        return JsonResponse({'msg_sale': '''
                                <span id="message-sale" style="color: green;">File data successfully updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-sale').slideUp("swing")
                                        }, 2000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/update_sale.html', )
    
@ensure_csrf_cookie
def update_lot_number(request):
    if request.method == "GET":
        return render(request, 'auctions/update_lot_number.html', )
    if request.method == 'POST':
        values = request.POST
        updateLot(values['lot_number'])
        return JsonResponse({'msg_sale': '''
                                <span id="message-sale" style="color: green;">Lot number successfully updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-sale').slideUp("swing")
                                        }, 2000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/update_sale.html', )


def handle_uploaded_allocations(f, filename):
    folder='media/documents/allocations/'
    fs = FileSystemStorage(location=folder)
    fs.save(filename, f)

def handle_uploaded_sale(f, filename):
    folder='media/documents/sales/'
    fs = FileSystemStorage(location=folder)
    fs.save(( str(int(datetime.timestamp(datetime.now()))) + '_' + f.name ), f)
        
class AuctionData:
    def auction_years():
        auctions = Auctions.objects.all()
        years = list()
        for auction in auctions:
            years.append(auction.year)
        years = set(years)
        years_relation = dict()
        years_data = dict()
        for year in years:
            years_relation[year] = list()
            years_data[year] = dict()
        for year in years:
            for auction in auctions:
                inner = {
                    'id': auction.Pid,
                    'number': auction.number,
                    'date': auction.date,
                    'allocations': auction.allocations,
                    'catalogue': auction.catalogue,
                    'invoices': auction.invoices,
                    'closing_date': auction.catalogue_closing_date,
                    'prompt_date': auction.prompt_date,
                    'year': auction.year,
                    'sales': auction.sales,
                    'catalogue_data': auction.catalogue_data,
                    'invoice_data': auction.invoice_data,
                    'invoice_number': auction.invoice_number,
                    'account_sales': auction.account_sales,
                    'account_sale_data': auction.account_sale_data,
                    'account_sale_number': auction.account_sale_number,
                }
                if auction.year == year:
                    years_relation[year].append(inner)

        for year in years_relation:
            years_data[year]['auctions'] = len(years_relation[year])
            years_data[year]['data'] = years_relation[year]
        
        return {
            'years': years,
            'years_relation': years_relation,
            'years_data': years_data
        }
    def get_single_auction_year(self):
        return self.auction_years()

class MarksData:
    def order_data():
        order = MarksOrder.objects.get(name="marks_order")
        print(type(order))
        return {
            'order': order.order,
        }

def auction_years(request):
    return render(
        request,
        'auctions/home.html',
        {'years': AuctionData.auction_years()['years_data']}
    )

def auctions_display(request, year):
    return render(
        request,
        'auctions/year_auctions.html',
        {
            'auctions': AuctionData.auction_years()['years_relation'][str(year)],
            'year': year,
        }
    )

def auction_view(request, year, number):
    for auction in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auction['number'] == str(number):
            auction_data = auction
            break
        else: auction_data = None
    return render(
        request,
        'auctions/auction.html',
        {
            'auction': AuctionData.auction_years()['years_data'][str(year)],
            'year': year,
            'number': number,
            'data': auction_data,
        }
    )

def generate_catalogue(request, year, number):
    for auction in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auction['number'] == str(number):
            auction_data = auction
            for val in auction_data:
                if(val == 'allocations'):
                    if(auction_data[val] != None):
                        auction_data['allocations'] = json.loads(auction_data[val])
                if(val == 'catalogue'):
                    if(auction_data[val] != None):
                        auction_data['catalogue'] = json.loads(auction_data[val])
                if(val == 'invoices'):
                    if(auction_data[val] != None):
                        auction_data['invoices'] = json.loads(auction_data[val])
                if(val == 'sales'):
                    if(auction_data[val] != None):
                        auction_data['sales'] = json.loads(auction_data[val])
            break
        else: auction_data = None
    lot = getCurrentLot()
    return render(
        request,
        'auctions/generate_catalogue.html',
        {
            'auction': AuctionData.auction_years()['years_data'][str(year)],
            'year': year,
            'number': number,
            'data': auction_data,
            'lot_number': lot,
        }
    )
def generate_invoices(request, year, number):
    for auction in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auction['number'] == str(number):
            auction_data = auction
            for val in auction_data:
                if(val == 'allocations'):
                    if(auction_data[val] != None):
                        auction_data['allocations'] = json.loads(auction_data[val])
                if(val == 'catalogue'):
                    if(auction_data[val] != None):
                        auction_data['catalogue'] = json.loads(auction_data[val])
                if(val == 'invoices'):
                    if(auction_data[val] != None):
                        auction_data['invoices'] = json.loads(auction_data[val])
                if(val == 'sales'):
                    if(auction_data[val] != None):
                        auction_data['sales'] = json.loads(auction_data[val])
            break
        else: auction_data = None
    if(auction_data != None):
        currentdate = date.today()
        sale_date = currentdate.strftime("%d/%m/%y")
        sale_date_format = DateFormat(currentdate).format("jS M, Y")
        prompt_date = DateFormat(auction_data['prompt_date']).format("j/m/Y")
        prompt_date_format = DateFormat(auction_data['prompt_date']).format("jS M, Y")
    else:
        sale_date = None
        sale_date_format = None
        prompt_date = None
        prompt_date_format = None
    return render(
        request,
        'auctions/generate_invoices.html',
        {
            'auction': AuctionData.auction_years()['years_data'][str(year)],
            'year': year,
            'number': number,
            'data': auction_data,
            'sale_date': sale_date,
            'sale_date_format': sale_date_format,
            'prompt_date': prompt_date,
            'prompt_date_format': prompt_date_format,
            'catalogue_data': auction_data['catalogue_data'],
            'invoice_data': auction_data['invoice_data'],
            'invoice_number': auction_data['invoice_number'],
        }
    )
def generate_account_sales(request, year, number):
    for auction in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auction['number'] == str(number):
            auction_data = auction
            for val in auction_data:
                if(val == 'allocations'):
                    if(auction_data[val] != None):
                        auction_data['allocations'] = json.loads(auction_data[val])
                if(val == 'catalogue'):
                    if(auction_data[val] != None):
                        auction_data['catalogue'] = json.loads(auction_data[val])
                if(val == 'invoices'):
                    if(auction_data[val] != None):
                        auction_data['invoices'] = json.loads(auction_data[val])
                if(val == 'sales'):
                    if(auction_data[val] != None):
                        auction_data['sales'] = json.loads(auction_data[val])
                if(val == 'account_sales'):
                    if(auction_data[val] != None):
                        auction_data['account_sales'] = json.loads(auction_data[val])
            break
        else: auction_data = None
    if(auction_data != None):
        currentdate = date.today()
        sale_date = currentdate.strftime("%d/%m/%y")
        sale_date_format = DateFormat(currentdate).format("jS M, Y")
        prompt_date = DateFormat(auction_data['prompt_date']).format("j/m/Y")
        prompt_date_format = DateFormat(auction_data['prompt_date']).format("jS M, Y")
    else:
        sale_date = None
        sale_date_format = None
        prompt_date = None
        prompt_date_format = None
    return render(
        request,
        'auctions/generate_account_sales.html',
        {
            'auction': AuctionData.auction_years()['years_data'][str(year)],
            'year': year,
            'number': number,
            'data': auction_data,
            'sale_date': sale_date,
            'sale_date_format': sale_date_format,
            'prompt_date': prompt_date,
            'prompt_date_format': prompt_date_format,
            'catalogue_data': auction_data['catalogue_data'],
            'account_sale_data': auction_data['account_sale_data'],
            'account_sale_number': auction_data['account_sale_number'],
        }
    )
    
@ensure_csrf_cookie
def marks_order(request):
    if request.method == "GET":
        return render(
            request,
            'marks_order.html',
            {'order': MarksData.order_data()['order']}
        )
    if request.method == 'POST':
        values = request.POST
        new_order = values['order']
        updateMarksOrder(new_order)
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;" class="text-sm">Order of marks updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(
            request,
            'marks_order.html',
            {'order': MarksData.order_data()['order']}
        )

    
### Generators

def last2(s):
    s = str(s)
    length = len(s)
    val = ''
    counter = 0
    for v in s:
        if(counter >= length-2):
            val += s[counter]
        counter += 1
    return val

@ensure_csrf_cookie
def generate_catalogue_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_catalogue.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = json.loads(values['data'])
        init_marks_order = json.loads(MarksData.order_data()['order'])
        marks_order = list()
        for mark in init_marks_order:
            if init_marks_order[mark] == 1:
                marks_order.append(mark)
        print(marks_order)
        r = str(int(random.uniform(100, 800)))
        GENERATE_CATALOGUE(
            file_data,
            str(int(datetime.timestamp(datetime.now())))+r,
            values['auction_id'],
            marks_order,
        )
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;">Catalogue Successfully Generated. Reload to sync changes.</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_catalogue.html', )

@ensure_csrf_cookie
def generate_invoices_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_invoices.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = json.loads(values['data'])
        print(values['auction_id'] + '-' + last2(values['auction_year']))
        GENERATE_INVOICES(file_data, {
            'sale_date': values['sale_date'],
            'prompt_date': values['prompt_date'],
            'auction_number': values['auction_id'] + '-' + last2(values['auction_year']),
            'auction_number_full': values['auction_year'] + '/' + values['auction_id'],
            'catalogue_data': values['catalogue_data'],
            'invoice_data': values['invoice_data'],
            'invoice_number': values['invoice_number'],
            'auction_Pid': values['auction_Pid'],
        }, values['auction_Pid'])
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;">Invoices Successfully Generated. Reload to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_invoices.html', )
    
@ensure_csrf_cookie
def generate_account_sales_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_account_sales.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = json.loads(values['data'])
        print(file_data)
        print(values['auction_id'] + '-' + last2(values['auction_year']))
        GENERATE_ACCOUNT_SALES(file_data, {
            'sale_date': values['sale_date'],
            'prompt_date': values['prompt_date'],
            'auction_number': values['auction_id'] + '-' + last2(values['auction_year']),
            'auction_number_alt': str(values['auction_year']) + '/' + values['auction_id'],
            'auction_number_0': str(values['auction_year']) + '/' + str(0) + values['auction_id'],
            'catalogue_data': values['catalogue_data'],
            'account_sale_data': values['account_sale_data'],
            'account_sale_number': values['account_sale_number'],
            'auction_Pid': values['auction_Pid'],
        }, values['auction_Pid'])
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;">Account Sale Successfully Generated. Reload to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_account_sales.html', )

@ensure_csrf_cookie
def download_zipped(request):
    if request.method == "POST":
        folder='media/documents/invoices/'
        
        values = request.POST
        files = json.loads(values['files'])
        filename = values['filename']
                        
        zip_subdir = filename
        zip_filename = "%s.zip" % zip_subdir

        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in files:
            fullpath = folder + fpath
            dir, fname = os.path.split(fullpath)
            
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fullpath, zip_path)

        zf.close()
        
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

def GENERATE_INVOICES(data, custom, id):    
    retdata = INVOICEGENERATOR(data, custom)
    dirs = retdata['dirs']
    dirs_alt = retdata['dirs_alt']
    if len(dirs) >= 1 and len(dirs) >= 1:
        return_data = [{
            "date": DateFormat(date.today()).format("jS M, Y"),
            "files": dirs,
            "files_alt": dirs_alt,
        }]
        try:
            updateInvoices(id, return_data)
            return True
        except:
            return False
    else:
        return False

def GENERATE_ACCOUNT_SALES(data, custom, id):    
    retdata = ACCOUNTSALEGENERATOR(data, custom)
    dirs = retdata['dirs']
    if len(dirs) >= 1 and len(dirs) >= 1:
        return_data = [{
            "date": DateFormat(date.today()).format("jS M, Y"),
            "files": dirs
        }]
        try:
            # updateAccountSales(id, return_data)
            return True
        except:
            return False
    else:
        return False

def GENERATE_CATALOGUE(data, custom, id, marks_order):
    dir = GENERATECATALOGUE(data, custom, marks_order)
    if dir:
        return_data = [{
            "date": DateFormat(date.today()).format("jS M, Y"),
            "file": dir['filename']
        }]
        try:
            updateCatalogue(id, return_data)
            updateCatalogueData(id, dir['catalogue_data'])
            updateInvoiceData(id, dir['invoice_data'])
            updateAccountSaleData(id, dir['account_sale_data'])
            return True
        except:
            return False
    else:
        return False


# Display File

class EmpImageDisplay(DetailView):
    template_name = 'display_catalogue.html'
    context_object_name = 'emp'