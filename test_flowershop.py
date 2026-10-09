import unittest
import tempfile
import os
import sqlite3


import flowershop
from flowershop import (
    init_db, add_product, get_products,
    add_customer, get_customers,
    add_order, get_orders,
)

class TestFlowerShop(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       
        cls._original_db = flowershop.DB_NAME
        cls._tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        flowershop.DB_NAME = cls._tmp.name
        init_db()


    @classmethod
    def tearDownClass(cls):
        flowershop.DB_NAME = cls._original_db
        if os.path.exists(cls._tmp.name):
            os.remove(cls._tmp.name)


   
    def test_01_add_product(self):
       
        before = len(get_products())


       
        add_product('Роза тестовая', 'Цветы', 250.0, 10)


       
        self.assertEqual(len(get_products()), before + 1)


   
    def test_02_get_products(self):
   
        add_product('Тюльпан тестовый', 'Цветы', 150.0, 5)
   
        products = get_products()
     
        self.assertTrue(len(products) >= 1)


    def test_03_add_customer(self):
     
        before = len(get_customers())

        add_customer('Тестов Тест', '+7-900-000-00-01')
   
        self.assertEqual(len(get_customers()), before + 1)


   
    def test_04_add_order(self):
     
        add_product('Букет тестовый', 'Букеты', 1000.0, 3)
        p = get_products('Букет тестовый')[0]
        c = get_customers()[0]

        add_order(c[0], p[0], 1, 1000.0)

        self.assertTrue(len(get_orders()) >= 1)


 
    def test_05_order_total(self):
     
        add_product('Пион тестовый', 'Цветы', 500.0, 5)
        p = get_products('Пион тестовый')[0]
        c = get_customers()[0]

        total = 3 * p[3]  # 3 × 500
        add_order(c[0], p[0], 3, total)

        self.assertEqual(get_orders()[0][4], 1500.0)
      
 
    def test_06_search(self):
   
        add_product('Роза уникальная', 'Цветы', 250.0, 10)


   
        result = get_products('уникальная')


   
        self.assertTrue(len(result) >= 1)


   
    def test_07_duplicate_product(self):
 
        add_product('Дубль тестовый', 'Цветы', 100.0, 1)

        with self.assertRaises(sqlite3.IntegrityError):
            add_product('Дубль тестовый', 'Цветы', 100.0, 1)




if __name__ == '__main__':
    unittest.main(verbosity=2)

