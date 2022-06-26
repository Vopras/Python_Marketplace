"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def add_cart(self, nr_prod, cart_id, prod_id):
        remaining = nr_prod
        while remaining > 0:
            wait = self.marketplace.add_to_cart(cart_id, prod_id)
            if not wait:
                time.sleep(self.retry_wait_time)
            else:
                remaining = remaining - 1

    def remove_cart(self, nr_prod, cart_id, prod_id):
        for i in range(0, nr_prod):
            self.marketplace.remove_from_cart(cart_id, prod_id)

    def print_carts(self, cart_id):
        order_list = self.marketplace.place_order(cart_id)
        for order in order_list:
            print(self.name, "bought", order)

    def add_product(self, prod_id, nr_prod):
        self.marketplace.add_product(prod_id, nr_prod)

    def remove_product(self, prod_id, nr_prod):
        self.marketplace.remove_product(prod_id, nr_prod)


    def run(self):
        cart_id = self.marketplace.new_cart()
        for cart in self.carts:
            for string in cart:
                command = string.get("type")
                prod_id = string.get("product")
                nr_prod = string.get("quantity")
                if command == "add":
                    self.add_cart(nr_prod, cart_id, prod_id)
                elif command == "remove":
                    self.remove_cart(nr_prod, cart_id, prod_id)
        self.print_carts(cart_id)
