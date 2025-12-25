#!/usr/bin/env python3
# /// script
# dependencies = ["google-genai"]
# ///
"""
GenImg - AI Image Generation Tool
Uses Gemini for image generation
"""

import os
import sys
import json
import base64
import argparse
import subprocess
from pathlib import Path

# Skill root directory (relative to this script)
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"

# Available models
MODELS = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"]

def verify_image(path: str) -> dict:
    """Verify that a file is a valid image using the `file` command."""
    try:
        result = subprocess.run(
            ["file", "--mime-type", "-b", path],
            capture_output=True,
            text=True,
            timeout=5
        )
        mime_type = result.stdout.strip()
        is_image = mime_type.startswith("image/")
        return {
            "valid": is_image,
            "mime_type": mime_type,
            "message": f"Valid {mime_type}" if is_image else f"Not an image: {mime_type}"
        }
    except Exception as e:
        return {"valid": False, "mime_type": "unknown", "message": f"Verification failed: {e}"}


STYLES = {
    "photo": "Photorealistic, high quality photograph, natural lighting",
    "illustration": "Digital illustration, clean lines, vibrant colors",
    "flat": "Flat design, vector style, minimal shadows, clean",
    "3d": "3D rendered, subtle shadows, depth, realistic materials",
    "minimalist": "Minimalist design, lots of whitespace, simple composition",
    "corporate": "Professional corporate style, clean, modern, business",
    "tech": "Modern tech aesthetic, gradients, geometric shapes, futuristic",
    "sketch": "Hand-drawn sketch style, pencil strokes, artistic",
    "isometric": "Isometric perspective, 3D blocks, clean geometric",
    "watercolor": "Watercolor painting style, soft edges, artistic",
    "anime": "Anime/manga style illustration, vibrant, expressive",
    "icon": "Simple icon, flat design, single subject, transparent friendly",
}


def load_env():
    """Load .env from skill directory."""
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    value = value.strip().strip('"').strip("'")
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value


def get_api_key() -> str:
    """Get API key from env."""
    load_env()
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(f"GEMINI_API_KEY not set. Add to {ENV_FILE} or environment.")
    return key


def get_base_url() -> str:
    """Get base URL from env (optional)."""
    load_env()
    return os.getenv("GOOGLE_GEMINI_BASE_URL")


