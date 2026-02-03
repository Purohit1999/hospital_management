from django.core.management.base import BaseCommand
from rq import Worker, Queue

from ai_hub.services.redis_conn import get_redis_connection


class Command(BaseCommand):
    help = "Start an RQ worker for the ai queue using Redis URL settings."

    def handle(self, *args, **options):
        redis_conn = get_redis_connection()
        if not redis_conn:
            self.stderr.write("Redis URL not configured. Worker cannot start.")
            return
        queue = Queue("ai", connection=redis_conn)
        worker = Worker([queue], connection=redis_conn)
        worker.work()
