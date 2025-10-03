"""
Simple Redis Stream Producer using Faker for realistic data generation.

This producer generates realistic web access logs with rotating "hot" IP addresses
that change over time, creating dynamic traffic patterns that are easy to understand.
"""

import redis
import random
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List
from faker import Faker


# Configuration from environment variables
STREAM_NAME = os.environ.get('STREAM_NAME')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Validate required environment variables
if not STREAM_NAME:
    raise ValueError("STREAM_NAME environment variable is required")


class SimpleProducer:
    """Simple producer that generates realistic logs with rotating hot IPs."""

    def __init__(self) -> None:
        """Initialize the producer and establish Redis connection."""
        try:
            self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            self.r.ping()
            print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

        # Initialize Faker for realistic data
        self.fake = Faker()
        
        # Hot IP configuration - simple and effective
        self.hot_ip_pool = [
            '192.168.1.100', '10.0.0.50', '172.16.0.25', '203.0.113.10',
            '198.51.100.5', '192.0.2.15', '203.0.113.25', '198.51.100.20',
            '192.168.1.200', '10.0.0.75', '172.16.0.50', '203.0.113.30',
            '198.51.100.100', '192.0.2.100', '172.16.1.10', '10.1.1.50'
        ]
        
        # Current active hot IPs (rotates every few minutes)
        self.current_hot_ips = []
        self.hot_ip_probabilities = []
        self.last_rotation_time = 0
        self.rotation_interval = 240  # Rotate hot IPs every 4 minutes
        
        # Initialize first set of hot IPs
        self._rotate_hot_ips()

    def _rotate_hot_ips(self) -> None:
        """Rotate the set of hot IPs and their probabilities."""
        current_time = time.time()
        
        # Only rotate if enough time has passed
        if current_time - self.last_rotation_time < self.rotation_interval:
            return
            
        # Select 4-6 random IPs from the pool to be "hot"
        num_hot_ips = random.randint(4, 6)
        self.current_hot_ips = random.sample(self.hot_ip_pool, num_hot_ips)
        
        # Assign random probabilities between 3% and 12% for each hot IP
        self.hot_ip_probabilities = [
            random.uniform(0.03, 0.12) for _ in self.current_hot_ips
        ]
        
        self.last_rotation_time = current_time
        print(f"🔄 Rotated hot IPs: {dict(zip(self.current_hot_ips, [f'{p:.1%}' for p in self.hot_ip_probabilities]))}")

    def _generate_ip(self) -> str:
        """Generate an IP address with hot IP probability."""
        self._rotate_hot_ips()  # Check if we need to rotate
        
        # Check if we should return a hot IP
        for hot_ip, probability in zip(self.current_hot_ips, self.hot_ip_probabilities):
            if random.random() < probability:
                return hot_ip
        
        # Return a random IP using Faker
        return self.fake.ipv4()

    def _generate_timestamp(self) -> str:
        """Generate a timestamp with some variation for different time windows."""
        base_time = datetime.now()
        # Add small random variation: -5 to +5 minutes
        variation_minutes = random.randint(-5, 5)
        variation_seconds = random.randint(0, 59)
        
        varied_time = base_time + timedelta(minutes=variation_minutes, seconds=variation_seconds)
        return varied_time.strftime('%Y-%m-%d %H:%M:%S')

    def _generate_log(self) -> Dict[str, str]:
        """Generate a realistic access log entry using Faker."""
        return {
            'method': random.choice(['GET', 'POST', 'PUT', 'DELETE', 'PATCH']),
            'ip': self._generate_ip(),
            'path': self.fake.uri_path(),  # Faker generates realistic paths
            'timestamp': self._generate_timestamp(),
            'user_agent': self.fake.user_agent(),  # Bonus: realistic user agents
            'status_code': str(random.choices(
                [200, 404, 500, 301, 403], 
                weights=[70, 15, 5, 7, 3]  # Realistic status code distribution
            )[0])
        }

    def add_log_to_stream(self) -> None:
        """Generate a log entry and add it to the Redis stream."""
        log = self._generate_log()
        print(f"📝 {log['ip']} {log['method']} {log['path']} - {log['status_code']}")
        self.r.xadd(STREAM_NAME, log)


def main() -> None:
    """Main function to run the simple producer."""
    producer = SimpleProducer()
    try:
        print("🚀 Starting simple producer with rotating hot IPs...")
        while True:
            producer.add_log_to_stream()
            # Small delay to make output readable and create time variation
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gracefully...")
        print("Producer stopped.")


if __name__ == '__main__':
    main()
