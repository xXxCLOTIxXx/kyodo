from .exceptions import checkException
from . import log
from .generators import generate_x_signature, random_ascii_string
from .constants import api_url, app_id, app_version

from aiohttp import ClientSession, ClientResponse
from json import dumps
from time import time as timestamp

class Requester:
	"""
	Main class for handling HTTPS requests in the Kyodo API library.

	This class is responsible for making HTTP requests to the Kyodo servers, managing headers, and providing 
	convenience methods for interaction with the API

	### Args:

		user_agent (str): 
			The User-Agent string sent in HTTP requests. It identifies the client software making the request.
		
		language (str): 
			The language code used for API requests and responses. It influences the language in which the responses are returned.
		
		timezone (str): 
			The timezone string (e.g., "Europe/Oslo", "Asia/Tokyo"). This may affect how dates and times are formatted and returned by the server.
		
		deviceId (str | None, optional): 
			A unique identifier for the device. If not provided, it will be generated.
	
	### Attributes:	
		user_agent (str): 
			The User-Agent string used in HTTP request headers.
		
		language (str): 
			The language used for API communication.
		
		timezone (str): 
			The timezone setting used in API requests.
		
		deviceId (str | None): 
			The device identifier.

	This class is used internally by the `Client` to manage HTTP requests and communicate with Kyodo servers.
	"""
	
	def __init__(self, user_agent: str, language: str, timezone: str, deviceId: str | None = None, sig_service_token: str | None = None):
		self.user_agent: str = user_agent
		self.timezone: str = timezone
		self.language: str = language
		self.token: str = None
		self.deviceId: str = deviceId or random_ascii_string(26)
		self.sig_service_token: str = sig_service_token


	def headers(self, headers: dict = None, content_type: str = "application/json") -> dict:
		t = int(timestamp())

		default_headers = {
			"user-agent": self.user_agent,
			"Accept": "application/json",
			"app-id": app_id,
			"app-version": app_version,
			"device-language": self.language,
			"device-timezone": self.timezone,
			"Accept-Language": self.language,
			"start-time": str(t),
			"device-id": self.deviceId,
			"x-signature": generate_x_signature(t, self.sig_service_token)
		}
		if content_type: default_headers["content-type"] = content_type
		if self.token: default_headers["Authorization"] = self.token

		if headers: default_headers.update(headers)
		return default_headers


	async def make_async_request(self, method: str, endpoint: str = None, body: dict | bytes = None, allowed_code: int = 200, headers: dict = None , api: str = None) -> ClientResponse:
		async with ClientSession() as asyncSession:
			response = await asyncSession.request(method, f"{api or api_url}{endpoint or ''}", data=dumps(body) if isinstance(body, dict) else body if body is not None else None, headers=self.headers(headers))
			log.debug(f"[https][{method}][{endpoint or ''}][{response.status}]: {len(body) if isinstance(body, bytes) else body}")
			return checkException(await response.text()) if response.status != allowed_code else response