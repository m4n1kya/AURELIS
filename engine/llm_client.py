"""
Multimodal LLM Client with Content-Addressable Caching
======================================================

Provides a fault-tolerant wrapper around Google Gemini for extracting structured
financial evidence from receipts and natural-language messages, backed by a
local SHA-256 disk cache and token telemetry.
"""

import hashlib
import json
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for multimodal financial evidence extraction using Google Gemini."""

    def __init__(self, cache_file: str = "llm_cache.json", model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.cache_file = cache_file
        self.cache: Dict[str, Any] = self._load_cache()

        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_calls: int = 0

    def _load_cache(self) -> Dict[str, Any]:
        """Load cached LLM responses from disk if available."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as exc:
                logger.warning("Failed to read LLM cache file %s: %s", self.cache_file, exc)
        return {}

    def _save_cache(self) -> None:
        """Persist cached LLM responses to disk."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2)
        except Exception as exc:
            logger.warning("Failed to write LLM cache file %s: %s", self.cache_file, exc)

    def _get_cache_key(self, prompt: str, image_path: Optional[str] = None) -> str:
        """Compute a deterministic SHA-256 cache key for a prompt and optional image payload."""
        digest = hashlib.sha256()
        digest.update(prompt.encode("utf-8"))
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                digest.update(img_file.read())
        return digest.hexdigest()

    def call_gemini(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        json_schema: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Execute a structured prompt against Google Gemini, returning a JSON string.
        Falls back to cached responses or an empty JSON object if offline.
        """
        cache_key = self._get_cache_key(prompt, image_path)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if not self.api_key:
            return "{}"

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            contents: list[Any] = [prompt]

            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    contents.append({"mime_type": "image/png", "data": img_file.read()})

            generation_config: Dict[str, Any] = {"response_mime_type": "application/json"}
            if json_schema:
                generation_config["response_schema"] = json_schema

            response = model.generate_content(contents, generation_config=generation_config)
            self.total_calls += 1

            usage = getattr(response, "usage_metadata", None)
            if usage:
                self.total_input_tokens += getattr(usage, "prompt_token_count", 0)
                self.total_output_tokens += getattr(usage, "candidates_token_count", 0)

            result_text = response.text or "{}"
            self.cache[cache_key] = result_text
            self._save_cache()
            return result_text
        except Exception as exc:
            logger.debug("Gemini invocation skipped or failed: %s", exc)
            return "{}"