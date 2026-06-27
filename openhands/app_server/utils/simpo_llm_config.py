"""Environment-driven LLM defaults for Simpo internal deployments."""

from __future__ import annotations

import os

SIMPO_DEFAULT_LLM_MODEL = 'xai/grok-4.3'
SIMPO_DEFAULT_REASONING_EFFORT = 'low'
SIMPO_LLM_PROFILE_NAME = 'Simpo xAI'


def _env_truthy(name: str) -> bool:
    return os.getenv(name, 'false').lower() in ('true', '1')


def get_default_llm_model() -> str:
    """Return the default LLM model id for this deployment."""
    return os.getenv('OH_DEFAULT_LLM_MODEL', SIMPO_DEFAULT_LLM_MODEL).strip()


def get_default_reasoning_effort() -> str:
    """Return the default reasoning effort for new/migrated LLM settings."""
    return os.getenv('OH_DEFAULT_LLM_REASONING_EFFORT', SIMPO_DEFAULT_REASONING_EFFORT).strip()


def get_llm_provider_allowlist() -> list[str] | None:
    """Return an allowlisted provider list when configured, else ``None``.

    ``OH_LLM_PROVIDER_ALLOWLIST`` accepts a comma-separated list, e.g.
    ``xai`` or ``xai,openai``. When unset, upstream multi-provider discovery
    is preserved.
    """
    raw = os.getenv('OH_LLM_PROVIDER_ALLOWLIST', '').strip()
    if not raw:
        return None
    providers = [part.strip() for part in raw.split(',') if part.strip()]
    return providers or None


def is_simpo_xai_only_mode() -> bool:
    """True when the deployment is restricted to the xAI provider allowlist."""
    allowlist = get_llm_provider_allowlist()
    return allowlist is not None and allowlist == ['xai']
