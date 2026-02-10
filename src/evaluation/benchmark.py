
import json
import logging
import time
from pathlib import Path
from src.core.reasoning_engine import ReasoningEngine
from src.utils.helpers import Config

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, config=None):
        self.config = config or Config()
        self.engine = ReasoningEngine(self.config)

    def load_test_cases(self, dataset_path):
        path = Path(dataset_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")
        with open(path) as f:
            return json.load(f)

    def run(self, test_cases, output_dir="results"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []
        for i, case in enumerate(test_cases):
            test_id = case.get("test_id", f"test_{i}")
            mode = case.get("mode", "social")
            image = case.get("image", "")
            expected = case.get("expected", {})
            try:
                start = time.time()
                result = self.engine.analyze_image(image, mode=mode)
                elapsed = time.time() - start
                matches = self._compare(result.get("parsed"), expected)
                results.append({
                    "test_id": test_id, "mode": mode,
                    "status": "pass" if matches["all_match"] else "fail",
                    "matches": matches, "elapsed_sec": round(elapsed, 2),
                    "parsed": result.get("parsed"), "expected": expected,
                })
            except Exception as e:
                results.append({"test_id": test_id, "mode": mode, "status": "error", "error": str(e)})

        summary = self._summarize(results)
        with open(Path(output_dir) / "benchmark_results.json", "w") as f:
            json.dump({"summary": summary, "results": results}, f, indent=2)
        return summary

    @staticmethod
    def _compare(parsed, expected):
        if not parsed or not expected:
            return {"all_match": not expected, "details": {}}
        details = {}
        all_match = True
        for key, expected_val in expected.items():
            actual_val = parsed.get(key)
            if isinstance(expected_val, bool):
                match = actual_val is expected_val
            elif isinstance(expected_val, str):
                match = str(actual_val).lower().strip() == expected_val.lower().strip()
            else:
                match = actual_val == expected_val
            details[key] = {"expected": expected_val, "actual": actual_val, "match": match}
            if not match:
                all_match = False
        return {"all_match": all_match, "details": details}

    @staticmethod
    def _summarize(results):
        total = len(results)
        passed = sum(1 for r in results if r.get("status") == "pass")
        failed = sum(1 for r in results if r.get("status") == "fail")
        errors = sum(1 for r in results if r.get("status") == "error")
        elapsed_list = [r["elapsed_sec"] for r in results if "elapsed_sec" in r]
        avg_time = sum(elapsed_list) / len(elapsed_list) if elapsed_list else 0
        return {
            "total": total, "passed": passed, "failed": failed, "errors": errors,
            "accuracy": round(passed / total, 4) if total > 0 else 0,
            "avg_latency_sec": round(avg_time, 2),
        }
