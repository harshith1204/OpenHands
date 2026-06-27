"""Tests for deployment LLM environment configuration."""

from openhands.app_server.utils.deployment_llm_config import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROFILE_NAME,
    DEFAULT_REASONING_EFFORT,
    get_default_llm_model,
    get_default_reasoning_effort,
)


def test_default_llm_model_fallback():
    assert get_default_llm_model() == DEFAULT_LLM_MODEL == 'xai/grok-4.3'


def test_default_reasoning_effort_fallback():
    assert get_default_reasoning_effort() == DEFAULT_REASONING_EFFORT == 'low'


def test_default_profile_name():
    assert DEFAULT_LLM_PROFILE_NAME == 'Default'


def test_env_overrides(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_MODEL', 'xai/grok-build-0.1')
    monkeypatch.setenv('OH_DEFAULT_LLM_REASONING_EFFORT', 'medium')
    assert get_default_llm_model() == 'xai/grok-build-0.1'
    assert get_default_reasoning_effort() == 'medium'
