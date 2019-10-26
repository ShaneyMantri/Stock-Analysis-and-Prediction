import matplotlib
matplotlib.use("Agg")

import base64
import datetime
import random
import time
from io import BytesIO

import matplotlib.pyplot as plt
import PIL
import PIL.Image
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from matplotlib import pylab
from pylab import *

from .graphplot import plotgraph, get_price
from .models import Company
from .Symbol_to_company import get_full_name
from .YahooFinanceAllAttributes import Obtain_price
from .unique_rows import read_unique_rows
from .linearReg import prediction

#GLOBAL
selected_companies = []
selected_companies_name_list = []
openpricelist = []
closepricelist = []
highest = []
lowest = []
company_for_graph = None

@login_required
def home(request):
    global selected_companies, selected_companies_name_list, openpricelist, closepricelist, highest, lowest,company_for_graph
    
    if len(selected_companies) == 0:
        messages.error(request, f'No company has been selected. Please select at least one company')
        return redirect('Stock-Checkbox')
    # print(selected_companies)
    
    selected_companies_name_list.clear()
    openpricelist.clear()
    closepricelist.clear()
    highest.clear()
    lowest.clear()
    for x in selected_companies:
        selected_companies_name_list.append(get_full_name(x))
        openprice,closeprice,high,low = Obtain_price(x)
        openpricelist.append(round(openprice,2))
        closepricelist.append(round(closeprice,2))
        highest.append(high)
        lowest.append(low)
    # print(selected_companies_name_list)
    combined_list = zip(selected_companies_name_list, selected_companies, openpricelist,closepricelist,highest,lowest)

    Current_date_time = datetime.datetime.now()
    context = {
        'combined_list':combined_list,
        'Current_date_time':Current_date_time
    }

    if request.method == 'POST':
        # plotgraph(request.POST.get('graphbutton'))
        t = None
        s = None   
        graph_of_company = request.POST.get('graphbutton')
        details_of_company = request.POST.get('detailsbutton')
        prediction_of_company = request.POST.get('predictionbutton')

        if graph_of_company is not None:
            t, s, xticks_var, waste = plotgraph(graph_of_company)
            # print("DONE4")
            plot(t, s)
            xticks(xticks_var, rotation  = 'vertical')
            xlabel('Time')
            ylabel('Price')
            title('Graph for {}'.format(graph_of_company))
            grid(True)
            # print("HELLO")
            # buffer = BytesIO()
            # canvas = pylab.get_current_fig_manager().canvas
            # canvas.draw()
            # pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
            # pilImage.save(buffer, "PNG")
            # pylab.close()
            buffer = None
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=500)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
            buffer.close()
            context1 = {
                'image_base64' : image_base64
            }
            
            return render(request, "stock/graph.html", context1)
        elif details_of_company is not None :
            time, openrate, closerate, high, low = read_unique_rows(details_of_company)
            full_name = get_full_name(details_of_company)
            combined_list_2 = zip(time, openrate, closerate,high,low)
            context2 = {
                'full_name':full_name,
                'details_of_company': details_of_company,
                'combined_list_2':combined_list_2
            }
            # print("HELLO")
            return render(request, "stock/about.html",context2)
        else:
            mse_error, df_shape_0, all_mid_data, N, run_avg_predictions, df_date_loc = prediction(prediction_of_company)
            figure(figsize = (20,10))
            plot(range(df_shape_0),all_mid_data,color='b',label='Prediction')
            plot(range(0,N),run_avg_predictions,color='orange', label='Actual')
            xticks(range(0,df_shape_0,50),df_date_loc,rotation  = 'vertical')
            xlabel('Date')
            ylabel('Mid Price')
            legend(fontsize=18)
            title('Prediction for {}'.format(prediction_of_company))
            grid(True)
            tick_params(axis='x', which='minor', bottom=False)
            buffer = None
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=500)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
            buffer.close()
            context2 = {
                'image_base64' : image_base64,
                'mse_error':mse_error
            }
            return render(request, "stock/prediction.html", context2)

    return render(request, "stock/home.html", context)


@login_required
def checkbox(request):
    global selected_companies
    selected_companies.clear()
    context1 = {
        "stocks" : Company.objects.all(),
        "title" : "Checkbox",
    }

    if request.method == 'POST':
        selected_companies.clear()
        selected_companies = request.POST.getlist('checks[]')
        # print(selected_companies)
        
        return redirect('Stock-Home')
    return render(request, "stock/Checkbox.html",context1)




def about(request):
    return render(request, "stock/about.html" , {"title" : "About"})
