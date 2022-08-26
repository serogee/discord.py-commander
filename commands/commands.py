import re
from context import Flags, Context

class Command:

    def __init__(self, callback, parent, aliases: list=[], mention_as_prefix=False, case_sensitive=False) -> None:
        self.group = parent
        self.callback = callback
        self.name = callback.__name__
        self.description = callback.__doc__
        self.parent = parent
        self.aliases = aliases
        self.triggers = [self.name, *aliases]
        self.mention_as_prefix = mention_as_prefix
        self.case_sensitive = case_sensitive
        if case_sensitive:
            self.regex = fr"{'|'.join([re.escape(trigger) for trigger in self.triggers])}"
        else:
            self.regex = fr"(?i:{'|'.join([re.escape(trigger) for trigger in triggers])})"
        

class FlaggedCommand(Command):

    def __init__(self, callback, parent, aliases: list = [], flags: list = [], inputs: list = [], mention_as_prefix=False, case_sensitive=False) -> None:
        super().__init__(callback, parent, aliases, mention_as_prefix, case_sensitive)
        _flags = []
        for _, __, inp in inputs:
            _flags.append(inp)
        for flag, *_ in flags:
            _flags.append(fr"({re.escape(flag)})")
        self.re = re.compile(fr"^[ \n]*(?P<_TRIGGER>{regex})(?P<_FLAGS>(?i:[^ \t\n\u200b]*?(?:{'|'.join(_flags)}))*[^ \t\n\u200b]*)[ \t\n\u200b]*(?P<_CONTENT>.*)$", re.DOTALL)
        