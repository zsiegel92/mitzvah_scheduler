import os

import redis
from rq import Worker, Queue, Connection
listen = ['default']

from app_factory import create_app
redis_url = os.getenv('REDISTOGO_URL')

conn = redis.from_url(redis_url)


def main():
	#DB io should be OKAY
	with create_app().app_context():
		with Connection(conn):
			worker = Worker(list(map(Queue, listen)))
			worker.work()

if __name__ == '__main__':
	main()
