import time
from locust import HttpUser, task, between, TaskSet

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})

    @task
    def a(self):
        response = self.client.get("/")
        
        with self.client.get("/catch", catch_response=True) as response:
            if response.text != "":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 4:
                response.failure("Request took too long")

