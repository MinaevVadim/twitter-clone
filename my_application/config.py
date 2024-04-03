from typing import Optional

from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD_DB: Optional[str] = os.environ.get('PASSWORD_DB')
LOGIN_DB: Optional[str] = os.environ.get('LOGIN_DB')
PORT_DB: Optional[str] = os.environ.get('PORT_DB')
HOST_DB: Optional[str] = os.environ.get('HOST_DB')
NAME_DB: Optional[str] = os.environ.get('NAME_DB')
