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
from main.catalogue.warehouse_confirmation import WHCONFIRMATIONGENERATOR
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
        auctions = Auctions.objects.all().order_by('Pid')
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
                    'warehouse_confirmations': auction.warehouse_confirmations,
                    'warehouse_confirmation_data': auction.warehouse_confirmation_data,
                    'warehouse_confirmation_number': auction.warehouse_confirmation_number,
                    'outlots': auction.outlots,
                }
                if auction.year == year:
                    years_relation[year].append(inner)

        for year in years_relation:
            # years_relation[year] = sorted()
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
    for auct in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auct['number'] == number:
            __id = auct['id']
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
            'id_': __id
        }
    )
def generate_invoices(request, year, number):
    sales_list = list()
    cleanup_list = list()
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
                        for invoice in json.loads(auction_data[val]):
                            if 'sale_id' in invoice:
                                sales_list.append(invoice['sale_id'])
                            else:
                                cleanup_list.append(invoice)
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
    for auct in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auct['number'] == number:
            __id = auct['id']
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
            'sales_list': sales_list,
            'cleanup_list': cleanup_list,
            'id_': __id
        }
    )
def generate_account_sales(request, year, number):
    sales_list = list()
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
    for auct in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auct['number'] == number:
            __id = auct['id']

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
            'sales_list': sales_list,
            'id_': __id
        }
    )
    
