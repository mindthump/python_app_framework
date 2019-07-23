import json
import random
import sys
import os
import falcon

# NOTE: Hack.
from toolbox.app_utils import initialize_logging


class FruitServer(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "<h1>Ooops.</h1>"
        with open('fruit.json') as fruit_list:
            fruits = falcon.json.loads(fruit_list.read())
            random_fruit = random.choice(fruits['fruits'])
            logger.info(f"Serving fruit: {random_fruit}")
        resp.body = json.dumps({"favorite_fruit": random_fruit})


logger = initialize_logging()

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
fruit_server = FruitServer()

app.add_route("/fruit", fruit_server)

