import json
import random
import falcon
import os

from app_utils import utils


class FruitServer(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.text = "<h1>Ooops.</h1>"
        # Look for the fruit list in the same directory as this file.
        # TODO: Put the fruit list in something K8s-ish
        with open(f"{os.path.dirname(__file__)}/fruit.json") as fruit_list:
            fruits = json.loads(fruit_list.read())
            random_fruit = random.choice(fruits["fruits"])
            logger.info(f"Serving fruit: {random_fruit}")
        resp.text = json.dumps({"favorite_fruit": random_fruit})


logger = utils.initialize_logging()

# falcon.API instances are callable WSGI apps
app = falcon.App()

# Resources are represented by long-lived class instances
fruit_server = FruitServer()

app.add_route("/fruit", fruit_server)
