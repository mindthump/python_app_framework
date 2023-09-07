import random
import sys
import json
from app_utils import app_framework


class Greeter(app_framework.AppFramework):
    def __init__(self):
        # This call to super().__init__ is the only required element
        super(Greeter, self).__init__()
        # Empty or constant values
        self.users = None
        self.db_server = None
        self.foo_db = None
        self.fruit_list = None
        self.selected_users = None

    def additional_arguments(self):
        # Only add_arguments, Framework will do the parsing
        self.parser.add_argument(
            "--default-greeting", action="store", env_var="DEFAULT_GREETING", default="Salutations"
        )
        # Titles are in a JSON file
        self.parser.add_argument(
            "--default-title", action="store", env_var="DEFAULT_TITLE", default="a nobody"
        )
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
            default="/opt/user-data/users.json",
        )

    def prepare(self):
        # Get resources, servers, etc. ready
        self.logger.info("Preparing to start.")
        self.users = self.get_user_info()
        # print(f"There are {len(self.users)} users: {self.users}.")
        # run() can handle a list; here we randomly subset the full user list.
        self.selected_users = random.sample(list(self.users.keys()), 1)
        # self.setup_db()

    def run(self):
        # TODO: Break this up, it's way overloaded
        # Actual application work here

        for user in self.selected_users:
            self.logger.info(f"Preparing to greet user {user}.")
            title = self.users[user].get("title", self.app_args.default_title)
            possessive = self.users[user].get("possessive-pronoun", "their")
            greeting = self.users[user].get("greeting", self.app_args.default_greeting)
            print(f"{greeting}, {user}!")

            try:
                # Random fruit from simple falcon app
                fruit = (
                    self.requests.get(self.app_args.fruit_server, timeout=2)
                    .json()
                    .get("favorite_fruit")
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
            
            self.logger.info(
                f"{user} is {title}, and {fruit} is {possessive} favorite fruit."
            )

        # DEBUG: raise app_framework.AppFrameworkError("Error Condition: RED")
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")

    def get_user_info(self):
        try:
            with open(self.app_args.user_info_path) as user_info:
                return json.loads(user_info.read())["users"]
        except Exception as ex:
            self.logger.warning(f"USER INFO FAILURE:\n{ex}")
            return json.loads("{}")


if __name__ == "__main__":
    app = Greeter()
    result = app.execute()
    sys.exit(result)
