import { SdkSectionPage } from "#/components/features/settings/sdk-settings/sdk-section-page";

const CONVERSATION_OWNED_AGENT_VERIFICATION_FIELD_KEYS = new Set([
  "verification.confirmation_mode",
  "verification.security_analyzer",
]);

function VerificationSettingsScreen() {
  return (
    <SdkSectionPage
      settingsSources={[
        {
          settingsSource: "conversation_settings",
          sectionKeys: ["verification"],
        },
        {
          settingsSource: "agent_settings",
          sectionKeys: ["verification"],
          excludeKeys: CONVERSATION_OWNED_AGENT_VERIFICATION_FIELD_KEYS,
        },
      ]}
      testId="verification-settings-screen"
    />
  );
}

export default VerificationSettingsScreen;
