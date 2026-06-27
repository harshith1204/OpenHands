"""Tests for deployment LLM environment configuration."""

from openhands.app_server.utils.deployment_llm_config import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROFILE_NAME,
    DEFAULT_REASONING_EFFORT,
    XAI_DEFAULT_BASE_URL,
    get_default_llm_api_key,
    get_default_llm_base_url,
    get_default_llm_model,
    get_default_reasoning_effort,
    is_xai_base_url,
)


def test_default_llm_model_fallback():
    assert get_default_llm_model() == DEFAULT_LLM_MODEL == 'xai/grok-4.3'


def test_default_reasoning_effort_fallback():
    assert get_default_reasoning_effort() == DEFAULT_REASONING_EFFORT == 'low'


def test_default_llm_api_key_fallback():
    assert get_default_llm_api_key() is None


def test_default_llm_base_url_fallback():
    assert get_default_llm_base_url() is None


def test_default_profile_name():
    assert DEFAULT_LLM_PROFILE_NAME == 'Default'


def test_env_overrides(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_MODEL', 'xai/grok-build-0.1')
    monkeypatch.setenv('OH_DEFAULT_LLM_REASONING_EFFORT', 'medium')
    monkeypatch.setenv('OH_DEFAULT_LLM_API_KEY', 'xai-test-key')
    monkeypatch.setenv('OH_DEFAULT_LLM_BASE_URL', XAI_DEFAULT_BASE_URL)
    assert get_default_llm_model() == 'xai/grok-build-0.1'
    assert get_default_reasoning_effort() == 'medium'
    assert get_default_llm_api_key() == 'xai-test-key'
    assert get_default_llm_base_url() == XAI_DEFAULT_BASE_URL


def test_default_llm_base_url_accepts_regional_xai_endpoint(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_BASE_URL', 'https://eu-west-1.api.x.ai/v1/')

    assert get_default_llm_base_url() == 'https://eu-west-1.api.x.ai/v1'


def test_default_llm_base_url_rejects_non_xai_endpoint(monkeypatch):
    monkeypatch.setenv('OH_DEFAULT_LLM_BASE_URL', 'https://llm-proxy.example.test/v1')

    try:
        get_default_llm_base_url()
    except ValueError as exc:
        assert 'OH_DEFAULT_LLM_BASE_URL must use xAI' in str(exc)
    else:
        raise AssertionError('Expected invalid xAI base URL to be rejected')


def test_is_xai_base_url():
    assert is_xai_base_url(XAI_DEFAULT_BASE_URL)
    assert is_xai_base_url('https://eu-west-1.api.x.ai/v1')
    assert not is_xai_base_url('http://api.x.ai/v1')
    assert not is_xai_base_url('https://llm-proxy.app.all-hands.dev/v1')
