import sys
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

    def prepare(self):
        # Get resources, servers, etc. ready
        self.users = ["Julio", "Adela"]

    def run(self):
        # Actual application work here
        for user in self.users:
            self.logger.info("Greeting user {}.".format(user))
            print("{}, {}!".format(self.app_args.greeting, user))
        r = self.requests.get("https://jsonplaceholder.typicode.com/todos/1")
        print("Request content:\n{}".format(r.content))
        return 0

    def cleanup(self):
        # Always runs at end: pass, fail, or exception
        app_framework.errprint("Cleaning up.")


if __name__ == "__main__":
    app = SampleApp()
    result = app.execute()
    sys.exit(result)
