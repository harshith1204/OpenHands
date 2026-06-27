"""Environment-driven LLM defaults for this deployment."""

from __future__ import annotations

import os

DEFAULT_LLM_MODEL = 'xai/grok-4.3'
DEFAULT_REASONING_EFFORT = 'low'
DEFAULT_LLM_PROFILE_NAME = 'Default'


def get_default_llm_model() -> str:
    """Return the default LLM model id for this deployment."""
    return os.getenv('OH_DEFAULT_LLM_MODEL', DEFAULT_LLM_MODEL).strip()


def get_default_reasoning_effort() -> str:
    """Return the default reasoning effort for new/migrated LLM settings."""
    return os.getenv('OH_DEFAULT_LLM_REASONING_EFFORT', DEFAULT_REASONING_EFFORT).strip()
