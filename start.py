import json
import messagePipe
from logs import config
from logs.TerminalLogger import LOGGER
from API.api import app
from orm.database import DataBaseConnector

if __name__ == "__main__":
    with open(file='./config.json',mode='r',encoding='utf-8') as f:
        config_data = json.load(f)
        config.set_global(config_data)
    LOGGER.INFO('Fished config set,now start api-services......')
    try:
        app.run()
    except Exception as e:
        LOGGER.ERROR('api-services start failed')
        LOGGER.ERROR('Error is:'+e)

    LOGGER.INFO('Finished api-services-starting,not start SSE_listener...')
    db_conn = DataBaseConnector(db=config.db_path)
    pipe = messagePipe.SSE_InvokeSubProcess(sseurl=config.sse_url,cookie=config.cookie,db=db_conn)
