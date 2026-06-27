"""Migrate persisted settings from OpenHands managed LLM flow to xAI defaults."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openhands.app_server.utils.deployment_llm_config import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROFILE_NAME,
    get_default_llm_model,
    get_default_reasoning_effort,
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


def migrate_settings_kwargs_for_xai(
    kwargs: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """Migrate raw settings JSON toward xAI defaults.

    Returns the (possibly updated) kwargs dict and whether any migration ran.
    """
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
        profiles = {DEFAULT_LLM_PROFILE_NAME: deepcopy(migrated_llm)}
        active = DEFAULT_LLM_PROFILE_NAME
        changed = True
    elif active not in profiles:
        active = (
            DEFAULT_LLM_PROFILE_NAME
            if DEFAULT_LLM_PROFILE_NAME in profiles
            else next(iter(profiles), DEFAULT_LLM_PROFILE_NAME)
        )
        changed = True

    migrated['llm_profiles'] = {
        'profiles': profiles,
        'active': active,
    }

    if migrated.get('llm_model') != migrated_llm.get('model'):
        migrated['llm_model'] = migrated_llm.get('model', DEFAULT_LLM_MODEL)
        changed = True

    return migrated, changed
