from termcolor import colored
import logging, os
import reader_handler
from flask import Flask
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

## Allow external requests
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

log = logging.getLogger('werkzeug')
log.disabled = True

main_handler = reader_handler.ReaderHandler()

@app.route("/reset")
@cross_origin()
def reset():
    """
    Stop and restart all reader thread
    :return:
    """
    print(colored("Reset received...", "blue"))
    if main_handler.reader_is_alive():
        main_handler.stop_readers()
    main_handler.start_readers()
    return "Reset OK !"

@app.route("/stop")
@cross_origin()
def stop():
    """
    Stop all reader thread
    :return:
    """
    print(colored("Stop received...", "blue"))
    if main_handler.reader_is_alive():
        main_handler.stop_readers()

    return "Stop OK !"

if __name__ == "__main__":
    try:
        print("####################")
        print(" Reader")
        print("####################")
        app.run(host=os.getenv("SERV_IP"))
    except KeyboardInterrupt:
        main_handler.stop_readers()
        print("Shutdown requested...exiting")
