import React from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { useSettingsNavItems } from "#/hooks/use-settings-nav-items";
import DocumentIcon from "#/icons/document.svg?react";
import { ContextMenuNavLink } from "../context-menu/context-menu-nav-link";
import { ContextMenuContainer } from "../context-menu/context-menu-container";

interface UserContextMenuProps {
  onClose: () => void;
}

export function UserContextMenu({ onClose }: UserContextMenuProps) {
  const { t } = useTranslation();
  const settingsNavItems = useSettingsNavItems();

  return (
    <ContextMenuContainer testId="user-context-menu" onClose={onClose}>
      <div className="flex flex-col gap-3 w-[248px]">
        <h3 className="text-lg font-semibold text-white">
          {t(I18nKey.SETTINGS$TITLE)}
        </h3>

        <div className="flex flex-col items-start gap-0 w-full">
          {settingsNavItems.map((renderedItem) => {
            if (renderedItem.type !== "item") {
              return null;
            }

            return (
              <ContextMenuNavLink
                key={renderedItem.item.to}
                item={renderedItem.item}
                onClick={onClose}
                disabled={renderedItem.disabled}
                disabledAgentName={renderedItem.disabledAgentName}
              />
            );
          })}
        </div>

        <a
          href="https://docs.openhands.dev"
          target="_blank"
          rel="noopener noreferrer"
          onClick={onClose}
          className="flex items-center gap-2 p-2 cursor-pointer hover:bg-white/10 hover:text-white rounded w-full text-xs"
        >
          <DocumentIcon className="text-white" width={16} height={16} />
          {t(I18nKey.SIDEBAR$DOCS)}
        </a>
      </div>
    </ContextMenuContainer>
  );
}
