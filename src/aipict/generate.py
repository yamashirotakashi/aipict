"""Simple Stable Diffusion image generation helper."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional

import torch
from diffusers import DPMSolverMultistepScheduler, StableDiffusionPipeline
from dotenv import load_dotenv


def load_pipeline(
    model_id: str,
    device: Optional[str] = None,
    use_half_precision: bool = True,
    auth_token: Optional[str] = None,
) -> StableDiffusionPipeline:
    """Instantiate a Stable Diffusion pipeline with sensible defaults."""

    load_dotenv()
    token = auth_token or os.getenv("HUGGINGFACE_TOKEN")

    dtype = torch.float16 if use_half_precision and torch.cuda.is_available() else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        use_auth_token=token,
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)

    return pipe


def generate_image(
    pipeline: StableDiffusionPipeline,
    prompt: str,
    negative_prompt: Optional[str] = None,
    num_inference_steps: int = 30,
    guidance_scale: float = 7.5,
    seed: Optional[int] = None,
    output_path: Path | str = "outputs/generated.png",
) -> Path:
    """Run the diffusion pipeline and persist the resulting image."""

    generator = None
    if seed is not None:
        generator = torch.Generator(device=pipeline.device).manual_seed(seed)

    output = pipeline(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )

    image = output.images[0]
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an image with Stable Diffusion")
    parser.add_argument("prompt", help="Positive text prompt")
    parser.add_argument("--negative", dest="negative", help="Negative prompt", default=None)
    parser.add_argument("--model", default="runwayml/stable-diffusion-v1-5", help="Model repo id")
    parser.add_argument("--steps", type=int, default=30, help="Number of inference steps")
    parser.add_argument("--guidance", type=float, default=7.5, help="Classifier-free guidance scale")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument(
        "--output",
        default="outputs/generated.png",
        help="Where to save the generated image",
    )
    parser.add_argument("--device", default=None, help="Force a device (cpu/cuda)")
    parser.add_argument(
        "--no-fp16",
        dest="use_half_precision",
        action="store_false",
        help="Disable half precision weights",
    )
    parser.set_defaults(use_half_precision=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipe = load_pipeline(
        model_id=args.model,
        device=args.device,
        use_half_precision=args.use_half_precision,
    )
    output_path = generate_image(
        pipeline=pipe,
        prompt=args.prompt,
        negative_prompt=args.negative,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        seed=args.seed,
        output_path=args.output,
    )
    print(f"Saved image to {output_path}")


if __name__ == "__main__":
    main()
