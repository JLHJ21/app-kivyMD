import pdfkit
import jinja2
import json
from kivy.network.urlrequest import UrlRequest
import MVC.controller.functions as functions

#print(functions.global_bolivar)

class PDF():

    def test():
        

        query_find = {
                #nombre de la coleccion
                "collection_choose": "sales", 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('6679862b5b4d0ac91b1fc8bc')"
                    },
                #dato a mostrar
                "projection": "None"
            }


        query_find = json.dumps(query_find)

        result= UrlRequest(url + 'find_one', req_body=query_find, req_headers=headers)

        result.wait()
        #while not result.is_finished:
        #    sleep(1)                         # seems to be unnecessary in this case
        #Clock.tick()

        results = result.result
        #data = json.loads(results)
        #a = json.loads(results[0])

        data = []

        for product in results['products_sales']:
            dictionary_product = {
                    'name_product': product['name_product'],
                    'amount_product': product['amount_wanted'],
                    'price_product_unit': product['price_product_unit'],
                    'total_product' : float(product['price_product_unit']) * int(product['amount_wanted'])
                }
            
            data.append(dictionary_product)

        client = results['data_client_sales'][0]['name_client']
        employeer = results['data_staff_sales'][0]['name_staff']
        date_did = results['date_sales']
        total_price = results['total_purchase_sales']
        id_bill = str(results['_id'])


        type_money = []
        for paid_money in results['data_money_sales']:
            type_money.append(paid_money)

        send_data = []
        send_data.append(client)
        send_data.append(employeer)
        send_data.append(date_did)
        send_data.append(total_price)
        send_data.append(id_bill)
        send_data.append(data)

        PDF.CreatePDF(send_data)

        #print(results)
        #print('-----')

        #for item in results.values():
        #    print(item)
        #    print('-----')


    def CreatePDF(id):

        
        query_find = {
                #nombre de la coleccion
                "collection_choose": "sales", 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": id
                    },
                #dato a mostrar
                "projection": "None"
            }

        results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find_one')


        products_list = []

        for product in results['products_sales']:
            
            total_product = float(product['price_product_unit']) * int(product['amount_wanted'])
            total_product = functions.FunctionsKivys.TransformProfit(total_product, 'human')

            
            price_product_unit = functions.FunctionsKivys.TransformProfit(product['price_product_unit'], 'human')

            dictionary_product = {
                    'name_product': product['name_product'],
                    'amount_product': product['amount_wanted'],
                    'price_product_unit': price_product_unit,
                    'total_product' : total_product

                }
            
            products_list.append(dictionary_product)

        client = results['data_client_sales'][0]['name_client']
        employeer = results['data_staff_sales'][0]['name_staff']
        date_did = results['date_sales']

        id_bill = str(results['_id'])

        total_price = results['total_purchase_sales']
        total_price = functions.FunctionsKivys.TransformProfit(total_price, 'human')

        type_money = []
        for paid_money in results['data_money_sales']:
            type_money.append(paid_money)
        '''
        client = 'Jorge'
        employeer = 'Luis'

        id_bill = 'abc1234'

        name_product = 'arroz'
        price_product = '500'
        amount_product = '4'

        total_price = 0

        total_price = total_price + (float(price_product) * int(amount_product))
        total_price = total_price + (float(price_product) * int(amount_product))


        products = [
            {
                'name_product': name_product,
                'price_product': price_product,
                'amount_product': amount_product,
                'total_product' : float(price_product) * int(amount_product)
            },
            {
                'name_product': 'harina',
                'price_product': '5000',
                'amount_product': '50',
                'total_product' : float(price_product) * int(amount_product)
            },
        ]
        date = '20-06-2024'
        type_paid = 'Dólar'
        '''

        context = {'client': client, 'employeer': employeer, 'products': products_list, 'date_did': date_did, 'total_price': total_price, 'type_paid': type_money, 'id_bill': id_bill}

        template_loader = jinja2.FileSystemLoader('C:/Users/PC/Documents/Universidad_PDFs_4/app-kivyMD/AppProject/MVC/controller/sales_history/pdf/')
        template_env = jinja2.Environment(loader=template_loader)

        html_template = 'template.html'

        template = template_env.get_template(html_template)

        output_text = template.render(context)


        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

        output_pdf = 'pdfs/pdf_creado_' + id_bill +'.pdf'

        #css_url = 'C:/Users/PC/Documents/Universidad_PDFs_4/app-kivyMD/AppProject/MVC/controller/sales_history/pdf/style.css'

        #pdfkit.from_string(output_text, output_pdf, configuration=config, css=css_url)
        pdfkit.from_string(output_text, output_pdf, configuration=config, options={"enable-local-file-access": ""})

PDF.CreatePDF("ObjectId('6679862b5b4d0ac91b1fc8bc')")