"""Unit tests for the config_models and config_router.

This module tests the config router endpoints,
focusing on the search_models and search_providers endpoints.
"""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from openhands.app_server.config_api.config_models import LLMModel, Provider
from openhands.app_server.config_api.config_router import router
from openhands.app_server.config_api.default_llm_model_service import (
    _to_llm_models,
    _to_providers,
)
from openhands.app_server.utils.dependencies import check_session_api_key
from openhands.app_server.utils.llm import get_supported_llm_models
from openhands.app_server.utils.paging_utils import encode_page_id, paginate_results


class TestLLMModel:
    """Test suite for LLMModel."""

    def test_create_model_with_name_and_verified(self):
        model = LLMModel(provider='openai', name='gpt-4', verified=True)

        assert model.provider == 'openai'
        assert model.name == 'gpt-4'
        assert model.verified is True

    def test_create_model_with_default_verified_false(self):
        model = LLMModel(provider='openai', name='gpt-4')

        assert model.provider == 'openai'
        assert model.name == 'gpt-4'
        assert model.verified is False


class TestProvider:
    """Test suite for Provider."""

    def test_create_provider(self):
        provider = Provider(name='openai', verified=True)

        assert provider.name == 'openai'
        assert provider.verified is True

    def test_create_provider_default_unverified(self):
        provider = Provider(name='some-provider')

        assert provider.name == 'some-provider'
        assert provider.verified is False


class TestPagination:
    """Test suite for pagination helper function."""

    def test_returns_first_page_when_no_page_id(self):
        models = [
            LLMModel(provider='openai', name='gpt-4', verified=True),
            LLMModel(provider='anthropic', name='claude-3', verified=True),
            LLMModel(provider='openai', name='gpt-3.5', verified=False),
        ]

        result, next_page_id = paginate_results(models, None, 2)

        assert len(result) == 2
        assert next_page_id == encode_page_id(2)

    def test_returns_second_page_when_page_id_provided(self):
        models = [
            LLMModel(provider='openai', name='gpt-4', verified=True),
            LLMModel(provider='anthropic', name='claude-3', verified=True),
            LLMModel(provider='openai', name='gpt-3.5', verified=False),
        ]
        encoded_page_id = encode_page_id(2)

        result, next_page_id = paginate_results(models, encoded_page_id, 2)

        assert len(result) == 1
        assert result[0].provider == 'openai'
        assert result[0].name == 'gpt-3.5'
        assert next_page_id is None


class TestToLLMModels:
    """Test suite for _to_llm_models conversion function."""

    def test_returns_list_of_llm_models(self):
        models = _to_llm_models(get_supported_llm_models())

        assert isinstance(models, list)
        assert all(isinstance(m, LLMModel) for m in models)

    def test_all_models_are_verified(self):
        models = _to_llm_models(get_supported_llm_models())

        assert models
        assert all(m.verified for m in models)
        xai_models = [m for m in models if m.provider == 'xai']
        assert any(m.name == 'grok-4.3' for m in xai_models)
        assert all(
            m.verified for m in xai_models if m.name in {'grok-4.3', 'grok-build-0.1'}
        )

    def test_xai_provider_is_verified(self):
        providers = _to_providers(get_supported_llm_models())
        xai = next((p for p in providers if p.name == 'xai'), None)

        assert xai is not None
        assert xai.verified is True


class TestToProviders:
    """Test suite for _to_providers conversion function."""

    def test_returns_list_of_providers(self):
        providers = _to_providers(get_supported_llm_models())

        assert isinstance(providers, list)
        assert all(isinstance(p, Provider) for p in providers)

    def test_providers_are_unique(self):
        providers = _to_providers(get_supported_llm_models())
        names = [p.name for p in providers]

        assert len(names) == len(set(names))

    def test_only_xai_provider(self):
        providers = _to_providers(get_supported_llm_models())

        assert len(providers) == 1
        assert providers[0].name == 'xai'
        assert providers[0].verified is True


@pytest.fixture
def test_client():
    """Create a test client with the actual config router and mocked dependencies.

    We override check_session_api_key to bypass auth checks.
    This allows us to test the actual Query parameter validation in the router.
    """
    app = FastAPI()
    app.include_router(router)

    # Override the auth dependency to always pass
    app.dependency_overrides[check_session_api_key] = lambda: None

    client = TestClient(app, raise_server_exceptions=False)
    yield client

    # Clean up
    app.dependency_overrides.clear()


