"""Tests for Simpo LLM environment configuration."""

from openhands.app_server.utils.simpo_llm_config import (
    get_default_llm_model,
    get_default_reasoning_effort,
    get_llm_provider_allowlist,
    is_simpo_xai_only_mode,
)


def test_default_llm_model_fallback():
    assert get_default_llm_model() == 'xai/grok-4.3'


def test_default_reasoning_effort_fallback():
    assert get_default_reasoning_effort() == 'low'


def test_provider_allowlist_unset_returns_none(monkeypatch):
    monkeypatch.delenv('OH_LLM_PROVIDER_ALLOWLIST', raising=False)
    assert get_llm_provider_allowlist() is None


def test_provider_allowlist_parses_comma_separated(monkeypatch):
    monkeypatch.setenv('OH_LLM_PROVIDER_ALLOWLIST', 'xai,openai')
    assert get_llm_provider_allowlist() == ['xai', 'openai']


def test_is_simpo_xai_only_mode_true(monkeypatch):
    monkeypatch.setenv('OH_LLM_PROVIDER_ALLOWLIST', 'xai')
    assert is_simpo_xai_only_mode() is True


def test_is_simpo_xai_only_mode_false_when_unset(monkeypatch):
    monkeypatch.delenv('OH_LLM_PROVIDER_ALLOWLIST', raising=False)
    assert is_simpo_xai_only_mode() is False


def test_env_overrides(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_MODEL', 'xai/grok-build-0.1')
    monkeypatch.setenv('OH_DEFAULT_LLM_REASONING_EFFORT', 'medium')
    assert get_default_llm_model() == 'xai/grok-build-0.1'
    assert get_default_reasoning_effort() == 'medium'
