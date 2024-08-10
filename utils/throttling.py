# throttling.py
import time
from collections import defaultdict
from fastapi import Request, HTTPException

class AdaptiveThrottling:
    def __init__(self, base_backoff: int = 1, max_backoff: int = 60):
        """
        Initialize the AdaptiveThrottling class.

        Args:
            base_backoff (int): The base backoff time in seconds.
            max_backoff (int): The maximum backoff time in seconds.
        """
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.request_frequency = defaultdict(list)
        self.error_count = defaultdict(int)

    def calculate_backoff(self, client_ip):
        """
        Calculate the backoff time based on the client's error count.

        Args:
            client_ip (str): The IP address of the client.

        Returns:
            int: The calculated backoff time in seconds.
        """
        error_count = self.error_count[client_ip]
        backoff_time = min(self.base_backoff * (2 ** error_count), self.max_backoff)
        return backoff_time

    async def check_rate_limit(self, request: Request):
        """
        Check if the client has exceeded the rate limit.

        Args:
            request (Request): The incoming request.

        Raises:
            HTTPException: If the client has exceeded the rate limit, a 429 status is raised.
        """
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old requests outside the time window (optional, based on your logic)
        self.request_frequency[client_ip] = [
            t for t in self.request_frequency[client_ip]
            if current_time - t < 60
        ]

        # Track current request
        self.request_frequency[client_ip].append(current_time)

        # Adjust based on errors
        if self.error_count[client_ip] > 0:
            retry_after = self.calculate_backoff(client_ip)
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests, please retry later",
                headers={"Retry-After": str(int(retry_after))}
            )

    def record_error(self, client_ip):
        """
        Increment the error count for a specific client.

        Args:
            client_ip (str): The IP address of the client.
        """
        self.error_count[client_ip] += 1

    def reset_error_count(self, client_ip):
        """
        Reset the error count for a specific client.

        Args:
            client_ip (str): The IP address of the client.
        """
        self.error_count[client_ip] = 0
