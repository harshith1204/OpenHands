"""Tests for xAI settings migration."""

from openhands.app_server.settings.xai_settings_migration import (
    migrate_settings_kwargs_for_xai,
)
from openhands.app_server.utils.deployment_llm_config import (
    DEFAULT_LLM_PROFILE_NAME,
    XAI_DEFAULT_BASE_URL,
)


def test_migration_rewrites_openhands_model():
    kwargs = {
        'llm_model': 'openhands/claude-opus-4-5-20251101',
        'agent_settings': {'llm': {'model': 'openhands/claude-opus-4-5-20251101'}},
        'llm_profiles': {
            'profiles': {
                'Default': {'model': 'openhands/claude-opus-4-5-20251101'},
            },
            'active': 'Default',
        },
    }
    migrated, changed = migrate_settings_kwargs_for_xai(kwargs)
    assert changed is True
    assert migrated['agent_settings']['llm']['model'] == 'xai/grok-4.3'
    assert migrated['agent_settings']['llm']['reasoning_effort'] == 'low'
    assert migrated['llm_model'] == 'xai/grok-4.3'
    assert set(migrated['llm_profiles']['profiles']) == {DEFAULT_LLM_PROFILE_NAME}
    assert migrated['llm_profiles']['active'] == DEFAULT_LLM_PROFILE_NAME


def test_migration_preserves_non_legacy_profiles():
    kwargs = {
        'llm_model': 'xai/grok-4.3',
        'agent_settings': {
            'llm': {'model': 'xai/grok-4.3', 'reasoning_effort': 'low'},
        },
        'llm_profiles': {
            'profiles': {
                'My xAI': {'model': 'xai/grok-4.3', 'reasoning_effort': 'high'},
            },
            'active': 'My xAI',
        },
    }
    migrated, changed = migrate_settings_kwargs_for_xai(kwargs)
    assert changed is False
    assert migrated['llm_profiles']['active'] == 'My xAI'


def test_migration_applies_env_credentials_and_clears_proxy(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_API_KEY', 'xai-test-key')
    monkeypatch.setenv('OH_DEFAULT_LLM_BASE_URL', XAI_DEFAULT_BASE_URL)
    kwargs = {
        'llm_model': 'xai/grok-4.3',
        'agent_settings': {
            'llm': {
                'model': 'xai/grok-4.3',
                'reasoning_effort': 'low',
                'api_key': 'sk-proxy-key',
                'base_url': 'https://llm-proxy.app.all-hands.dev',
            },
        },
        'llm_profiles': {
            'profiles': {
                'Default': {
                    'model': 'xai/grok-4.3',
                    'reasoning_effort': 'low',
                    'api_key': 'sk-proxy-key',
                    'base_url': 'https://llm-proxy.app.all-hands.dev',
                },
            },
            'active': 'Default',
        },
    }

    migrated, changed = migrate_settings_kwargs_for_xai(kwargs)

    assert changed is True
    assert migrated['agent_settings']['llm']['api_key'] == 'xai-test-key'
    assert migrated['agent_settings']['llm']['base_url'] == XAI_DEFAULT_BASE_URL
    assert migrated['llm_profiles']['profiles']['Default']['api_key'] == 'xai-test-key'
    assert (
        migrated['llm_profiles']['profiles']['Default']['base_url']
        == XAI_DEFAULT_BASE_URL
    )
