import datetime
import random
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from matplotlib import pylab
from pylab import *

from .getpriceforgraph import get_price
from .graphplot import plotgraph
from .models import Company
from .Symbol_to_company import get_full_name
from .yf import Obtain_price

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
    # context1 = {
    #     "stocks" : selected_companies_name_list,
    #     "title" : "Home",
    #     "Symbols":selected_companies,
    #     # "date": s[0],
    #     "Current_Price": "LOL"
    # }
    
    context = {
        'combined_list':combined_list,
        'Current_date_time':Current_date_time
    }

    if request.method == 'POST':
        plotgraph(request.POST.get('graphbutton'))
        # company_for_graph = request.POST.get('graphbutton')

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
        
        selected_companies = request.POST.getlist('checks[]')
        # print(selected_companies)
        
        return redirect('Stock-Home')
    return render(request, "stock/Checkbox.html",context1)




def about(request):
    return render(request, "stock/about.html" , {"title" : "About"})


# def graphplot(request):
#     global company_for_graph

#     if company_for_graph is None:
#         messages.error(request, f'No company has been selected. Please select any one company')
#         return redirect('Stock-Home')
    
#     xdata, ydata1 = get_price(company_for_graph)
#     nb_element = 50

#     kwargs1 = {'shape': 'circle'}

#     extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}

#     chartdata = {
#         'x': xdata,
#         'name1': 'series 1', 'y1': ydata1, 'kwargs1': kwargs1, 'extra1': extra_serie1,

#     }
#     charttype = "scatterChart"
#     data = {
#         'charttype': charttype,
#         'chartdata': chartdata,
#     }
#     return render_to_response('scatterchart.html', data)
