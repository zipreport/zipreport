from argparse import ArgumentParser


class ArgParser(ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.failed = False
        self.error_message = ""

    def error(self, message):
        self.failed = True
        self.error_message = message

    def format_parameters(self):
        formatter = self._get_formatter()

        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # determine help from format above
        return formatter.format_help()
