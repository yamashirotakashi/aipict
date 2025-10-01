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

## Phase 3 artifacts

- `presets/comfyui/lightnovel_workflow.json` / `turnaround_workflow.json` — ラノベ立ち絵・三面図プリセット定義。
- `config/phase3/preset_registry.json` / `character_tags.json` — プリセット参照とキャラクタータグ辞書。
- `scripts/phase3/check_character_prompt.py` — キャラ用プロンプトのタグ整合検証ツール。
- `scripts/phase3/sync_presets.sh` — プリセットレジストリに基づくComfyUIプリセット同期。
- `docs/xml/stage3-report.xml` — プリセットカタログ、キャラクター一貫性ルール、運用手順のレポート。
- `tests/phase3/test_stage3.py` — Phase3成果物の構造と整合性をTDDで担保するpytest。

## Phase 4 artifacts

- `config/phase4/dataset_ledger.csv` — 許諾・ライセンス・商用可否を管理する台帳テンプレート。
- `config/phase4/caption_config.json` / `dedup_config.json` — 自動キャプション・重複除去の設定。
- `datasets/lora_template/` — 画像/キャプション/分割/レポートの標準ディレクトリ構成と品質レポート雛形。
- `scripts/phase4/generate_captions.py` / `dedup_images.py` / `run_lora_training.sh` — キャプション生成、重複検出、LoRA学習実行テンプレート。
- `docs/xml/stage4-report.xml` — データ整備と学習フロー、MCP計画をまとめたレポート。
- `tests/phase4/test_stage4.py` — Phase4成果物の存在と必須設定をチェックするpytest。
