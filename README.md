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

## Phase 1 artifacts

- `scripts/phase1/setup_wsl_rocm.sh` — WSL/ROCm構築チェックリストを出力する手順スクリプト。
- `docs/xml/stage1-report.xml` — Phase1実施記録（チェックリスト・落とし穴・MCP連携案）。
- `logs/phase1/torch_device_check_example.log` — `torch`デバイス検証ログの雛形。
- `tests/phase1/test_stage1.py` — 上記成果物の存在と内容をTDDで担保するpytest。

## Phase 2 artifacts

- `scripts/phase2/setup_shared_venv.sh` — UI群の共通venv構築スクリプト。
- `scripts/phase2/install_comfyui.sh` / `install_sdnext.sh` / `install_invokeai.sh` — 各UI導入と起動ラッパー生成スクリプト。
- `config/phase2/service_ports.json` — 標準ポート定義（ComfyUI:8188 / SD.Next:7860 / InvokeAI:9090）。
- `docs/xml/stage2-report.xml` — venv戦略、ポート標準化、モデル配置規約をまとめたレポート。
- `tests/phase2/test_stage2.py` — Phase2成果物の存在と主要要件を検証するpytest。
