from django.test import SimpleTestCase

from .services.rag import chunk_text
from .services.agent import run_compliance_agent
from .services.ml import predict_no_show


class RagTests(SimpleTestCase):
    def test_chunking(self):
        text = "a" * 2000
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        self.assertTrue(len(chunks) >= 3)


class AgentTests(SimpleTestCase):
    def test_agent_trace(self):
        result = run_compliance_agent("Test discharge summary", use_llm=False)
        steps = result["steps"]
        self.assertTrue(len(steps) >= 3)


class MlTests(SimpleTestCase):
    def test_no_show_score_range(self):
        score = predict_no_show({"days_until": 3, "hour": 10})
        self.assertTrue(0.0 <= score <= 1.0)
