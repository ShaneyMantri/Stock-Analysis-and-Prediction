import datetime
from io import BytesIO
import PIL
import PIL.Image
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from matplotlib import pylab
from pylab import *

from .models import Company
from .Symbol_to_company import get_full_name
from .yf import Obtain_price
from .getpriceforgraph import get_price
from .graphplot import plotgraph



#GLOBAL
selected_companies = []
selected_companies_name_list = []
openpricelist = []
closepricelist = []
highest = []
lowest = []



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


# def getimage(symbol):
#     # Construct the graph

#     x, y = get_price(symbol)
#     scatter(x, y, label= "dots", color= "blue",  marker= ".", s=30)
#     print(x,y)
#     xlabel('Epoch Time')
#     ylabel('Price')
#     title('Stock Trend')
#     # grid(True)

#     # # Store image in a string buffer
#     # buffer = StringIO()
#     # canvas = pylab.get_current_fig_manager().canvas
#     # canvas.draw()
#     # pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
#     # pilImage.save(buffer, "PNG")
#     # pylab.close()
#     buffer = BytesIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
#     graphIMG.save(buffer, "PNG")
#     pylab.close()
#     # Send buffer in a http response the the browser with the mime type image/png set
#     return HttpResponse(buffer.getvalue(), mimetype="image/png")