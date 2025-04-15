from json import loads, JSONDecodeError





class RemoteGeneratorError(Exception):
	"""
	Base class for all remote signature generator errors.
	"""
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class GeneratorServiceUnavailable(RemoteGeneratorError):
	"""
	Called when the remote signature generation server does not respond.
	"""


#++++++++++++++++++++++++++++++++++++++++++++++++++++=


class KyodoError(Exception):
	"""
	Base class for all kyodo-related errors.
	"""
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class LibraryError(Exception):
	"""
	Base class for all library-related errors.
	"""
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)
#++++++++++++++++++++++++++++++++++++++++++++++++++++=




class UnknownError(LibraryError):
	"""
	An unknown error occurred.
	"""

class NeedAuthError(LibraryError):
	"""
	Called when an attempt is made to perform an action that requires authorization.
	"""


class UnsupportedArgumentType(LibraryError):
	"""
	Called when you pass an unsupported argument type.
	"""


class UnsupportedFileType(LibraryError):
	"""
	Called when you pass an unsupported file type.
	"""

class ArgumentNeeded(LibraryError):
	"""
	Called when no arguments are passed or a required argument is missing.
	"""

class NoDataError(LibraryError):
	"""
	Called when the final data for a request is empty (all arguments are None).
	"""



#=====================================================



class NotFoundError(KyodoError):
	"""
	Called if the resource is not found.
	"""


class ForbiddenError(KyodoError):
	"""
	Called when the server denies an action.
	"""


class TooManyRequestsError(KyodoError):
	"""
	Called when you send too many requests in a short period of time (just put a sleep for 2 seconds)
	"""


class AccessRestricted(KyodoError):
	"""
	Called when there is insufficient permission to execute the request.
	"""



errors = {
	"0:404": NotFoundError,
	"0:403": ForbiddenError,
	"0:419": AccessRestricted,
	"0:429": TooManyRequestsError,
}

def checkException(data):
	try:
		data = loads(data)
		apiCode = data.get("apiCode")
		code = data.get("code")
		_ = f"{apiCode}:{code}"
	except JSONDecodeError:
		raise UnknownError(data)
	if _ in errors: raise errors[_](data)
	else:raise UnknownError(data)