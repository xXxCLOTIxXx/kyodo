from .logger import Logger, logging
from .exceptions import NeedAuthError
from .constants import SIG_GEN_API, SIG_GEN_TOKEN
from requests import get
from sys import exit


log = Logger()

def require_auth(func):
    def wrapper(self, *args, **kwargs):
        if not getattr(self, "token", ""):
            raise NeedAuthError(
                "You need to be authorized to use this method"
            )
        return func(self, *args, **kwargs)

    return wrapper


def require_uid(func):
    def wrapper(self, *args, **kwargs):
        if not getattr(self.me, "userId", ""):
            raise NeedAuthError(
                "Your account ID is required. Login via token does not provide information about your ID. To specify your ID use: client.me.userId = 'your_id'"
            )
        return func(self, *args, **kwargs)

    return wrapper




def check_gen_service():
    result = get(f"{SIG_GEN_API}/service/ping")
    if result.status_code == 200:
        data: dict = result.json()
        if data.get("alive") is False:
            log.critical("The signature generation service is undergoing maintenance or is temporarily down.")
            exit()
    else:
        log.critical("The signature generation service is not responding. It may no longer be active. Please check for the latest version of the library.")
        exit()
