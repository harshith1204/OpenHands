"""Environment-driven LLM defaults for this deployment."""

from __future__ import annotations

import os
from urllib.parse import urlparse

DEFAULT_LLM_MODEL = 'xai/grok-4.3'
DEFAULT_REASONING_EFFORT = 'low'
DEFAULT_LLM_PROFILE_NAME = 'Default'
XAI_DEFAULT_BASE_URL = 'https://api.x.ai/v1'


def get_default_llm_model() -> str:
    """Return the default LLM model id for this deployment."""
    return os.getenv('OH_DEFAULT_LLM_MODEL', DEFAULT_LLM_MODEL).strip()


def get_default_reasoning_effort() -> str:
    """Return the default reasoning effort for new/migrated LLM settings."""
    return os.getenv('OH_DEFAULT_LLM_REASONING_EFFORT', DEFAULT_REASONING_EFFORT).strip()


def get_default_llm_api_key() -> str | None:
    """Return the deployment-provided LLM API key, if configured."""
    api_key = os.getenv('OH_DEFAULT_LLM_API_KEY')
    if api_key is None:
        return None
    return api_key.strip() or None


def get_default_llm_base_url() -> str | None:
    """Return the deployment-provided LLM base URL, if configured."""
    base_url = os.getenv('OH_DEFAULT_LLM_BASE_URL')
    if base_url is None:
        return None
    normalized = base_url.strip().rstrip('/')
    if not normalized:
        return None
    if not is_xai_base_url(normalized):
        raise ValueError(
            'OH_DEFAULT_LLM_BASE_URL must use xAI OpenAI-compatible endpoint '
            f'{XAI_DEFAULT_BASE_URL} or a documented regional xAI /v1 endpoint.'
        )
    return normalized


def is_xai_base_url(base_url: str) -> bool:
    """Return whether a base URL matches xAI's documented /v1 API endpoint."""
    parsed = urlparse(base_url)
    host = parsed.hostname or ''
    return (
        parsed.scheme == 'https'
        and parsed.path.rstrip('/') == '/v1'
        and (host == 'api.x.ai' or host.endswith('.api.x.ai'))
    )
