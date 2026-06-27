import React from "react";
import { useTranslation } from "react-i18next";
import { ModelSelector } from "#/components/shared/modals/settings/model-selector";
import { useAgentSettingsSchema } from "#/hooks/query/use-agent-settings-schema";
import { useSettings } from "#/hooks/query/use-settings";
import { SettingsInput } from "#/components/features/settings/settings-input";
import { HelpLink } from "#/ui/help-link";
import { KeyStatusIcon } from "#/components/features/settings/key-status-icon";
import {
  SdkSectionHeaderProps,
  SdkSectionPage,
} from "#/components/features/settings/sdk-settings/sdk-section-page";
import { I18nKey } from "#/i18n/declaration";
import { Settings, SettingsSchema } from "#/types/settings";
import { useSaveLlmProfile } from "#/hooks/mutation/use-save-llm-profile";
import { useActivateLlmProfile } from "#/hooks/mutation/use-activate-llm-profile";

const DEFAULT_PROFILE_NAME = "Default";

const LLM_EXCLUDED_KEYS = new Set([
  "llm.model",
  "llm.api_key",
  "llm.base_url",
  "llm.auth_type",
  "llm.subscription_vendor",
]);

function LlmSettingsScreen() {
  const { t } = useTranslation();
  const { data: settings } = useSettings();
  useAgentSettingsSchema(settings?.agent_settings_schema);

  const saveProfile = useSaveLlmProfile();
  const activateProfile = useActivateLlmProfile();
  const lastSavedApiKeyTypedRef = React.useRef(false);

  const buildHeader = React.useCallback(
    ({ values, isDisabled, onChange }: SdkSectionHeaderProps) => {
      const modelValue =
        typeof values["llm.model"] === "string" ? values["llm.model"] : "";
      const apiKeySet = settings?.llm_api_key_set;

      return (
        <div
          className="flex flex-col gap-6"
          data-testid="llm-settings-form-basic"
        >
          <ModelSelector
            currentModel={modelValue || undefined}
            onChange={(_provider, model) => {
              if (model) {
                onChange("llm.model", `xai/${model}`);
              }
            }}
            wrapperClassName="!flex-col !gap-6"
            isDisabled={isDisabled}
          />

          <SettingsInput
            testId="llm-api-key-input"
            label={t(I18nKey.SETTINGS_FORM$API_KEY)}
            type="password"
            className="w-full"
            value={
              typeof values["llm.api_key"] === "string"
                ? values["llm.api_key"]
                : ""
            }
            placeholder={apiKeySet ? "<hidden>" : ""}
            onChange={(value) => onChange("llm.api_key", value)}
            isDisabled={isDisabled}
            startContent={
              apiKeySet ? <KeyStatusIcon isSet={apiKeySet} /> : undefined
            }
          />

          <HelpLink
            testId="llm-api-key-help-anchor"
            text={t(I18nKey.SETTINGS$DONT_KNOW_API_KEY)}
            linkText={t(I18nKey.SETTINGS$CLICK_FOR_INSTRUCTIONS)}
            href="https://console.x.ai/"
          />
        </div>
      );
    },
    [settings?.llm_api_key_set, t],
  );

  const buildPayload = React.useCallback(
    (
      defaultPayload: Record<string, unknown>,
      context: {
        values: Record<string, string | boolean>;
        dirty: Record<string, boolean>;
        view: "basic" | "advanced" | "all";
      },
    ) => {
      const typedApiKey =
        typeof context.values["llm.api_key"] === "string"
          ? context.values["llm.api_key"].trim()
          : "";
      lastSavedApiKeyTypedRef.current = typedApiKey.length > 0;
      return defaultPayload;
    },
    [],
  );

  const handleSaveSuccess = React.useCallback(async () => {
    try {
      await saveProfile.mutateAsync({
        name: DEFAULT_PROFILE_NAME,
        request: {
          include_secrets: true,
          preserve_existing_api_key: !lastSavedApiKeyTypedRef.current,
        },
      });
      await activateProfile.mutateAsync(DEFAULT_PROFILE_NAME);
    } catch {
      // Best-effort sync to Default profile after settings save.
    }
  }, [activateProfile, saveProfile]);

  const getInitialView = React.useCallback(
    (_currentSettings: Settings, _filteredSchema: SettingsSchema) =>
      "basic" as const,
    [],
  );

  return (
    <SdkSectionPage
      settingsSources={[
        {
          settingsSource: "agent_settings",
          sectionKeys: ["llm"],
          excludeKeys: LLM_EXCLUDED_KEYS,
          variant: "openhands",
        },
      ]}
      header={buildHeader}
      buildPayload={buildPayload}
      onSaveSuccess={handleSaveSuccess}
      getInitialView={getInitialView}
      forceShowAdvancedView={false}
      allowAdvancedView={false}
      allowAllView={false}
      testId="llm-settings-screen"
    />
  );
}

export default LlmSettingsScreen;
