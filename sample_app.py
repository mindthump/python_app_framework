import sys
# import os
import app_framework
# import toolbox


class SampleApp(app_framework.AppFramework):
    def __init__(self):
        super(SampleApp, self).__init__()

    def additional_arguments(self):
        self.parser.add_argument(
            "--something",
            action="store",
            env_var="SOMETHING",
            default="e854ac52fca74c9eb0495589727a63b0",
        )

    def prepare(self):
        pass

    def run(self):
        pass

    def cleanup(self):
        pass


if __name__ == "__main__":
    # Get an application instance.
    app = SampleApp()
    # Since this subclass doesn't override execute(), this gives control to the superclass
    result = app.execute()
    sys.exit(result)
