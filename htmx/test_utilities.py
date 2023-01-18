import unittest
from . import utilities

class UtilitiesTestCase(unittest.TestCase):

    def setUp(self):
        self.gini = utilities.GiniIndex(2010)
        self.cpi = utilities.CpiIndex('FPCPITOTLZGDEU')
        self.stock = utilities.StockIndex('SP500')

    def test_gini_index_attributes(self):
        inputs = {
            'FRANCE' : 'FRA',
            'ITALY' : 'ITA',
            'NORWAY' : 'NOR',
            'POLAND' : 'POL',
            'SWEDEN' : 'SWE',
            'UK' : 'GBR'
            }
        self.assertEquals(self.gini.inputs, inputs)
        self.assertEquals(self.gini.year, 2010)

    def test_gini_index_get_data(self):
        self.gini.get_data(name='FRANCE', ticker='FRA')
        data = {'FRANCE': '33.7'}
        self.assertEquals(self.gini.results, data)

    def test_gini_index_get_results(self):
        self.gini.get_results()
        data = {'FRANCE': '33.7', 'UK': '34.4', 'SWEDEN': '27.7', 'NORWAY': '25.7', 'ITALY': '34.7', 'POLAND': '33.2'}
        self.assertEquals(self.gini.results, data)

    def test_gini_index_get_context(self):
        data = self.gini.get_context()
        self.assertIsNotNone(data['script'])
        self.assertIsNotNone(data['div'])
        self.assertEquals(data['years'], range(2010,2019))

    def test_cpi_index_attributes(self):
        inputs = {
            'GERMANY' : 'FPCPITOTLZGDEU',
            'ITALY' : 'FPCPITOTLZGITA',
            'NORWAY' : 'FPCPITOTLZGNOR',
            'POLAND' : 'FPCPITOTLZGPOL',
            'SWEDEN' : 'FPCPITOTLZGSWE',
            'UK' : 'FPCPITOTLZGGBR'
        }
        self.assertEquals(self.cpi.inputs, inputs)
        self.assertEquals(self.cpi.symbol, 'FPCPITOTLZGDEU')

    def test_cpi_index_get_key(self):
        dictionary = {'key' : 'value'}
        result = self.cpi.get_key(dictionary, 'value')
        self.assertEquals(result, ['key'])

    def test_cpi_index_get_context(self):
        data = self.cpi.get_cpi_context()
        self.assertIsNotNone(data['script'])
        self.assertIsNotNone(data['div'])
        self.assertEquals(data['inputs'], self.cpi.inputs)

    def test_gini_index_attributes(self):
        inputs = {
            'S&P 500' : 'SP500',
            'DOW JONES' : 'DJIA',
            'NASDAQ 100' : 'NASDAQ100',
            'WILSHIRE 5000' : 'WILL5000PR',
            'WILSHIRE US REIT' : 'WILLREITIND'
        }
        self.assertEquals(self.stock.inputs, inputs)
        self.assertEquals(self.stock.stock, 'SP500')

    def test_stock_index_get_context(self):
        data = self.stock.get_stock_context()
        self.assertIsNotNone(data['script'])
        self.assertIsNotNone(data['div'])
        self.assertEquals(data['inputs'], self.stock.inputs)



    


