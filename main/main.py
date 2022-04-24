from . import models
import json
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from main.catalogue.connector import CONNECTOR
from mysql.connector import connect, Error

def updateJson(current, value, update=False):
    status = 'insert'
    if(current == None):
        if(value != None or value != ''):
            if(len(value) >= 1):
                data = json.dumps(value); status = True
            else: data = None; status = False
        else: data = None; status = False
    else:
        if(value != None or value != ''):
            if(len(value) >= 1):
                current = json.loads(current)
                if(not update):
                    ins = current + value
                else:
                    value_id = value[0]['id']
                    left_bound = value[0]['left_bound']
                    data_layer = value[0]['data_layer']
                    counter = 0
                    for val in current:
                        for key in val:
                            if(key == 'id'):
                                if(val[key] == value_id):
                                    current[counter]['left_bound'] = left_bound
                                    current[counter]['data_layer'] = data_layer
                        counter += 1
                    ins = current
                data = json.dumps(ins)
                status = True
            else: data = None; status = False
        else: data = None; status = False
    return {
        'data': data,
        'status': status
    }

def updateAllocations(id, value):
    a = models.Auctions.objects.get(Pid = id)
    current = a.allocations
    new = updateJson(current, value)
    if(new['status']):
        a.allocations = new['data']
        a.save()
        return True
    else: return False
    
def updateSales(id, value):
    a = models.Auctions.objects.get(Pid = id)
    current = a.sales
    new = updateJson(current, value)
    if(new['status']):
        a.sales = new['data']
        a.save()
        return True
    else: return False

def updateCatalogue(id, value):
    a = models.Auctions.objects.get(Pid = id)
    current = a.catalogue
    new = updateJson(current, value)
    if(new['status']):
        a.catalogue = new['data']
        a.save()
        return True
    else: return False

def updateInvoices(id, value):
    print(id)
    a = models.Auctions.objects.get(Pid = id)
    current = a.invoices
    new = updateJson(current, value)
    if(new['status']):
        a.invoices = new['data']
        a.save()
        return True
    else: return False
    
def updateAccountSales(id, value):
    print(id)
    a = models.Auctions.objects.get(Pid = id)
    current = a.account_sales
    new = updateJson(current, value)
    if(new['status']):
        a.account_sales = new['data']
        a.save()
        return True
    else: return False

def updateInvoiceData(id, value):
    folder='media/documents/invoice_data/'
    fs = FileSystemStorage(location=folder)
    a = models.Auctions.objects.get(Pid = id)
    filename = 'InvoiceData_' + str(int(datetime.timestamp(datetime.now()))) + '.json'
    a.invoice_data = filename
    a.save()
    with fs.open(filename, 'w') as outfile:
        json.dump(value, outfile, indent=4, default=str)
        
def updateAccountSaleData(id, value):
    folder='media/documents/account_sale_data/'
    fs = FileSystemStorage(location=folder)
    a = models.Auctions.objects.get(Pid = id)
    filename = 'AccountSaleData_' + str(int(datetime.timestamp(datetime.now()))) + '.json'
    a.account_sale_data = filename
    a.save()
    with fs.open(filename, 'w') as outfile:
        json.dump(value, outfile, indent=4, default=str)
        
def updateCatalogueData(id, value):
    folder='media/documents/catalogue_data/'
    fs = FileSystemStorage(location=folder)
    a = models.Auctions.objects.get(Pid = id)
    filename = 'CatalogueData_' + str(int(datetime.timestamp(datetime.now()))) + '.json'
    a.catalogue_data = filename
    a.save()
    with fs.open(filename, 'w') as outfile:
        json.dump(value, outfile, indent=4, default=str)
    
def updateSingleAllocation(id, value):
    a = models.Auctions.objects.get(Pid = id)
    current = a.allocations
    new = updateJson(current, value, True)
    if(new['status']):
        a.allocations = new['data']
        a.save()
        return True
    else: return False

def updateSingleSale(id, value):
    a = models.Auctions.objects.get(Pid = id)
    current = a.sales
    new = updateJson(current, value, True)
    if(new['status']):
        a.sales = new['data']
        a.save()
        return True
    else: return False
    
def updateMarksOrder(new):
    a = models.MarksOrder.objects.get(name = "marks_order")
    a.order = new
    if a.save():
        return True
    else: return False

def getCurrentLot():
    try:
        with connect(**CONNECTOR) as connection:
            current_lot = '''SELECT `number` FROM `lot_number`'''
            with connection.cursor() as cursor:
                cursor.execute(current_lot)
                row = cursor.fetchone()
                return row[0]
    except Error as e:
            print(e)
            
def updateLot(lot_number):
    try:
        with connect(**CONNECTOR) as connection:
            update_lot = '''UPDATE `lot_number` SET `number` = %s'''
            with connection.cursor() as cursor:
                cursor.execute(update_lot, (lot_number,))
                connection.commit()
    except Error as e:
            print(e)