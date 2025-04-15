<body>
 	<h1 align="center">
		<img src="https://github.com/xXxCLOTIxXx/kyodo/blob/main/docs/res/banner.png" alt="kyodo api">
	</h1>
	<p align="center">
	    <a href="https://github.com/xXxCLOTIxXx/kyodo/releases"><img src="https://img.shields.io/github/v/release/xXxCLOTIxXx/kyodo" alt="GitHub release" />
	    <a href="https://pypi.org/project/kyodo/"><img src="https://img.shields.io/pypi/v/kyodo.svg" alt="Pypi version" />
	    <img src="https://img.shields.io/pypi/dm/kyodo"/>
	    <a href="https://github.com/xXxCLOTIxXx/kyodo/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="license" /></a>
	    <a href="https://github.com/xXxCLOTIxXx/kyodo/blob/main/docs/index.md"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https://github.com/xXxCLOTIxXx/kyodo/blob/main/docs/index.md" alt="docs" /></a>
	</p>
	<div align="center">
		<a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/sponsor.md">
			<img src="https://img.shields.io/static/v1?style=for-the-badge&label=Sponsor project&message=%E2%9D%A4&color=ff69b4" alt="Sponsor project"/>
		</a>
		<a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/contacts.md">
      		<img src="https://img.shields.io/badge/Контакты-Contacts-F79B1F?style=for-the-badge&amp;logoColor=0077b6&amp;color=0077b6" alt="Contacts"/>
		</a>
	</div>
	<br>
<div align="center">
	
# Kyodo – Python library for creating bots on the social network "[Hi Kyodo](https://hi.kyodo.app/)"

Powered by <a href="https://kyodo-service.onrender.com/">kyodo-service</a> x-sig generator
</a>
</div>

<div align="center">
	
## A simple example of logging in and listing chats on an account
</div>

```python
from kyodo import Client
import asyncio
from ast import literal_eval

client = Client(socket_enable=False)

async def main():
    try:await client.login(email="gmail@gmail.com", password="password")
    except Exception as e:
        print("LOGIN ERROR:", literal_eval(str(e))["message"])
        exit()
    
    """
    During the login process, you may be required to confirm your account — 
    follow the link sent to your email, then try logging in again.

    Once logged in successfully, save the received token.
    In the future, it is recommended to use client.login_token("token") 
    to avoid entering your email and password again.
    """


    print(f"Loginned as {client.me.nickname}\nTOKEN: {client.token}")
    print("My chats:")
    chats_list = await client.get_my_chats()
    for chat in chats_list.chats:
        print(chat.name, " -> ", chat.chatId)

if __name__ == "__main__":
    asyncio.run(main())   
```

<div align="center">

#
## Example of chat event handling
</div>

```python
from kyodo import Client, EventType, ChatMessage
import asyncio

client = Client()
TOKEN="account.auth.token"

@client.event(EventType.ChatMessage)
async def on_message(msg: ChatMessage):
    print(f"{msg.author.nickname}: {msg.content}")

@client.event(EventType.ChatMemberJoin)
async def on_member_join(msg: ChatMessage):
    print(f"New chat member: {msg.author.nickname} [chat -> {msg.chatId}]")


@client.command(["/ping"])
async def on_bot_ping(msg: ChatMessage):
    await client.send_message(msg.circleId, msg.chatId, "Pong!", msg.messageId)

async def main():
    await client.login_token(TOKEN)
    await client.socket_wait()

if __name__ == "__main__":
    asyncio.run(main())
```

<div align="center">
	<a href="https://github.com/xXxCLOTIxXx/kyodo/blob/main/docs/index.md">
		<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=1&pause=31&color=3DACF7&random=false&width=195&lines=Read+the+documentation" alt="Read the documentation"/>
	</a>
</div>
</body>
