import uuid
import requests
import json


class Yuno(object):

    api_version = "v1"

    def __init__(self, public_api_key, private_secret_key, sandbox):
        self.public_api_key = public_api_key
        self.private_secret_key = private_secret_key

        if not sandbox:
            self.api_base_url = "https://api.y.uno"
        else:
            self.api_base_url = "https://api-sandbox.y.uno"

    def headers(self):
        return {
            "Content-Type": "application/json",
            "charset": "utf-8",
            "Accept": "application/json",
            "private-secret-key": self.private_secret_key,
            "public-api-key": self.public_api_key,
            "X-idempotency-key": self.generate_idempotency_key(),
        }

    def base_request(self, url, method, data={}):
        base_url = self.api_base_url + "/" + self.api_version + "/"

        try:
            response = requests.request(
                method, base_url + url, data=json.dumps(data), headers=self.headers()
            )

            # return json.loads(response.content.decode("utf-8"))
            return response

        # TODO: Create especifics exceptions
        except Exception as error:
            raise

    def get(self, url, data={}):
        return self.base_request(url, "GET", data=data)

    def post(self, url, data={}):
        return self.base_request(url, "POST", data=data)

    def put(self, url, data={}):
        return self.base_request(url, "PUT", data=data)

    def generate_idempotency_key(self):
        return str(uuid.uuid4())
