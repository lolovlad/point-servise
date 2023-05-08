from Server.app import app
import uvicorn
from settings import settings

uvicorn.run("Server.app:app", host=settings.host_server, port=settings.port_server)
