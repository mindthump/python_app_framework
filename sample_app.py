import sys
import json
import app_framework


class SampleApp(app_framework.AppFramework):
    def __init__(self):
        # This call to super().__init__ is the only required element
        super(SampleApp, self).__init__()
        # Empty or constant values
        self.users = None

    def additional_arguments(self):
        # Only add_arguments, Framework will do the parsing
        self.parser.add_argument(
            "--greeting", action="store", env_var="GREETING", default="Hola"
        )
        self.parser.add_argument(
            "--targeturl", action="store", env_var="TARGET_URL", default="spew"
        )
        self.parser.add_argument(
            "--title", action="store", env_var="TITLE", default="nobody"
        )

    def prepare(self):
        # Get resources, servers, etc. ready
        self.users = ["Julio", "Adela"]

    def run(self):
        # Actual application work here
        for user in self.users:
            self.logger.info("Preparing to greet user {}.".format(user))
            print("{}, {}!".format(self.app_args.greeting, user))
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        request_data = {"title": self.app_args.title}
        try:
            response = self.requests.post(
                # This should be running httpbin, which reflects the request
                # 'spew' (default) service launched in docker-compose.yml
                "http://{target}/post".format(target=self.app_args.targeturl), json=request_data, headers=headers
            )
            response_json = response.json()
            self.logger.debug("Request content:\n{}".format(response_json))
            response_data = response_json.get('data') or '{}'
            title = json.loads(response_data).get('title', 'nobody')
            self.logger.info("{} is a {}.".format(self.users[0], title))
        except self.requests.ConnectionError as cerr:
            self.logger.warning("Could not connect to 'spew' service, is it running? See application log for details.")
            self.logger.debug("Connection Error: {}".format(cerr))
            return 66
        except Exception as ex:
            self.logger.warning("A severe error occurred while communicating with the 'spew' service. See application log for details.")
            self.logger.debug("Connection Error: {}".format(ex))
            return 99
        # DEBUG: raise app_framework.AppFrameworkError("Error Condition: RED")
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")


if __name__ == "__main__":
    app = SampleApp()
    result = app.execute()
    sys.exit(result)
