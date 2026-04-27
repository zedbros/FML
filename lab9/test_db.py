import unittest
import db
import datetime

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure the database is clean and loaded before tests
        db.drop_tables()
        db.load_db()

    @classmethod
    def tearDownClass(cls):
        # Clean up database after all tests
        db.drop_tables()
        db.load_db()

    def test_get_customers(self):
        customers_table = db.get_customers(use_tabulate=False)
        self.assertIsInstance(customers_table, list)
        self.assertEqual(len(customers_table), 8)
        customer = customers_table[0]
        self.assertEqual(customer[0], 22)
        self.assertEqual(customer[1], "Ferme Asile")
        self.assertEqual(customer[2], "Pascal Gremet")
        self.assertEqual(customer[3], "Promenade des Pêcheurs 10")
        self.assertEqual(customer[4], 46.2291492)
        self.assertEqual(customer[5], 7.2895976)
        self.assertEqual(customer[6], "1950")
        self.assertEqual(customer[7], "Sion")
        self.assertEqual(customer[8], "VS")

    def test_get_beers(self):
        beers_table = db.get_beers(use_tabulate=False)
        self.assertIsInstance(beers_table, list)
        self.assertEqual(len(beers_table), 7)
        beer = beers_table[0]
        self.assertEqual(beer[0], 1)
        self.assertEqual(beer[1], "Avalanche")
        self.assertEqual(beer[2], "Pale Ale")
        self.assertEqual(beer[3], 3)

    def test_insert_delivery_and_items(self):
        # Insert a new delivery
        customer_id = 22 # Ferme Asile
        delivery_id = db.insert_delivery(customer_id)
        self.assertIsInstance(delivery_id, int)
        self.assertGreater(delivery_id, 0) # Should get a valid ID

        # Insert items for this delivery
        beer_id_1 = 4 # Paratonnerre
        quantity_1 = 24
        db.insert_delivery_item(delivery_id, beer_id_1, quantity_1)

        beer_id_2 = 5 # BLIPA
        quantity_2 = 12
        db.insert_delivery_item(delivery_id, beer_id_2, quantity_2)

        # Check to verify the data was inserted correctly
        deliveries_table = db.list_deliveries(use_tabulate=False)
        self.assertIsInstance(deliveries_table, list)
        self.assertEqual(len(deliveries_table), 2)

        today = datetime.date.today().strftime("%Y-%m-%d")

        self.assertEqual(deliveries_table[0][0], delivery_id, "Delivery ID is not correct")
        self.assertEqual(deliveries_table[0][1], "Ferme Asile", "Customer name is not correct")
        self.assertEqual(deliveries_table[0][2], today, "Delivery date is not correct")
        self.assertEqual(deliveries_table[0][3], "Paratonnerre", "Beer name is not correct")
        self.assertEqual(deliveries_table[0][4], 24, "Quantity is not correct")

        self.assertEqual(deliveries_table, [(1, 'Ferme Asile', today, 'Paratonnerre', 24), (1, 'Ferme Asile', today, 'BLIPA', 12)])

if __name__ == '__main__':
    unittest.main() 