import time

from flask import Flask,Response
from orm import database
from logs import config

app = Flask(__name__)


@app.route('/topic/<tid>')
def getTopicWithComments(tid):
    results = {key:value for key,value in database.DataBaseConnector(db=config.db_path).queryTopicWithComments(tid).items()}
    return results

@app.route('/topic/versions/<tid>')
def getTopics(tid):
    results = database.DataBaseConnector(db=config.db_path).queryTopic(tid=tid)
    return {
        'results':results
    }

@app.route("/stream")
def stream():
    def event_stream():
        while True:
            time.sleep(2)
            if True:
                yield r"data:{}\n\n".format("11")
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run()