from base64 import b64decode
from pathlib import Path

import environ

from libnftinema.structs import ClientKey

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()


SECRET_KEY = "your_secret_key"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "libnftinema.testapp",
]
AUTH_USER_MODEL = "testapp.TestUser"
MIDDLEWARE = []
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}
USE_I18N = False
USE_L10N = False
USE_TZ = False

ROOT_URLCONF = "libnftinema.testapp.urls"

NFTINEMA_CHECK_API_CLIENT_HANDLER = env.str(
    "NFTINEMA_CHECK_API_CLIENT_HANDLER",
    "libnftinema.testapp.handlers.check_api_client_test",
)


NFTINEMA_CLIENT_KEY = ClientKey(
    "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJrdHkiOiJvY3QiLCJrIjoiRGZra3h1ZVZTVnl3TmJfSW9lVU5WOG5fUjBFclcwVUVtaTB6aGRCY01TVSIsImFsZyI6IkhTMjU2Iiwia2lkIjoiYXBpX2NsaWVudF9Bb1l6blB6ckhNTXY0b1IydkZqU1FDIn0.",
)
PASSPORT_PUBLIC_KEY = (
    b64decode(
        "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBc0xQTHdpT0pXNmZPVURvRksvSjBcbnpIb2hBN2VPMGhDZis5cEVYayt1alRFL213bEdUMFhRdFQwSjhlYjBPY005Sjg0Z1Jid1VhMGlCcFoxYmdBMDlcbnBnQWNJeFVzSmt4M1dKVHI5cW9kTzd4d2FHQ3FWVlEwMjZIR2FmNGZrSUE5YTUrQWF2S2NTeFVTdURmK2JMUHNcbjZDbUFyRGdmRkNUd1VLcFhXUHVjS1hHRXgyMEVEVGU3U2JzWExCN1FCL1FxaXpFQlJ5NXBNdFU4S2hraW9GVHFcbjA4SUt3eVJBTVltbHNSVFlZYjBEeVBYa2xrOVpvdUx0U1hORlpscWpZL2pOekRIdlNtOXBpSFJmekc3SllRZitcbk1rVVQzWmJwWEZORjBwSFlFRTkrcTYvYThlMjNwYnA2cFFyNVo4Sk5hSi96cHhRSXJkOThwWDAyZ25tYVVmZzZcbkdRSURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS0=",
    )
    .decode()
    .replace("\\n", "\n")
)

USER_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MjQxMTQyOTgsImV4cCI6MjAzOTQ3NDI5OCwidXNlcl91dWlkIjoiMTQ3Zjk0MzQtY2Q5NS00ZmFhLWJmNjgtZTYyMTk5YzYxOTFkIiwidGFyZ2V0X2FjY2VzcyI6Im1haW4iLCJjb3VudHJ5X2lzbyI6IlVTIn0.GXwf5taLnyfqaCx7QI00HCaU0ddHFJUUxNe9Ld7DDIkMxTmjMaNkeevibbaQ_9TXLgrD3xH6oor6Pi0sEtqJzh1pgqnpwlZVxsHfM8cnJCdYiTM1xqFHziwSvXMhM4Hkt6HCq8G6njqB-nWzeoKyWhfTRu-HVOOy5zEzUm4AqQfGM6CMDW4m1G90TvsSrrqzuBdTDddqoPcDwAeyzJ5xV3XlWEXiMruGzSCaMpDUimGCXKdYulUEm0q_u9ETNzpatq-WSKQLvo3331vuZ9UjVTe_P3ahV0YSN4yFBYBbdeyoNdbzr8L5BdowNryBnc6AvFWzWgRy290wvg96gWRWGw"
