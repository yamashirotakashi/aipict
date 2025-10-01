# aipict

AI image generation workspace scaffold. This project uses Hugging Face Diffusers to create images from text prompts.

## Project layout

- `src/aipict/` – reusable helpers for loading diffusion pipelines and generating images
- `prompts/` – store curated prompt files for later reuse
- `assets/` – keep reference renders, mood boards, or training imagery
- `notebooks/` – exploratory experiments, prototyping, and prompt engineering notebooks
- `outputs/` – generated images (ignored in git by default)

## Quick start

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Authenticate with Hugging Face (optional but recommended)**
   - Create a token at <https://huggingface.co/settings/tokens>
   - Copy `.env.example` to `.env` and set `HUGGINGFACE_TOKEN=your_token`
   - Alternatively export `HUGGINGFACE_TOKEN` in your shell
4. **Generate an image**
   ```bash
   python -m aipict.generate "a cozy cyberpunk café, volumetric lighting, ultra detailed"
   ```
   Use `--negative "blurry, low quality"` or `--model stabilityai/stable-diffusion-xl-base-1.0` for different styles.

## Next steps

- Add notebooks under `notebooks/` for prompt exploration and model comparisons.
- Integrate custom pipelines (e.g., ControlNet, LoRA) by extending `src/aipict/generate.py`.
- Automate batch rendering scripts and dataset preparation workflows.
