from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse, ClientConnectionError, WSServerHandshakeError
from asyncio import create_task
from asyncio import sleep as asleep
from json import loads, dumps


from ..utils import log, exceptions
from ..utils.constants import ws_api
from .socket_handler import Handler

class Socket(Handler):

	"""
	Module for working with kyodo socket in real time. Not used separately from the client.
	"""

	token: str
	deviceId: str

	socket_enable: bool
	error_trace: bool

	def __init__(self):
		self.connection: ClientWebSocketResponse = None
		self.task_receiver = None
		self.task_pinger = None
		self.ws_client_session = None

		Handler.__init__(self)
	

	async def ws_on_close(self, code: int, reason: str) -> None:
		log.debug("[ws][close] Closed with code %s and reason %s", code, reason)
		self.task_receiver.cancel()


	async def ws_resolve(self):
		while True:
			try:
				msg = await self.connection.receive()
				if msg.type != WSMsgType.TEXT: continue
				try:data = loads(msg.data)
				except:
					log.debug(f"[ws][recive] The socket received an unreadable message: {data}")
					continue

				log.debug(f"[ws][recive]: {data}")
				await self.handle_data(data)
			except (WSServerHandshakeError, ClientConnectionError) as e:
				self.ws_on_close(e.code, e.message)
				return

	async def ws_connect(self):
		"""
		Connect to web socket
		"""
		if self.connection:
			log.debug(f"[ws][start] The socket is already running.")
			return
		
		if not self.token:
			raise exceptions.NeedAuthError
		
		try:
			self.ws_client_session = ClientSession(base_url=ws_api)
			self.connection = await self.ws_client_session.ws_connect(
				f"/?token={self.token}&deviceId={self.deviceId}"
			)
			self.task_receiver = create_task(self.ws_resolve())
			self.task_pinger = create_task(self.__pinger())
			log.debug(f"[ws][start] Socket Started")
		except Exception as e:
			from traceback import format_exc
			log.critical(f"[ws][start] Error while starting Socket : {e} {'' if not self.error_trace else f'\n{format_exc()}'}")


	async def ws_disconnect(self):
		"""
		Disconnect from websocket
		"""
		if self.connection:
			log.debug(f"[ws][stop] closing socket...")
			try:
				self.task_receiver.cancel()
				self.task_pinger.cancel()
				await self.connection.close()
				self.connection = None
				await self.ws_client_session.close()
				self.ws_client_session = None
			except Exception as e:
				log.debug(f"[ws][stop] Error while closing Socket : {e}")
		else:
			log.debug(f"[ws][stop] Socket not running.")


	async def __pinger(self):
		while self.connection:
			try:
				await self.ws_send('{"o":7,"d":{}}')
			except Exception as e:
				log.debug(f"[ws][pinger] Ping error: {e}")
			await asleep(10)

	async def ws_send(self, data: str | dict):
		"""
		Send message to websocket
		"""
		if self.connection is None:
			log.debug("[ws][stop] Socket not running.")
			return
		
		log.debug(f"[ws][send]: {data}")
		await self.connection.send_str(
			data if isinstance(data, str) else dumps(data)
		)

	async def socket_wait(self):
		"""
		Starts a loop that continuously listens for new messages from the WebSocket connection.
		
		This method is used to keep the program running and process incoming messages in real-time. 
		It ensures that the WebSocket connection remains open, and the program doesn't exit unexpectedly while 
		awaiting messages. 

		The loop will run as long as `self.socket_enable` is True. The method sleeps for 3 seconds between 
		iterations to prevent unnecessary CPU usage while waiting for new data.

		Example:
			await client.socket_wait()
		"""
		while self.socket_enable:
			await asleep(3)