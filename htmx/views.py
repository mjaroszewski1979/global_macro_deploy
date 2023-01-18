from django.shortcuts import render
from .utilities import GiniIndex, CpiIndex, StockIndex

def home(request):
    return render(request, 'home.html')

def gini(request):
    
    year = request.GET.get('year', 2008)
    gi = GiniIndex(year=year)
    context = gi.get_context()
    if request.htmx:
        return render(request, 'partials/chart.html', context)

    return render(request, 'gini.html', context)

def cpi(request):

    symbol = request.GET.get('symbol', 'FPCPITOTLZGPOL')
    cpi = CpiIndex(symbol=symbol)
    context = cpi.get_cpi_context()
    if request.htmx:
        return render(request, 'partials/chart.html', context)

    return render(request, 'cpi.html', context)

def stock(request):

    stock = request.GET.get('stock', 'SP500')
    stock = StockIndex(stock=stock)
    context = stock.get_stock_context()
    if request.htmx:
        return render(request, 'partials/chart.html', context)

    return render(request, 'stock.html', context)

def page_not_found(response, exception):
    return render(response, '404.html')

def server_error(response):
    return render(response, '500.html')