class TestSearchModelsEndpoint:
    """Test suite for /models/search endpoint."""

    def test_returns_200_with_paginated_results(self, test_client):
        response = test_client.get('/config/models/search')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'items' in data
        assert 'next_page_id' in data

    def test_respects_limit_parameter(self, test_client):
        response = test_client.get('/config/models/search', params={'limit': 2})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['items']) <= 2

    def test_filters_by_query_name_contains(self, test_client):
        response = test_client.get('/config/models/search', params={'query': 'gpt'})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert 'gpt' in item['name'].lower()

    def test_filters_by_verified_eq_true(self, test_client):
        response = test_client.get(
            '/config/models/search', params={'verified__eq': True}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert item['verified'] is True

    def test_filters_by_verified_eq_false(self, test_client):
        response = test_client.get(
            '/config/models/search', params={'verified__eq': False}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert item['verified'] is False

    def test_combines_query_and_verified_filters(self, test_client):
        response = test_client.get(
            '/config/models/search', params={'query': 'gpt', 'verified__eq': True}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert 'gpt' in item['name'].lower()
            assert item['verified'] is True

    def test_pagination_with_page_id(self, test_client):
        response1 = test_client.get('/config/models/search', params={'limit': 1})
        data1 = response1.json()

        if data1.get('next_page_id'):
            response2 = test_client.get(
                '/config/models/search',
                params={'limit': 1, 'page_id': data1['next_page_id']},
            )
            data2 = response2.json()

            assert response2.status_code == status.HTTP_200_OK
            assert data1['items'][0]['name'] != data2['items'][0]['name']

    def test_invalid_limit_parameter_returns_422(self, test_client):
        response = test_client.get('/config/models/search', params={'limit': 0})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_limit_exceeds_max_returns_422(self, test_client):
        response = test_client.get('/config/models/search', params={'limit': 101})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSearchProvidersEndpoint:
    """Test suite for /providers/search endpoint."""

    def test_returns_200_with_paginated_results(self, test_client):
        response = test_client.get('/config/providers/search')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'items' in data
        assert 'next_page_id' in data
        assert len(data['items']) > 0

    def test_respects_limit_parameter(self, test_client):
        response = test_client.get('/config/providers/search', params={'limit': 2})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['items']) <= 2

    def test_filters_by_query(self, test_client):
        response = test_client.get(
            '/config/providers/search', params={'query': 'openai'}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert 'openai' in item['name'].lower()

    def test_filters_by_verified_eq_true(self, test_client):
        response = test_client.get(
            '/config/providers/search', params={'verified__eq': True}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert item['verified'] is True

    def test_filters_by_verified_eq_false(self, test_client):
        response = test_client.get(
            '/config/providers/search', params={'verified__eq': False}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert item['verified'] is False

    def test_pagination_with_page_id(self, test_client):
        response1 = test_client.get('/config/providers/search', params={'limit': 1})
        data1 = response1.json()

        if data1.get('next_page_id'):
            response2 = test_client.get(
                '/config/providers/search',
                params={'limit': 1, 'page_id': data1['next_page_id']},
            )
            data2 = response2.json()

            assert response2.status_code == status.HTTP_200_OK
            assert data1['items'][0]['name'] != data2['items'][0]['name']

    def test_providers_include_verified_flag(self, test_client):
        response = test_client.get('/config/providers/search')

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for item in data['items']:
            assert 'name' in item
            assert 'verified' in item

    def test_invalid_limit_parameter_returns_422(self, test_client):
        response = test_client.get('/config/providers/search', params={'limit': 0})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_limit_exceeds_max_returns_422(self, test_client):
        response = test_client.get('/config/providers/search', params={'limit': 101})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestXaiOnlyDiscovery:
    """Model discovery is xAI-only in this deployment."""

    def test_get_supported_llm_models_returns_xai_only(self):
        response = get_supported_llm_models()

        assert response.models == ['xai/grok-4.3', 'xai/grok-build-0.1']
        assert response.verified_providers == ['xai']
        assert response.default_model == 'xai/grok-4.3'
        assert 'openhands/' not in ' '.join(response.models)