def generate_warehouse_confirmations(request, year, number):
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
                if(val == 'warehouse_confirmations'):
                    if(auction_data[val] != None):
                        auction_data['warehouse_confirmations'] = json.loads(auction_data[val])
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
    for auct in AuctionData.auction_years()['years_data'][str(year)]['data']:
        if auct['number'] == number:
            __id = auct['id']
    return render(
        request,
        'auctions/generate_warehouse_confirmations.html',
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
            'warehouse_confirmation_data': auction_data['warehouse_confirmation_data'],
            'warehouse_confirmation_number': auction_data['warehouse_confirmation_number'],
            'id_': __id
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

@ensure_csrf_cookie
def update_invoice_number(request):
    if request.method == "GET":
        return render(
            request,
            'update_invoice_number.html',
        )
    if request.method == 'POST':
        values = request.POST
        auction_id = values['auction_id']
        value = values['value']
        updateInvoiceNumber(auction_id, value)
        return JsonResponse({'msg': '''
                                <span id="message-dataI" style="color: green;" class="text-md text-center">Invoice Number updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-dataI').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            ''', 'value': value})
    else:
        return render(
            request,
            'update_invoice_number.html',
        )

@ensure_csrf_cookie
def update_account_sale_number(request):
    if request.method == "GET":
        return render(
            request,
            'update_account_sale_number.html',
        )
    if request.method == 'POST':
        values = request.POST
        auction_id = values['auction_id']
        value = values['value']
        updateAccountSaleNumber(auction_id, value)
        return JsonResponse({'msg': '''
                                <span id="message-dataA" style="color: green;" class="text-md text-center">Account Sale Number updated</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-dataA').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            ''', 'value': value})
    else:
        return render(
            request,
            'update_account_sale_number.html',
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
        reprint_placement = values['reprint_placement']
        init_marks_order = json.loads(MarksData.order_data()['order'])
        marks_order = list()
        for mark in init_marks_order:
            if init_marks_order[mark] == 1:
                marks_order.append(mark)
        print(marks_order)
        print("reprint_placement")
        print(reprint_placement)
        r = str(int(random.uniform(100, 800)))
        GENERATE_CATALOGUE(
            file_data,
            str(int(datetime.timestamp(datetime.now())))+r,
            values['auction_id'],
            marks_order,
            reprint_placement,
        )
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;" class="mb-2 block text-center">Catalogue Successfully Generated. <strong>Auto-reloading</strong> to sync changes.</span>
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
                                <span id="message-data" style="color: green;" class="mb-2 block text-center">Invoices Successfully Generated. <strong>Auto-reloading</strong> to sync changes</span>
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
        GENERATE_ACCOUNT_SALES(file_data, {
            'sale_date': values['sale_date'],
            'prompt_date': values['prompt_date'],
            'auction_number': values['auction_id'] + '-' + last2(values['auction_year']),
            'auction_number_alt': str(values['auction_year']) + '/' + values['auction_id'],
            'auction_number_0': str(last2(values['auction_year'])) + '/' + str(0) + values['auction_id'],
            'catalogue_data': values['catalogue_data'],
            'account_sale_data': values['account_sale_data'],
            'account_sale_number': values['account_sale_number'],
            'auction_Pid': values['auction_Pid'],
            'auction_date_title': values['auction_date_title'],
            'auction_year': values['auction_year'],
            '_auction_number': values['auction_id'],
        }, values['auction_Pid'])
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;" class="mb-2 block text-center">Account Sales Successfully Generated. <strong>Auto-reloading</strong> to sync changes</span>
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
def generate_warehouse_confirmations_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_warehouse_confirmations.html', )
    if request.method == 'POST':
        values = request.POST
        file_data = json.loads(values['data'])
        print(file_data)
        print(values['auction_id'] + '-' + last2(values['auction_year']))
        GENERATE_WAREHOUSE_CONFIRMATIONS(file_data, {
            'sale_date': values['sale_date'],
            'prompt_date': values['prompt_date'],
            'auction_number': values['auction_id'] + '-' + last2(values['auction_year']),
            'auction_number_alt': str(values['auction_year']) + '/' + values['auction_id'],
            'auction_number_0': str(values['auction_year']) + '/' + str(0) + values['auction_id'],
            'catalogue_data': values['catalogue_data'],
            'warehouse_confirmation_data': values['warehouse_confirmation_data'],
            'warehouse_confirmation_number': values['warehouse_confirmation_number'],
            'auction_Pid': values['auction_Pid'],
        }, values['auction_Pid'])
        return JsonResponse({'msg': '''
                                <span id="message-data" style="color: green;" class="mb-2 block text-center">Warehouse Confirmations Successfully Generated. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_warehouse_confirmations.html', )
    
@ensure_csrf_cookie
def delete_catalogue_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_catalogue.html', )
    if request.method == 'POST':
        values = request.POST
        deleteCatalogueData(values['auction_id'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Catalogues Deleted. <strong>Auto-reloading</strong> to sync changes.</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_catalogue.html', )

@ensure_csrf_cookie
def delete_invoices_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_invoices.html', )
    if request.method == 'POST':
        values = request.POST
        deleteInvoiceData(values['auction_id'], values['sale_id'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Invoices Deleted. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_invoices.html', )

@ensure_csrf_cookie
def delete_all_invoices_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_invoices.html', )
    if request.method == 'POST':
        values = request.POST
        deleteInvoiceData(values['auction_id'], values['type'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Invoices Deleted. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_invoices.html', )
    
@ensure_csrf_cookie
def delete_account_sales_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_account_sales.html', )
    if request.method == 'POST':
        values = request.POST
        print(values)
        deleteAccountSaleData(values['auction_id'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Account Sales Deleted. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_account_sales.html', )

@ensure_csrf_cookie
def delete_all_account_sales_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_invoices.html', )
    if request.method == 'POST':
        values = request.POST
        deleteInvoiceData(values['auction_id'], values['type'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Invoices Deleted. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_invoices.html', )
    
@ensure_csrf_cookie
def delete_warehouse_confirmations_data(request):
    if request.method == "GET":
        return render(request, 'auctions/generate_warehouse_confirmations.html', )
    if request.method == 'POST':
        values = request.POST
        deleteWarehouseConfirmationData(values['auction_id'])
        return JsonResponse({'msg': '''
                                <span id="message-data2" style="color: green;" class="text-center">Warehouse Confirmations Deleted. <strong>Auto-reloading</strong> to sync changes</span>
                                <script>
                                    $(function(){
                                        setTimeout(() => {
                                            $('#message-data2').slideUp("swing")
                                        }, 5000)
                                    })
                                </script/>
                            '''})
    else:
        return render(request, 'auctions/generate_warehouse_confirmations.html', )

@ensure_csrf_cookie
def download_zipped(request, type):
    if request.method == "POST":
        if type == 'invoices':
            folder='media/documents/invoices/'
        elif type == 'account_sales':
            folder='media/documents/account_sales/'
        elif type == 'warehouse_confirmations':
            folder='media/documents/warehouse_confirmations/'
        else:
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
    outlot = retdata['outlot']
    if len(dirs) >= 1 and len(dirs) >= 1:
        return_data = [{
            "date": DateFormat(date.today()).format("jS M, Y"),
            "files": dirs,
            "files_alt": dirs_alt,
            "sale_id": data[0]['id'],
        }]
        try:
            updateInvoices(id, return_data)
            updateOutlots(outlot)
            updateAuctionOutlots(id, outlot)
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
            "files": dirs,
        }]
        try:
            updateAccountSales(id, return_data)
            return True
        except:
            return False
    else:
        return False

def GENERATE_CATALOGUE(data, custom, id, marks_order, reprint_placement):
    dir = GENERATECATALOGUE(data, custom, marks_order, reprint_placement)
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

def GENERATE_WAREHOUSE_CONFIRMATIONS(data, custom, id):    
    retdata = WHCONFIRMATIONGENERATOR(data, custom)
    dirs = retdata['dirs']
    if len(dirs) >= 1 and len(dirs) >= 1:
        return_data = [{
            "date": DateFormat(date.today()).format("jS M, Y"),
            "files": dirs
        }]
        try:
            # updateWarehouseConfirmations(id, return_data)
            return True
        except:
            return False
    else:
        return False

# Display File

class EmpImageDisplay(DetailView):
    template_name = 'display_catalogue.html'
    context_object_name = 'emp'