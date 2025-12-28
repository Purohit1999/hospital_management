import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ai_hub.services.agent import run_compliance_agent


MISSING_MAP = {
    "diagnosis present": "Diagnosis",
    "follow-up present": "Follow-up plan",
    "medication list present": "Medication list",
}


class Command(BaseCommand):
    help = "Evaluate the compliance agent using a small local dataset."

    def handle(self, *args, **options):
        eval_path = os.path.join(
            settings.BASE_DIR, "ai_hub", "eval", "compliance_eval_set.jsonl"
        )
        if not os.path.exists(eval_path):
            self.stderr.write(
                "Eval set not found. Create ai_hub/eval/compliance_eval_set.jsonl"
            )
            return

        results = []
        total_score = 0
        total_hit_rate = 0
        count = 0

        with open(eval_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                draft = payload.get("draft", "")
                expected_missing = payload.get("expected_missing", [])

                result = run_compliance_agent(draft, use_llm=False)
                missing = _extract_missing(result.get("steps", []))

                correct = 0
                for item in expected_missing:
                    if item in missing:
                        correct += 1
                score = correct
                hit_rate = round(correct / len(expected_missing), 3) if expected_missing else 0

                results.append(
                    {
                        "expected_missing": expected_missing,
                        "missing_found": missing,
                        "score": score,
                        "hit_rate": hit_rate,
                    }
                )
                total_score += score
                total_hit_rate += hit_rate
                count += 1

        summary = {
            "avg_score": round(total_score / count, 3) if count else 0.0,
            "avg_hit_rate": round(total_hit_rate / count, 3) if count else 0.0,
            "count": count,
            "results": results,
        }

        out_path = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "agent_eval_results.json")
        os.makedirs(settings.AI_HUB_ARTIFACTS_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=True)

        self.stdout.write(
            f"Compliance eval complete. Avg score: {summary['avg_score']}. Output: {out_path}"
        )


def _extract_missing(steps):
    for step in steps:
        if step.get("step") == "VALIDATE":
            lines = step.get("output", "").splitlines()
            missing = []
            for line in lines:
                normalized = line.strip().lower()
                if normalized.endswith("no") and "present" in normalized:
                    key = normalized.replace(":", "")
                    key = key.replace(" no", "").strip()
                    mapped = MISSING_MAP.get(key)
                    if mapped:
                        missing.append(mapped)
            return missing
    return []
