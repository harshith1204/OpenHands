import { Provider } from "#/types/settings";

/**
 * Structured response from ``GET /api/options/models``.
 *
 * The backend is the single source of truth — the frontend no longer carries
 * its own hardcoded verified-model lists.
 */
export interface ModelsResponse {
  /** Flat list of ``provider/model`` strings (bare names already prefixed). */
  models: string[];
  /** Model names (without provider) that OpenHands has verified to work well. */
  verified_models: string[];
  /** Provider names shown in the "Verified" section of the model selector. */
  verified_providers: string[];
  /** Recommended default model id (e.g. ``xai/grok-4.3``). */
  default_model: string;
  /** ``provider/model`` strings the backend serves but does not promote
   *  (e.g. legacy alias routes on a managed LiteLLM proxy): not dropdown
   *  options, but saved settings referencing them still count as available.
   *  Optional so older backends (no field) behave as before. */
  hidden_models?: string[];
}

export interface WebClientFeatureFlags {
  enable_billing: boolean;
  hide_llm_settings: boolean;
  enable_linear: boolean;
  hide_users_page: boolean;
  hide_billing_page: boolean;
  hide_integrations_page: boolean;
  /** Hide personal workspaces from the org list/selector for users who
   *  belong to at least one team org (OHE "org-only" installs). */
  hide_personal_workspaces?: boolean;
  /** When false, hide the BYOK editing UI (custom model, base URL, API key)
   *  in LLM settings — users only pick from the managed model dropdown.
   *  Defaults to true (absent ⇒ allowed) so SaaS/existing installs are
   *  unaffected. Saved BYOK settings keep working at runtime either way. */
  allow_user_llm_configuration?: boolean;
  enable_acp?: boolean;
  enable_onboarding: boolean;
  enable_automations?: boolean;
}

export interface ACPModelOption {
  id: string;
  label: string;
}

export interface ACPProviderConfig {
  key: string;
  display_name: string;
  default_command: string[];
  default_model?: string | null;
  available_models?: ACPModelOption[];
  api_key_env_var?: string | null;
  base_url_env_var?: string | null;
}

export interface WebClientConfig {
  app_mode: "saas" | "oss";
  posthog_client_key: string | null;
  feature_flags: WebClientFeatureFlags;
  providers_configured: Provider[];
  maintenance_start_time: string | null;
  auth_url: string | null;
  recaptcha_site_key: string | null;
  faulty_models: string[];
  error_message: string | null;
  updated_at: string;
  github_app_slug: string | null;
  gitlab_enabled?: boolean;
  provider_default_hosts?: Partial<Record<Provider, string>>;
  slack_enabled?: boolean;
  acp_providers?: ACPProviderConfig[];
  llm_provider_allowlist?: string[] | null;
}
