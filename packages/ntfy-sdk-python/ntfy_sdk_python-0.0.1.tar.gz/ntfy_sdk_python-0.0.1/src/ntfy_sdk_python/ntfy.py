import requests


class Ntfy:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def publish(self, message, topic):

        if not topic:
            raise ValueError("Topic is required")

        payload = {"message": message}

        if self.token:
            headers = {
                "Authorization": f"Bearer {self.token}",
            }

        requests.post(
            self.url + "/" + topic,
            headers=headers,
            json=payload,
        )
