"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = {}
        self.carts = {}
        self.producer_id = 0
        self.consumer_id = 0
        self.lock_publish = Lock()
        self.lock_cart = Lock()

    def producer_init(self):
        self.producers[self.producer_id] = []
        return self.producer_id

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producer_id = self.producer_id + 1
        return self.producer_init()

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.lock_publish.acquire()
        if len(self.producers.get(producer_id)) > self.queue_size_per_producer:
            self.lock_publish.release()
            return False
        else:
            producer = self.producers.get(producer_id)
            producer.append(product)
            self.lock_publish.release()
            return True

    def cart_init(self):
        self.carts[self.consumer_id] = []
        return self.consumer_id

    def add_to_cart(self, cart_id, product):
        """
        Adds the product to the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: product to add to the cart
        """
        self.lock_cart.acquire()
        if len(self.carts.get(cart_id)) > self.queue_size_per_producer:
            self.lock_cart.release()
            return False
        else:
            cart = self.carts.get(cart_id)
            cart.append([product, self.producer_id])
            self.lock_cart.release()
            return True


    def checkout(self, cart_id):
        """
        Returns the products in the cart

        :type cart_id: Int
        :param cart_id: id cart

        :returns a list of products in the cart
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        self.lock_cart.release()
        return cart

    def remove_from_cart(self, cart_id, product):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: product to remove from the cart
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][0] == product:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_producer(self, cart_id, producer_id):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type producer_id: Int
        :param producer_id: id producer
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][1] == producer_id:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_product(self, cart_id, product):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: product to remove from the cart
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][0] == product:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_product_and_producer(self, cart_id, product, producer_id):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: product to remove from the cart

        :type producer_id: Int
        :param producer_id: id producer
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][0] == product and cart[i][1] == producer_id:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_producer_and_product(self, cart_id, producer_id, product):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type producer_id: Int
        :param producer_id: id producer

        :type product: Product
        :param product: product to remove from the cart
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][0] == product and cart[i][1] == producer_id:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_product_and_producer_and_quantity(self, cart_id, product, producer_id, quantity):
        """
        Removes the product from the cart

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: product to remove from the cart

        :type producer_id: Int
        :param producer_id: id producer

        :type quantity: Int
        :param quantity: quantity to remove from the cart
        """
        self.lock_cart.acquire()
        cart = self.carts.get(cart_id)
        for i in range(len(cart)):
            if cart[i][0] == product and cart[i][1] == producer_id and cart[i][2] == quantity:
                cart.pop(i)
        self.lock_cart.release()
        return True

    def remove_from_cart_by_product_and_quantity(self, cart_id, product, quantity):


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.consumer_id = self.consumer_id + 1
        return self.cart_init()

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        prod_id = -1
        find_product = False
        key_list = list(self.producers.keys())

        for key in key_list:
            for prod in self.producers.get(key):
                if prod == product:
                    prod_id = key
                    find_product = True

        if find_product:
            self.lock_cart.acquire()
            self.carts.get(cart_id).append([product, prod_id])
            self.producers.get(prod_id).remove(product)
            self.lock_cart.release()

        return find_product

    def remove_from_cart(self, cart_id, product):
        cart = self.carts.get(cart_id)
        remove_id = None
        for prod, id_prod in cart:
            if prod == product:
                remove_id = id_prod
        cart.remove([product, remove_id])
        self.carts[cart_id] = cart
        self.producers.get(remove_id).append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        product_list = []
        products = self.carts.get(cart_id)
        for product, product_id in products:
            product_list.append(product)
        return product_list
