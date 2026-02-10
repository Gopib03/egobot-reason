
import json
import logging
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from src.core.reasoning_engine import ReasoningEngine
from src.core.action_planner import ActionPlanner
from src.evaluation.benchmark import BenchmarkRunner
from src.utils.helpers import Config

console = Console()


def _setup_logging(verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@click.group()
@click.option("--verbose", "-v", is_flag=True)
def main(verbose):
    """EgoBot Reason — Egocentric Robot Reasoning with Cosmos Reason 2."""
    _setup_logging(verbose)


@main.command()
@click.option("--image", type=click.Path(exists=True))
@click.option("--video", type=click.Path(exists=True))
@click.option("--image-url", type=str)
@click.option("--mode", type=click.Choice(["social","handover","spatial","trajectory","safety","thrown_object","planning","full"], case_sensitive=False), default="social")
@click.option("--task", type=str, default=None)
@click.option("--output", "-o", type=click.Path(), default=None)
def analyze(image, video, image_url, mode, task, output):
    """Analyze an image or video using Cosmos Reason 2."""
    config = Config()
    engine = ReasoningEngine(config)

    if not image and not video and not image_url:
        console.print("[red]Error: Provide --image, --video, or --image-url[/red]")
        sys.exit(1)

    console.print(Panel(f"Mode: [bold]{mode}[/bold]", title="EgoBot Reason"))

    try:
        if mode == "full":
            result = engine.full_analysis(image or video)
        elif task and image:
            result = ActionPlanner(config).plan_multi_step(image, task)
        elif video:
            result = engine.analyze_video(video, mode=mode)
        elif image_url:
            result = engine.analyze_image_url(image_url, mode=mode)
        else:
            result = engine.analyze_image(image, mode=mode)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    # Display
    reasoning = result.get("reasoning", "")
    if reasoning:
        console.print(Panel(reasoning[:2000], title="Reasoning", border_style="blue"))
    parsed = result.get("parsed")
    if parsed:
        console.print(Panel(Syntax(json.dumps(parsed, indent=2), "json", theme="monokai"), title="Output", border_style="green"))
    else:
        console.print(Panel(result.get("answer", "")[:3000], title="Answer", border_style="yellow"))

    if result.get("type") == "full_analysis":
        for name, sub in result.get("results", {}).items():
            console.print(f"\n[bold]-- {name.upper()} --[/bold]")
            if sub.get("parsed"):
                console.print(json.dumps(sub["parsed"], indent=2))

    if output:
        with open(output, "w") as f:
            json.dump(result, f, indent=2)
        console.print(f"\nSaved to [bold]{output}[/bold]")


@main.command()
@click.option("--port", type=int, default=8080)
@click.option("--host", type=str, default="0.0.0.0")
def serve(port, host):
    """Launch the HTML dashboard."""
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    from pathlib import Path
    import tempfile

    app = Flask(__name__, static_folder=str(Path(__file__).parent.parent / "web"))
    CORS(app)
    config = Config()
    engine = ReasoningEngine(config)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/api/modes")
    def modes():
        return jsonify({"modes": engine.available_modes()})

    @app.route("/api/analyze", methods=["POST"])
    def api_analyze():
        mode = request.form.get("mode", "social")
        file = request.files.get("image")
        if not file:
            return jsonify({"error": "No image provided"}), 400
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        file.save(tmp.name)
        tmp.close()
        try:
            result = engine.full_analysis(tmp.name) if mode == "full" else engine.analyze_image(tmp.name, mode=mode)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    console.print(f"Dashboard at [bold]http://{host}:{port}[/bold]")
    app.run(host=host, port=port, debug=False)


@main.command()
@click.option("--dataset", type=click.Path(exists=True), required=True)
@click.option("--output", "-o", type=str, default="results")
def benchmark(dataset, output):
    """Run the evaluation benchmark."""
    config = Config()
    runner = BenchmarkRunner(config)
    cases = runner.load_test_cases(dataset)
    summary = runner.run(cases, output_dir=output)
    console.print(Panel(
        f"Total: {summary['total']} | Passed: {summary['passed']} | "
        f"Failed: {summary['failed']} | Errors: {summary['errors']}\n"
        f"Accuracy: {summary['accuracy']:.1%} | Avg Latency: {summary['avg_latency_sec']}s",
        title="Benchmark Results",
    ))


if __name__ == "__main__":
    main()