class ImageGenerator:
    """Gemini image generator."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_api_key()
        self.base_url = get_base_url()

        from google import genai
        from google.genai import types
        self.genai = genai
        self.types = types

        # Support custom base URL
        if self.base_url:
            self.client = genai.Client(
                api_key=self.api_key,
                http_options={"base_url": self.base_url}
            )
        else:
            self.client = genai.Client(api_key=self.api_key)

        self.model = MODELS[0]

    def set_model(self, model: str):
        """Set model name."""
        self.model = model

    def generate(
        self,
        prompt: str,
        output_path: str = "generated.png",
        style: str = None,
        negative_prompt: str = None,
        aspect_ratio: str = "16:9",
    ) -> dict:
        """Generate an image."""
        full_prompt = self._build_prompt(prompt, style, negative_prompt, aspect_ratio)

        config = self.types.GenerateContentConfig(
            temperature=0.7,
            response_modalities=["image", "text"],
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[full_prompt],
            config=config,
        )

        return self._save_image(response, output_path)

    def _build_prompt(self, prompt: str, style: str, negative: str, ratio: str) -> str:
        """Build optimized prompt."""
        parts = [prompt]

        if style:
            parts.append(STYLES.get(style, style))

        ratio_hints = {
            "16:9": "widescreen composition",
            "9:16": "vertical/portrait composition",
            "1:1": "square composition",
            "4:3": "traditional aspect ratio",
        }
        if ratio in ratio_hints:
            parts.append(ratio_hints[ratio])

        parts.append("high quality, detailed")

        if negative:
            parts.append(f"Avoid: {negative}")

        return ". ".join(parts)

    def _save_image(self, response, output_path: str) -> dict:
        """Save image from response and verify it."""
        if hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Get API-reported mime type
                    api_mime = getattr(part.inline_data, 'mime_type', 'unknown')

                    raw_data = part.inline_data.data
                    data_type = type(raw_data).__name__

                    # Handle different data types
                    if isinstance(raw_data, bytes):
                        image_data = raw_data
                    elif isinstance(raw_data, str):
                        image_data = base64.b64decode(raw_data)
                    else:
                        return {"success": False, "error": f"Unknown data type: {data_type}"}

                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    # Verify the saved file is actually an image
                    verification = verify_image(output_path)
                    if not verification["valid"]:
                        # Remove invalid file
                        Path(output_path).unlink(missing_ok=True)
                        return {
                            "success": False,
                            "error": f"Generated file is not a valid image: {verification['message']}",
                            "verification": verification
                        }

                    return {
                        "success": True,
                        "path": output_path,
                        "verified": True,
                        "mime_type": verification["mime_type"]
                    }

        return {"success": False, "error": "No image in response"}

    def edit(self, prompt: str, image_path: str, output_path: str = "edited.png") -> dict:
        """Edit an existing image."""
        if not Path(image_path).exists():
            return {"success": False, "error": f"Image not found: {image_path}"}

        with open(image_path, 'rb') as f:
            image_data = f.read()

        suffix = Path(image_path).suffix.lower()
        mime_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
        mime_type = mime_types.get(suffix, "image/png")

        contents = [
            prompt,
            self.types.Part.from_bytes(data=image_data, mime_type=mime_type),
        ]

        config = self.types.GenerateContentConfig(
            temperature=0.7,
            response_modalities=["image", "text"],
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        return self._save_image(response, output_path)


def list_styles():
    """List available styles."""
    print("Available styles:\n")
    for key, desc in STYLES.items():
        print(f"  {key:12} - {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s "a futuristic city at sunset"
  %(prog)s "mountain landscape" -s photo -o landscape.png
  %(prog)s "cloud icon" -s icon -r 1:1 -o cloud.png
  %(prog)s "add rainbow" -e source.png -o edited.png

Config: {ENV_FILE}
        """
    )

    parser.add_argument("prompt", nargs="?", help="Image description")
    parser.add_argument("-o", "--output", default="generated.png", help="Output path")
    parser.add_argument("-s", "--style", help="Style preset or custom description")
    parser.add_argument("-r", "--ratio", default="16:9",
                       choices=["16:9", "9:16", "4:3", "3:2", "1:1"],
                       help="Aspect ratio")
    parser.add_argument("-n", "--negative", help="What to avoid")
    parser.add_argument("-m", "--model", default=MODELS[0], choices=MODELS,
                       help=f"Model name (default: {MODELS[0]})")
    parser.add_argument("-e", "--edit", metavar="IMAGE", help="Edit existing image")
    parser.add_argument("--api-key", help="Override API key")
    parser.add_argument("--list-styles", action="store_true", help="List styles")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.list_styles:
        list_styles()
        return 0

    if not args.prompt:
        parser.error("prompt required (or use --list-styles)")

    try:
        gen = ImageGenerator(api_key=args.api_key)
        if args.model:
            gen.set_model(args.model)

        if args.edit:
            result = gen.edit(args.prompt, args.edit, args.output)
        else:
            result = gen.generate(args.prompt, args.output, args.style, args.negative, args.ratio)

        if args.json:
            print(json.dumps(result))
        elif result["success"]:
            mime_info = f" ({result.get('mime_type', 'unknown')})" if result.get("verified") else ""
            print(f"Generated: {result['path']}{mime_info} [verified]")
        else:
            print(f"Error: {result.get('error')}", file=sys.stderr)
            return 1

        return 0 if result["success"] else 1

    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
