import { OSS_NAV_ITEMS, SettingsNavItem } from "#/constants/settings-nav";
import { isSettingsPageHidden } from "#/utils/settings-utils";
import { useConfig } from "#/hooks/query/use-config";
import { useSettings } from "./query/use-settings";
import { I18nKey } from "#/i18n/declaration";

export type SettingsNavRenderedItem =
  | {
      type: "item";
      item: SettingsNavItem;
      disabled?: boolean;
      disabledAgentName?: string;
    }
  | { type: "header"; text: I18nKey }
  | { type: "divider" };

export function useSettingsNavItems(): SettingsNavRenderedItem[] {
  const { data: config } = useConfig();
  const { data: settings } = useSettings();
  const featureFlags = config?.feature_flags;

  const isAcpAgent = settings?.agent_settings?.agent_kind === "acp";
  const acpServerName = isAcpAgent
    ? (config?.acp_providers?.find(
        ({ key }) => key === settings?.agent_settings?.acp_server,
      )?.display_name ?? "ACP Agent")
    : null;

  const items = OSS_NAV_ITEMS.filter(
    (item) => !isSettingsPageHidden(item.to, featureFlags),
  );

  return items.map((item) => {
    if (isAcpAgent && item.disabledByAcp) {
      return {
        type: "item" as const,
        item,
        disabled: true,
        disabledAgentName: acpServerName ?? undefined,
      };
    }
    return { type: "item" as const, item };
  });
}
