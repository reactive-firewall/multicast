# header placeholder

__module__ = "tests.exceptions"

class CommandExecutionError(RuntimeError):
	def __init__(self, message, exit_code, *args, **kwargs):
		super().__init__(message, *args, **kwargs)
		self.exit_code = exit_code