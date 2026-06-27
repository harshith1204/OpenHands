"""Migrate persisted settings from OpenHands managed LLM flow to Simpo xAI."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openhands.app_server.utils.simpo_llm_config import (
    SIMPO_DEFAULT_LLM_MODEL,
    SIMPO_DEFAULT_REASONING_EFFORT,
    SIMPO_LLM_PROFILE_NAME,
    get_default_llm_model,
    get_default_reasoning_effort,
    is_simpo_xai_only_mode,
)


def _is_legacy_managed_model(model: str | None) -> bool:
    if not model:
        return True
    return model.startswith('openhands/')


def _normalize_llm_dict(llm: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Return migrated LLM dict and whether it changed."""
    migrated = deepcopy(llm)
    changed = False

    model = migrated.get('model')
    if _is_legacy_managed_model(str(model) if model is not None else None):
        migrated['model'] = get_default_llm_model()
        changed = True

    if not migrated.get('reasoning_effort'):
        migrated['reasoning_effort'] = get_default_reasoning_effort()
        changed = True

    return migrated, changed


def migrate_settings_kwargs_for_simpo_xai(
    kwargs: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """Migrate raw settings JSON toward Simpo xAI defaults when enabled.

    Returns the (possibly updated) kwargs dict and whether any migration ran.
    """
    if not is_simpo_xai_only_mode():
        return kwargs, False

    migrated = deepcopy(kwargs)
    changed = False

    agent_settings = migrated.setdefault('agent_settings', {})
    if not isinstance(agent_settings, dict):
        return kwargs, False

    llm = agent_settings.get('llm')
    if not isinstance(llm, dict):
        llm = {}
        agent_settings['llm'] = llm
        changed = True

    migrated_llm, llm_changed = _normalize_llm_dict(llm)
    if llm_changed:
        agent_settings['llm'] = migrated_llm
        changed = True

    profiles_block = migrated.get('llm_profiles')
    profiles: dict[str, Any]
    active: str | None
    if isinstance(profiles_block, dict):
        raw_profiles = profiles_block.get('profiles')
        profiles = raw_profiles if isinstance(raw_profiles, dict) else {}
        active = profiles_block.get('active')
    else:
        profiles = {}
        active = None

    needs_profile_rewrite = (
        not profiles
        or any(
            _is_legacy_managed_model(
                str((profile or {}).get('model'))
                if isinstance(profile, dict)
                else None
            )
            for profile in profiles.values()
        )
    )

    if needs_profile_rewrite:
        profiles = {SIMPO_LLM_PROFILE_NAME: deepcopy(migrated_llm)}
        active = SIMPO_LLM_PROFILE_NAME
        changed = True
    elif active not in profiles:
        active = SIMPO_LLM_PROFILE_NAME if SIMPO_LLM_PROFILE_NAME in profiles else next(
            iter(profiles), SIMPO_LLM_PROFILE_NAME
        )
        changed = True

    migrated['llm_profiles'] = {
        'profiles': profiles,
        'active': active,
    }

    # Keep top-level llm_model in sync for any legacy readers.
    if migrated.get('llm_model') != migrated_llm.get('model'):
        migrated['llm_model'] = migrated_llm.get('model', SIMPO_DEFAULT_LLM_MODEL)
        changed = True

    return migrated, changed
