import threading
from flask import current_app


class AutoSync:
    def auto_sync(self):
        with current_app.test_client as client:
            # client.post(url_for('used_vacation.used'))
            print("threading")

        threading.Timer(10, self.auto_sync).start()
