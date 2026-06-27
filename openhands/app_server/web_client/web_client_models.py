from datetime import datetime

from pydantic import BaseModel, Field

from openhands.agent_server.env_parser import DiscriminatedUnionMixin
from openhands.app_server.config_api.config_models import AppMode
from openhands.app_server.integrations.service_types import ProviderType


class WebClientFeatureFlags(BaseModel):
    enable_billing: bool = False
    hide_llm_settings: bool = False
    enable_linear: bool = False
    hide_users_page: bool = False
    hide_billing_page: bool = False
    hide_integrations_page: bool = False
    # When true, the web client hides personal workspaces from the org list
    # and selector for users who belong to at least one team org. Used by
    # OHE installs that bootstrap a default org and want it to be the only
    # workspace users see. UI-level only — the orgs API still returns
    # personal orgs, and disabling the flag restores them.
    hide_personal_workspaces: bool = False
    # When false, the web client hides the BYOK editing UI (custom model
    # string, base URL, and API key inputs) in LLM settings, leaving only the
    # managed model dropdown. Used by OHE installs where admins curate the
    # model list on the bundled LiteLLM proxy. Defaults to True so SaaS and
    # existing installs are unaffected. UI-level only — previously saved BYOK
    # settings keep working at runtime.
    allow_user_llm_configuration: bool = True
    enable_acp: bool = False
    enable_onboarding: bool = False
    enable_automations: bool = True


class ACPModelOption(BaseModel):
    id: str
    label: str


class ACPProviderConfig(BaseModel):
    key: str
    display_name: str
    default_command: list[str]
    default_model: str | None = None
    available_models: list[ACPModelOption] = Field(default_factory=list)
    api_key_env_var: str | None = None
    base_url_env_var: str | None = None


class WebClientConfig(DiscriminatedUnionMixin):
    app_mode: AppMode
    posthog_client_key: str | None
    feature_flags: WebClientFeatureFlags
    providers_configured: list[ProviderType]
    maintenance_start_time: datetime | None
    auth_url: str | None
    recaptcha_site_key: str | None
    faulty_models: list[str]
    error_message: str | None
    updated_at: datetime
    github_app_slug: str | None
    gitlab_enabled: bool = False
    provider_default_hosts: dict[str, str] = Field(default_factory=dict)
    slack_enabled: bool = False
    acp_providers: list[ACPProviderConfig] = Field(default_factory=list)
    llm_provider_allowlist: list[str] | None = None
