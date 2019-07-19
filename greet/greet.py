import random
import sys
import json
from toolbox import app_framework


# import couchdb


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
        self.parser.add_argument(
            "--user-info-server",
            action="store",
            env_var="USER_INFO_SERVER",
            default="http://localhost:8081",
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
            default="http://fruit:80/",
        )
        self.parser.add_argument(
            "--user-info-path",
            action="store",
            env_var="USER_INFO_PATH",
            # This should be a service secret, mounted to this service.
            default="/run/secrets/user_info",
        )

    def prepare(self):
        # Get resources, servers, etc. ready
        self.users = self.get_user_info()
        self.fruit_list = self.get_fruit_list()
        # self.setup_db()

    def run(self):
        # TODO: Break this up, it's way overloaded
        # Actual application work here

        # headers = {"accept": "application/json", "Content-Type": "application/json"}
        # request_data = {"title": self.app_args.default_title}

        for user in self.users:
            self.logger.info(f"Preparing to greet user {user}.")
            print(f"{self.app_args.greeting}, {user}!")

            try:
                # response = self.requests.post(
                #     # TODO: Falcon REST app: add and remove items, fetch random, etc.
                #     # TODO: I doubt this is solid or safe. What is the best target name?
                #     # TODO: Use URL mangling lib instead of concatenation?
                #     self.app_args.user_info_server + "/post",
                #     json=request_data,
                #     headers=headers,
                # )
                # response_json = response.json()
                # self.logger.debug("Request content:\n{}".format(response_json))
                # response_data = response_json.get("data") or "{}"

                title = self.users[user].get("title", "unperson")

                fruit_list = self.requests.get(self.app_args.fruit_server).json().get("fruits")
                fruit = random.choice(fruit_list)

                self.logger.info(
                    f"{user} is a {title}, and {fruit} is their favorite fruit."
                )
            except self.requests.ConnectionError as cerr:
                self.logger.warning(
                    f"Could not connect to '{self.app_args.user_info_server}' service, is it running? See application log for details."
                )
                self.logger.debug("Connection Error: {}".format(cerr))
                return 66
            except Exception as ex:
                self.logger.warning(
                    f"A severe error occurred while communicating with the '{self.app_args.user_info_server}' service. See application log for details."
                )
                self.logger.debug(f"USER INFO FAIL:\n{ex}")
                return 99

        # try:
        #     test_db_response = self.db['foo']
        #     self.logger.info(f"Database result: {test_db_response}")
        # except Exception as ex:
        #     self.logger.debug("Database Error: {}".format(ex))

        # DEBUG: raise app_framework.AppFrameworkError("Error Condition: RED")
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")

    # def setup_db(self):
    #     # Connect to a database
    #     self.db_server = couchdb.Server()
    #     if self.app_args.db_name in self.db_server:
    #         self.db = self.db_server[self.app_args.db_name]
    #     else:
    #         self.db = self.db_server.create(self.app_args.db_name)
    #     pass

    def get_fruit_list(self):
        # A stupid list of fruit, but via REST from a companion app
        # At the moment it's really a static page, as a placeholder for:
        # TODO: Move fruit list to a secret?
        try:
            fruit_list = self.requests.get(self.app_args.fruit_server).json().get("fruits")
        except Exception as ex:
            self.logger.warning(f"FRUIT FAILURE:\n{ex}")
            fruit_list = ["squash"]
        return fruit_list

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
