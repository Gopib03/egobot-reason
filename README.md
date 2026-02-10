cat > README.md << 'EOF'
# 🤖 EgoBot Reason — Egocentric Robot Reasoning with Cosmos Reason 2

> NVIDIA Cosmos Cookoff Submission

Gives robots the ability to see, understand, and safely interact with humans from a first-person perspective using NVIDIA Cosmos Reason 2.

## Features
- 🧑‍🤝‍🧑 Social Intent Recognition
- 📐 Spatial Awareness
- ⚠️ Safety Assessment
- 🎯 Action Planning

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your NVIDIA_API_KEY to .env
```

## Usage
```bash
# Analyze an image
python -m src.cli analyze --image photo.jpg --mode social

# Analyze a video
python -m src.cli analyze --video clip.mp4 --mode safety

# Run all modes
python -m src.cli analyze --image photo.jpg --mode full

# Web dashboard
python -m src.cli serve --port 8080

# Benchmark
python -m src.cli benchmark --dataset tests/sample_cases.json
```

## Configuration (.env)

| Variable | Default |
|----------|---------|
| NVIDIA_API_KEY | (required) |
| COSMOS_MODEL | nvidia/cosmos-reason2-8b |
| COSMOS_BASE_URL | https://integrate.api.nvidia.com/v1 |
| MAX_TOKENS | 4096 |
| TEMPERATURE | 0.3 |
| VIDEO_FPS | 2 |

## Self-Hosted NIM
```bash
docker run -it --rm --gpus all --shm-size=16GB \
  -e NGC_API_KEY=$NGC_API_KEY -p 8000:8000 \
  nvcr.io/nim/nvidia/cosmos-reason2-8b:latest

export COSMOS_BASE_URL="http://localhost:8000/v1"
```

## Project Structure
```
src/
  cli.py                    # CLI entry point
  core/
    cosmos_client.py        # Cosmos Reason 2 API
    video_processor.py      # Frame extraction
    reasoning_engine.py     # Reasoning pipeline
    action_planner.py       # Action planning
  prompts/
    social_reasoning.py     # Social intent
    spatial_reasoning.py    # Spatial layout
    safety_assessment.py    # Safety checks
    action_planning.py      # Next actions
  evaluation/
    benchmark.py            # Eval harness
web/
  index.html                # Dashboard
tests/
  test_reasoning.py         # Unit tests
```

## Tests
```bash
pytest tests/
```

## License

Apache 2.0

Built with [NVIDIA Cosmos Reason 2](https://build.nvidia.com/nvidia/cosmos-reason2-8b)
EOF