from app import app
import threading
import webbrowser


if __name__ == '__main__':
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    app.run(port=port, debug=False)

