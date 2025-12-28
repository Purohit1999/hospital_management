import json
import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from ai_hub.services.rag import retrieve


class Command(BaseCommand):
    help = "Evaluate RAG retrieval on a small local dataset."

    def handle(self, *args, **options):
        eval_path = os.path.join(settings.BASE_DIR, "ai_hub", "eval", "rag_eval_set.jsonl")
        if not os.path.exists(eval_path):
            self.stderr.write("Eval set not found. Create ai_hub/eval/rag_eval_set.jsonl")
            return

        total = 0
        passed = 0
        latency_sum = 0
        failures = []
        results = []

        with open(eval_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                question = payload.get("question", "")
                expected = payload.get("expected_keywords", [])
                min_hits = int(payload.get("min_hits", 1))

                citations, latency_ms = retrieve(question, top_k=3)
                latency_sum += latency_ms

                combined = " ".join(
                    [
                        f"{c.get('text', '')} {c.get('snippet', '')}"
                        for c in citations
                    ]
                ).lower()

                hits = 0
                for kw in expected:
                    if kw.lower() in combined:
                        hits += 1
                is_pass = hits >= min_hits
                total += 1
                if is_pass:
                    passed += 1
                else:
                    failures.append({"question": question, "hits": hits})

                results.append(
                    {
                        "question": question,
                        "hits": hits,
                        "min_hits": min_hits,
                        "pass": is_pass,
                        "latency_ms": latency_ms,
                    }
                )

        pass_rate = round(passed / total, 3) if total else 0.0
        avg_latency_ms = int(latency_sum / total) if total else 0
        summary = {
            "pass_rate": pass_rate,
            "avg_latency_ms": avg_latency_ms,
            "failing_count": len(failures),
            "failures": failures[:3],
            "results": results,
        }

        out_path = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "rag_eval_results.json")
        os.makedirs(settings.AI_HUB_ARTIFACTS_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=True)

        self.stdout.write(f"RAG eval complete. Pass rate: {pass_rate}. Output: {out_path}")
