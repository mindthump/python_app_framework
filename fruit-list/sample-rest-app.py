import falcon


class SampleRestAppResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        # Get this from sample app?
        resp.body = "\nHey there, world.\n" "\n" "    ~ Me\n\n"


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
sample_rest_app = SampleRestAppResource()

app.add_route("/greet", sample_rest_app)
