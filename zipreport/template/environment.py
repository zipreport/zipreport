from jinja2 import Environment


class EnvironmentWrapper:
    def wrap(self, e: Environment) -> Environment:
        """
        Customize and return the Jinja2 Environment() object

        Note: object e is the initial Environment object created by JinjaRender()
        This function must return an environment object

        :param e: Environment
        :return: Environment
        """
        return e
