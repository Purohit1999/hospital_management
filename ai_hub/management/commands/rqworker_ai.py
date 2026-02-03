from django.core.management.base import BaseCommand
from rq import Worker

from ai_hub.services.redis_conn import get_queue


class Command(BaseCommand):
    help = "Start an RQ worker for the ai queue using Redis URL settings."

    def handle(self, *args, **options):
        queue, redis_key = get_queue("ai")
        if not queue:
            self.stderr.write("Redis URL not configured. Worker cannot start.")
            return
        self.stdout.write(f"RQ worker using queue={queue.name} redis_env={redis_key or 'unknown'}")
        worker = Worker([queue], connection=queue.connection)
        worker.work()
