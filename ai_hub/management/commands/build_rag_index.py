from django.core.management.base import BaseCommand
from django.conf import settings

from ai_hub.services.rag import load_docs_from_dir, build_index


class Command(BaseCommand):
    help = "Build RAG index from ai_hub/knowledge_base documents."

    def handle(self, *args, **options):
        docs = load_docs_from_dir(settings.AI_HUB_KB_DIR)
        if not docs:
            self.stdout.write("No documents found in knowledge_base.")
            return
        result = build_index(docs, top_k=3)
        self.stdout.write(
            f"Indexed {result['count']} chunks from {len(docs)} documents."
        )
