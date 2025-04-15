from ..utils import log
from traceback import format_exc
from ..objects import EventType, ChatMessage, BaseEvent

class Handler:
	
	"""
	Additional module to socket for creating event handlers
	"""
	handlers: dict = {}
	error_trace: bool

	async def handle_data(self, _data: dict):
		data: dict = _data.get("d", {})
		_o = _o = _data.get("o")
		await self.call(data, _o)



	async def call(self, data: dict, type: str):

		match type:
			case EventType.ChatMessage:
				sub_type = data.get("message", {}).get("type")
				data = ChatMessage(data)
			case _:
				sub_type = None
				data = BaseEvent(data, type)



		if type in self.handlers or EventType.ANY in self.handlers or f"{type}:{sub_type}" in self.handlers:

			for i in (EventType.ANY, type, f"{type}:{sub_type}"):
				if i not in self.handlers:
					continue
				for func in self.handlers[i]:
					try:
						await func(data)
					except Exception as e:
						log.error(f"[ws][event][{func}]Error: {e}{'' if not self.error_trace else f'\n{format_exc()}'}")

	def event(self, type: str | int):
		"""
		Decorator for registering an event handler.

		:param type: Event type string or kyodo.EventType.ANY.
		:return: Decorator function.
		"""
		def registerHandler(handler):
			self.add_handler(type, handler)
			return handler
		return registerHandler

	def add_handler(self, type: str | int, handler):
		"""
		Registers an event handler for a specific event type.

		:param type: Event type string or kyodo.EventType.ANY.
		:param handler: Function to handle the event.
		:return: The registered handler.
		"""
		if type in self.handlers:
			self.handlers[type].append(handler)
		else:
			self.handlers[type] = [handler]
		return handler

	@staticmethod
	def command_validator(commands: list[str], handler):
		async def wrapped_handler(data: ChatMessage):
			if not isinstance(data.content, str):
				return
			
			message_content = data.content.lower()
			for command in commands:
				if message_content.startswith(command.lower()):
					data.content = data.content[len(command):].strip()
					await handler(data)
					break
		return wrapped_handler

	def command(self, commands: list):
		"""
		Decorator for registering a command handler.

		:param commands: List of commands.
		:return: Decorator function.
		"""
		def registerCommands(handler):
			self.add_command(commands, handler)
			return handler
		return registerCommands

	def add_command(self, commands: list, handler):
		"""
		Registers a command handler for processing messages.

		:param commands: List of commands.
		:param handler: Function to execute when a command is detected.
		:return: Command validator function.
		"""
		if EventType.ChatTextMessage in self.handlers:
			self.handlers[EventType.ChatTextMessage].append(self.command_validator(commands, handler))
		else:
			self.handlers[EventType.ChatTextMessage] = [self.command_validator(commands, handler)]
		return self.command_validator


