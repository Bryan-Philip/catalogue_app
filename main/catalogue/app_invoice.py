from datetime import datetime
import PySimpleGUI as sg
import shutil
import calendar
import time
from invoice import INVOICEGENERATOR

sg.theme('SandyBeach')

layout = [
    [sg.Text('Filename')],
    [sg.Input(), sg.FileBrowse()],
    [sg.Text('Left Bound', size=(14, 1)), sg.InputText()],
    [sg.Text('Title Layer', size=(14, 1)), sg.InputText()],
    [sg.Text('Prompt Date', size=(14, 1)), sg.InputText()],
    [sg.Text('Sale Date', size=(14, 1)), sg.InputText()],
    [sg.Text('Auction Number', size=(14, 1)), sg.InputText()],
    [sg.OK(button_text="submit", ), sg.Cancel()]
]

window = sg.Window(
    'Generate Invoice',
    layout,
    size=(600, 500),
    resizable=True,
    titlebar_background_color="black",
    titlebar_text_color="white"
)

event, values = window.read()
window.close()

if event == 'submit':
    file = values[0]
    left_bound = values[1]
    title_layer = values[2]
    prompt_date = values[3]
    sale_date = values[4]
    auction_number = values[5]
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    now = str(ts)
    dest = 'uploads/sales/' + now + '.xlsx'
    shutil.copy(file, dest)
    file = dest
    if(left_bound == None or left_bound == '' or title_layer == None or title_layer == '' or file == None or file == '' or prompt_date == None or prompt_date == '' or sale_date == '' or sale_date == None or auction_number == None or auction_number == ''):
        layout = [
            [sg.Text('Some values are missing')],
            [sg.OK(button_text="Ok",)]
        ]
        window = sg.Window(
            'Missing form values',
            layout,
            size=(600, 500),
            resizable=True,
            titlebar_background_color="black",
            titlebar_text_color="white"
        )
    else:
        try:
            print('Generating invoices...')
            INVOICEGENERATOR(input_data=[
                {
                    'left_bound': left_bound,
                    'data_layer': title_layer,
                    'file': file
                }
            ], custom_data={
                'prompt_date': prompt_date,
                'sale_date': sale_date,
                'auction_number': auction_number
            })
            layout = [
                [sg.Text('Invoices generated')],
                [sg.Text('Check the app root folder under the "invoices" subdirectory')],
                [sg.OK(button_text="Ok",)]
            ]
            window = sg.Window(
                'Generating Invoices...',
                layout,
                size=(600, 500),
                resizable=True,
                titlebar_background_color="black",
                titlebar_text_color="white"
            )
            print('Invoices Generated')
        except:
            print('An error occurred generating the invoices..')
            layout = [
                [sg.Text('An error occurred generating the invoices..')],
                 [sg.Text('Check the logs for more information')],
                [sg.OK(button_text="submit", )]
            ]
            window = sg.Window(
                'Generating Invoices...',
                layout,
                size=(600, 500),
                resizable=True,
                titlebar_background_color="black",
                titlebar_text_color="white"
            )
        print('-- Process finished --')        
else:
    print('-- Application closed --')