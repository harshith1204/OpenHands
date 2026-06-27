/**
 * OSS-only app mode hook. Always reports open-source / self-hosted mode.
 */
export function useAppMode() {
  return {
    isOss: true,
    isSaas: false,
    isCloud: false,
    isSelfHosted: false,
    isEnterpriseSelfHosted: false,
    isEnterpriseCloud: false,
    appMode: "oss" as const,
    deploymentMode: undefined,
  };
}
