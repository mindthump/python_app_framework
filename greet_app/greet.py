import random
import sys
import json
from toolbox import app_framework


class Greeter(app_framework.AppFramework):
    def __init__(self):
        # This call to super().__init__ is the only required element
        super(Greeter, self).__init__()
        # Empty or constant values
        self.users = None
        self.db_server = None
        self.foo_db = None
        self.fruit_list = None

    def additional_arguments(self):
        # Only add_arguments, Framework will do the parsing
        self.parser.add_argument(
            "--greeting", action="store", env_var="GREETING", default="Hola"
        )
        # Titles are in a service secret
        self.parser.add_argument(
            "--default-title", action="store", env_var="DEFAULT_TITLE", default="nobody"
        )
        # self.parser.add_argument(
        #     "--db-host", action="store", env_var="DB_HOST", default=""
        # )
        # self.parser.add_argument(
        #     "--db-name", action="store", env_var="DB_NAME", default="hunny-jar"
        # )
        self.parser.add_argument(
            "--fruit-server",
            action="store",
            env_var="FRUIT_SERVER",
            default="http://fruit:80/fruit",
        )
        self.parser.add_argument(
            "--user-info-path",
            action="store",
            env_var="USER_INFO_PATH",
            # This should be a service secret, mounted to this service.
            default="/run/secrets/user-info",
        )

    def prepare(self):
        # Get resources, servers, etc. ready
        self.users = self.get_user_info()
        # self.setup_db()

    def run(self):
        # TODO: Break this up, it's way overloaded
        # Actual application work here

        for user in self.users:
            self.logger.info(f"Preparing to greet user {user}.")
            print(f"{self.app_args.greeting}, {user}!")

            try:
                title = self.users[user].get("title", "unperson")
                # TODO: Random fruit for now, get it based on some key?
                fruit = (
                    self.requests.get(self.app_args.fruit_server)
                    .json()
                    .get("favorite_fruit")
                )

                self.logger.info(
                    f"{user} is a {title}, and {fruit} is their favorite fruit."
                )
            except self.requests.ConnectionError as cerr:
                self.logger.warning(
                    f"Could not connect to '{self.app_args.fruit_server}' service, is it running? See application log for details."
                )
                self.logger.debug("Connection Error: {}".format(cerr))
                return 66
            except Exception as ex:
                self.logger.warning(
                    f"A severe error occurred while communicating with the '{self.app_args.fruit_server}' service. See application log for details."
                )
                self.logger.debug(f"USER INFO FAIL:\n{ex}")
                return 99

        # DEBUG: raise app_framework.AppFrameworkError("Error Condition: RED")
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")

    def get_user_info(self):
        try:
            # Shhh... it's a secret.
            with open(self.app_args.user_info_path) as user_info:
                return json.loads(user_info.read())["users"]
        except Exception as ex:
            self.logger.warning(f"SECRETS FAILURE:\n{ex}")
            return json.loads("{}")


if __name__ == "__main__":
    app = Greeter()
    result = app.execute()
    sys.exit(result)
