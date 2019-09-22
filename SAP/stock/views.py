import datetime
from io import BytesIO

import PIL
import PIL.Image
import plotly.graph_objs as go
import plotly.offline as opy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
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


@login_required
def home(request):
    global selected_companies, selected_companies_name_list, openpricelist, closepricelist, highest, lowest
    
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


