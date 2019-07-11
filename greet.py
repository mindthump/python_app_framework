import sys
import json
import app_framework


class Greeter(app_framework.AppFramework):
    def __init__(self):
        # This call to super().__init__ is the only required element
        super(Greeter, self).__init__()
        # Empty or constant values
        self.users = None

    def additional_arguments(self):
        # Only add_arguments, Framework will do the parsing
        self.parser.add_argument(
            "--greeting", action="store", env_var="GREETING", default="Hola"
        )
        self.parser.add_argument(
            "--target-hostname",
            action="store",
            env_var="TARGET_HOSTNAME",
            default="spew",
        )
        self.parser.add_argument(
            "--target-port", action="store", env_var="TARGET_PORT", default="80"
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
            # TODO: Get a random fruit from the fruit-list server
            response = self.requests.post(
                # This should be running httpbin, which reflects the request
                # Service launched in docker-compose.yml
                # TODO: I doubt this is solid or safe. What is the best target name?
                "http://{target}:{port}/post".format(
                    target=self.app_args.target_hostname, port=self.app_args.target_port
                ),
                json=request_data,
                headers=headers,
            )
            response_json = response.json()
            self.logger.debug("Request content:\n{}".format(response_json))
            response_data = response_json.get("data") or "{}"
            title = json.loads(response_data).get("title", "nobody")
            self.logger.info("{} is a {}.".format(self.users[0], title))
        except self.requests.ConnectionError as cerr:
            self.logger.warning(
                "Could not connect to '{target}:{port}' service, is it running? See application log for details.".format(
                    target=self.app_args.target_hostname, port=self.app_args.target_port
                )
            )
            self.logger.debug("Connection Error: {}".format(cerr))
            return 66
        except Exception as ex:
            self.logger.warning(
                "A severe error occurred while communicating with the '{target}:{port}' service. See application log for details.".format(
                    target=self.app_args.target_hostname, port=self.app_args.target_port
                )
            )
            self.logger.debug("Connection Error: {}".format(ex))
            return 99
        # DEBUG: raise app_framework.AppFrameworkError("Error Condition: RED")
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")


if __name__ == "__main__":
    app = Greeter()
    result = app.execute()
    sys.exit(result)
