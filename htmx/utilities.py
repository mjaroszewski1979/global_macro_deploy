import math
import requests
import datetime
import os
from threading import Thread
from bs4 import BeautifulSoup as bs
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from pandas_datareader._utils import RemoteDataError
import pandas_datareader.data as pdr
import numpy as np


class GiniIndex:
    def __init__(self, year):
        self.year = year
        self.results = {}
        self.inputs = {
            'FRANCE' : 'FRA',
            'ITALY' : 'ITA',
            'NORWAY' : 'NOR',
            'POLAND' : 'POL',
            'SWEDEN' : 'SWE',
            'UK' : 'GBR'
            }
        self.gini_values = []
        self.gini_countries = []
        
    def get_data(self, name, ticker):
        api_key = os.environ.get('API_KEY')
        endpoint = 'https://fred.stlouisfed.org/data/SIPOVGINI' + ticker + '.txt'
        params = {'api_key': api_key, 'file_type': 'json'}
        try:
            response = requests.get(endpoint,params=params)
            soup = bs(response.text,"lxml")
            data = soup.text.split('\n')
            for line in data:
                if str(self.year) in line:
                    self.results[name] = line.rstrip()[-4:]
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)   
            
    def get_results(self):
        threads = []
        for key in self.inputs:
            threads.append(Thread(target=self.get_data, args=[key, self.inputs[key]]))
            
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return self.results

    
    def get_context(self):
        if self.get_results() is not None:
            sorted_results = sorted(self.results.items(), key=lambda x: x[1])
            for item in sorted_results:
                self.gini_countries.append(item[0])
                self.gini_values.append(item[1])
            cds = ColumnDataSource(data=dict(countries=self.gini_countries, vals=self.gini_values))
            fig = figure(x_range=self.gini_countries, sizing_mode='stretch_both', height=400, toolbar_location="below", title=f"GINI Index for ({self.year})")
            fig.title.align = 'center'
            fig.title.text_font_size = '1.5em'
            fig.xaxis.major_label_orientation = math.pi / 4
            fig.vbar(source=cds, x='countries', top='vals', width=0.1, color='black', fill_color='white')
            fig.background_fill_color = "#312450"
            fig.grid.visible = False
            tooltips = [
                ('Country', '@countries'),
                ('GINI', '@vals')
            ]
            fig.add_tools(HoverTool(tooltips=tooltips))
            script, div = components(fig)
            context = {
                'script': script,
                'div': div,
                'years': range(2010,2019)
            }
            return context
        else:
            context = {
                'error_msg' : 'Data you requested is temporarily unavailabl'
            }
            return context

class CpiIndex:
    def __init__(self, symbol):
        self.symbol = symbol
        self.inputs = {
            'GERMANY' : 'FPCPITOTLZGDEU',
            'ITALY' : 'FPCPITOTLZGITA',
            'NORWAY' : 'FPCPITOTLZGNOR',
            'POLAND' : 'FPCPITOTLZGPOL',
            'SWEDEN' : 'FPCPITOTLZGSWE',
            'UK' : 'FPCPITOTLZGGBR'
        }

    def get_key(self, dct, value):
        return [key for key in dct if (dct[key] == value)]
    
    def get_cpi_context(self):
        try:
            df = pdr.DataReader(self.symbol, 'fred', start = datetime.datetime(2000, 1, 1), end = datetime.datetime.now())
            years = [df.index[x].year for x in range(12)]
            values = [round(df[self.symbol][x], 2) for x in range(12)] 
            data = self.get_key(self.inputs, self.symbol)
            fig = figure(sizing_mode='stretch_both', height=400, toolbar_location="below", title=f"CPI Index for {data[0]}")
            fig.line(x=years, y=values, line_color='white', width=1, line_dash = "dotted")
            fig.xaxis.axis_label = 'Lookback Period'
            fig.yaxis.axis_label = 'Percent'
            fig.title.align = 'center'
            fig.title.text_font_size = '1.5em'
            fig.background_fill_color = "#312450"
            fig.grid.visible = False
            tooltips = [
                    ('Years', '@x'),
                    ('CPI', '@y')
                ]
            fig.add_tools(HoverTool(tooltips=tooltips))
            script, div = components(fig)
            context = {
                'script': script,
                'div': div,
                'inputs' : self.inputs
            }
            return context
        except RemoteDataError:
            context = {
                'error_msg' : 'Data you requested is temporarily unavailabl'
            }
            return context


class StockIndex:
    def __init__(self, stock):
        self.stock = stock
        self.inputs = {
            'S&P 500' : 'SP500',
            'DOW JONES' : 'DJIA',
            'NASDAQ 100' : 'NASDAQ100',
            'WILSHIRE 5000' : 'WILL5000PR',
            'WILSHIRE US REIT' : 'WILLREITIND'
        }

    def get_key(self, dct, value):
        return [key for key in dct if (dct[key] == value)]

    def get_stock_context(self):
        try:

            data = self.get_key(self.inputs, self.stock)
            df = pdr.DataReader(self.stock, 'fred', start = datetime.datetime(2000, 1, 1), end = datetime.datetime.now())
            df['pct_change'] = df.pct_change() * 100
            result = df['pct_change'].values.tolist()
            positive_return = np.array([x for x in result if x >= 0])[:1000]
            negative_return = np.array([x for x in result if x < 0])[:1000]
            if len(positive_return) > len(negative_return):
                positive_return = np.array([x for x in result if x >= 0])[:(len(negative_return))]
            else:
                negative_return = np.array([x for x in result if x < 0])[:(len(positive_return))]
            bins = hexbin(positive_return, negative_return, 0.2)
            data = self.get_key(self.inputs, self.stock)
            fig = figure(tools="wheel_zoom,reset", 
                match_aspect=True, 
                background_fill_color='#312450', 
                sizing_mode='stretch_both', 
                height=500, 
                toolbar_location="below", 
                title=f"Returns for {data[0]}")
            fig.xaxis.axis_label = 'Positive Returns'
            fig.yaxis.axis_label = 'Negative Returns'
            fig.title.align = 'center'
            fig.title.text_font_size = '1.5em'
            fig.grid.visible = False
            fig.hex_tile(q="q", r="r", size=0.1, line_color=None, source=bins,
            fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))

            script, div = components(fig)
            context = {
                'script': script,
                'div': div,
                'inputs' : self.inputs
            }
            return context

        except RemoteDataError:
            context = {
                'error_msg' : 'Data you requested is temporarily unavailabl'
            }
            return context







    



