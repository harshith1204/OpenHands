import React from "react";
import { ModalBackdrop } from "#/components/shared/modals/modal-backdrop";
import { Typography } from "#/ui/typography";

interface SettingsModalBaseProps {
  isOpen: boolean;
  title: string;
  footer: React.ReactNode;
  children: React.ReactNode;
}

export function ApiKeyModalBase({
  isOpen,
  title,
  footer,
  children,
}: SettingsModalBaseProps) {
  if (!isOpen) {
    return null;
  }

  return (
    <ModalBackdrop>
      <div className="border border-tertiary p-6 rounded-lg max-w-md w-full flex flex-col gap-4 bg-base-secondary">
        <Typography.H3>{title}</Typography.H3>
        {children}
        <div className="flex gap-3">{footer}</div>
      </div>
    </ModalBackdrop>
  );
}
