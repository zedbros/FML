"""
Lets you interact with the database of beer deliveries.
"""

from typing import TypedDict
import sqlite3
import tabulate  # used to display the tables in a nice way, so that the agent can read them


def get_db_connection():
    conn = sqlite3.connect('beers.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def drop_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS DeliveryItems")
    cursor.execute("DROP TABLE IF EXISTS Deliveries")
    cursor.execute("DROP TABLE IF EXISTS Customers")
    cursor.execute("DROP TABLE IF EXISTS Beers")
    conn.commit()

def load_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    with open('lab9/beers.sql', encoding='utf-8') as f:
        cursor.executescript(f.read())
    conn.commit()   


class Article(TypedDict):
    article_id: int
    quantity: int


def get_customers(use_tabulate=True) -> list[tuple] | str:
    """
    use_tabulate: if True, return a string with the table formatted with tabulate. Usefull format to give to the agent.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    if use_tabulate:
        return tabulate.tabulate(cursor.fetchall(), headers=["ID", "Name", "Address", "Postal_Code", "City", "Canton"], tablefmt="grid")
    else:
        return cursor.fetchall()

def get_beers(use_tabulate=True) -> list[tuple] | str:
    """
    use_tabulate: if True, return a string with the table formatted with tabulate. Usefull format to give to the agent.
    Returns a list of tuples with the beers in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Beers")
    if use_tabulate:
        return tabulate.tabulate(cursor.fetchall(), headers=["ID", "Beer_Name", "Category", "Unit_Price"], tablefmt="grid", numalign="right")
    else:
        return cursor.fetchall()

def insert_delivery(customer_id) -> int:
    """
    Insert a delivery into the database.
    Returns the id of the newly created delivery.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Deliveries (Customer_ID) VALUES (?)", (customer_id,))
    conn.commit()
    return cursor.lastrowid

def insert_delivery_item(delivery_id, beer_id, quantity) -> None:
    """
    Insert a delivery item into the database.
    delivery_id: the id of the delivery to which the item belongs
    beer_id: the id of the beer
    quantity: the quantity of the beer
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DeliveryItems (Delivery_ID, Beer_ID, Quantity) VALUES (?, ?, ?)", (delivery_id, beer_id, quantity))
    conn.commit()  

def list_deliveries(use_tabulate=True) -> list[tuple] | str:
    # """
    # use_tabulate: if True, return a string with the table formatted with tabulate. Usefull format to give to the agent.
    # """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Deliveries")
    if use_tabulate:
        t = tabulate.tabulate(cursor.fetchall(), headers=["ID", "Customer_ID", "Delivery_Date"], tablefmt="grid")
        print(t)
        return t
    else:
        print("EUUUUG")
        t = cursor.fetchall()
        return t
    # raise NotImplementedError("implement me!!!")


if __name__ == "__main__":
    # example usage, insert a delivery

    if input("Reinitialize the database? (y/n)").lower() == "y":
        drop_tables()
        load_db()

        delivery_id = insert_delivery(22)
        print(f"Inserted delivery {delivery_id}")
        insert_delivery_item(delivery_id, 1, 10)
        insert_delivery_item(delivery_id, 2, 20)
        print(list_deliveries())
    
