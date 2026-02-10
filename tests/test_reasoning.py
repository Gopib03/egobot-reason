
import pytest
from src.utils.helpers import Config
from src.core.cosmos_client import CosmosClient
from src.core.reasoning_engine import ReasoningEngine
from src.evaluation.benchmark import BenchmarkRunner


class TestCosmosClient:
    def test_no_key_raises(self):
        with pytest.raises(ValueError):
            CosmosClient(Config(nvidia_api_key=""))

    def test_parse_with_tags(self):
        r, a = CosmosClient._parse_reasoning("<think>\nthought\n</think>\nanswer")
        assert r == "thought"
        assert a == "answer"

    def test_parse_without_tags(self):
        r, a = CosmosClient._parse_reasoning("plain text")
        assert r == ""
        assert a == "plain text"


class TestReasoningEngine:
    def test_modes_exist(self):
        assert "social" in ReasoningEngine.available_modes()
        assert "safety" in ReasoningEngine.available_modes()

    def test_bad_mode(self):
        with pytest.raises(ValueError):
            ReasoningEngine._get_prompts("fake")

    def test_json_parsing(self):
        res = ReasoningEngine._format_result("social", {
            "reasoning": "x", "answer": '{"intent":"handover"}', "usage": {}
        })
        assert res["parsed"]["intent"] == "handover"

    def test_invalid_json(self):
        res = ReasoningEngine._format_result("social", {
            "reasoning": "x", "answer": "not json", "usage": {}
        })
        assert res["parsed"] is None


class TestBenchmark:
    def test_compare_match(self):
        r = BenchmarkRunner._compare({"a": "b"}, {"a": "b"})
        assert r["all_match"]

    def test_compare_mismatch(self):
        r = BenchmarkRunner._compare({"a": "x"}, {"a": "b"})
        assert not r["all_match"]

    def test_summarize(self):
        s = BenchmarkRunner._summarize([
            {"status": "pass", "elapsed_sec": 1},
            {"status": "fail", "elapsed_sec": 2},
        ])
        assert s["total"] == 2
        assert s["accuracy"] == 0.5