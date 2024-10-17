# header placeholder

__module__ = "tests.exceptions"

class CommandExecutionError(RuntimeError):
	"""
	Exception raised when a command execution fails.

	Attributes:
		message (str) -- Description of the error.
		exit_code (int) -- The exit code associated with the error.

	Meta-Testing:

		Testcase 1: Initialization with message and exit code.
			A. - Initializes the error.
			B. - checks inheritance.
			C. - checks each attribute.

			>>> error = CommandExecutionError("Failed to execute command", exit_code=1)
			>>> isinstance(error, RuntimeError)
			True
			>>> error.message
			'Failed to execute command'
			>>> error.exit_code
			1
	"""

	def __init__(self, message, exit_code, *args, **kwargs):
		"""
		Initialize CommandExecutionError with a message and exit code.

		Parameters:
			message (str) -- Description of the error.
			exit_code (int) -- The exit code associated with the error.
			*args: Variable length argument list.
			**kwargs: Arbitrary keyword arguments.

		Meta-Testing:

			Testcase 1: Initialization with different exit code:
				 A. - Initializes a CommandExecutionError with a specific exit code.
				 B. - Checks the message is still set, as super class would.
				 C. - check the specific exit code is 2.

				>>> error = CommandExecutionError("Error message", 2)
				>>> error.message
				'Error message'
				>>> error.exit_code
				2
		"""
		super().__init__(message, *args, **kwargs)
		self.exit_code = exit_code

