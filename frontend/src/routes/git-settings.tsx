import React from "react";
import { useTranslation } from "react-i18next";
import { useConfig } from "#/hooks/query/use-config";
import { useSettings } from "#/hooks/query/use-settings";
import { BrandButton } from "#/components/features/settings/brand-button";
import { useDeleteGitProviders } from "#/hooks/mutation/use-delete-git-providers";
import { GitHubTokenInput } from "#/components/features/settings/git-settings/github-token-input";
import { GitLabTokenInput } from "#/components/features/settings/git-settings/gitlab-token-input";
import { AzureDevOpsTokenInput } from "#/components/features/settings/git-settings/azure-devops-token-input";
import { ForgejoTokenInput } from "#/components/features/settings/git-settings/forgejo-token-input";
import { ConfigureGitHubRepositoriesAnchor } from "#/components/features/settings/git-settings/configure-github-repositories-anchor";
import { I18nKey } from "#/i18n/declaration";
import {
  displayErrorToast,
  displaySuccessToast,
} from "#/utils/custom-toast-handlers";
import { retrieveAxiosErrorMessage } from "#/utils/retrieve-axios-error-message";
import { GitSettingInputsSkeleton } from "#/components/features/settings/git-settings/github-settings-inputs-skeleton";
import { useAddGitProviders } from "#/hooks/mutation/use-add-git-providers";
import { useUserProviders } from "#/hooks/use-user-providers";

function GitSettingsScreen() {
  const { t } = useTranslation();

  const { mutate: saveGitProviders, isPending } = useAddGitProviders();
  const { mutate: disconnectGitTokens, isPending: isDisconnecting } =
    useDeleteGitProviders();

  const { data: settings, isLoading } = useSettings();
  const { providers } = useUserProviders();
  const { data: config } = useConfig();

  const isSaas = config?.app_mode === "saas";
  const shouldRenderGitHubConfigureButton = isSaas && config?.github_app_slug;

  const [githubTokenInputHasValue, setGithubTokenInputHasValue] =
    React.useState(false);
  const [gitlabTokenInputHasValue, setGitlabTokenInputHasValue] =
    React.useState(false);
  const [azureDevOpsTokenInputHasValue, setAzureDevOpsTokenInputHasValue] =
    React.useState(false);
  const [forgejoTokenInputHasValue, setForgejoTokenInputHasValue] =
    React.useState(false);

  const [githubHostInputHasValue, setGithubHostInputHasValue] =
    React.useState(false);
  const [gitlabHostInputHasValue, setGitlabHostInputHasValue] =
    React.useState(false);
  const [azureDevOpsHostInputHasValue, setAzureDevOpsHostInputHasValue] =
    React.useState(false);
  const [forgejoHostInputHasValue, setForgejoHostInputHasValue] =
    React.useState(false);

  const existingGithubHost = settings?.provider_tokens_set.github;
  const existingGitlabHost = settings?.provider_tokens_set.gitlab;
  const existingAzureDevOpsHost = settings?.provider_tokens_set.azure_devops;
  const existingForgejoHost = settings?.provider_tokens_set.forgejo;

  const isGitHubTokenSet = providers.includes("github");
  const isGitLabTokenSet = providers.includes("gitlab");
  const isAzureDevOpsTokenSet = providers.includes("azure_devops");
  const isForgejoTokenSet = providers.includes("forgejo");

  const formAction = async (formData: FormData) => {
    const disconnectButtonClicked =
      formData.get("disconnect-tokens-button") !== null;

    if (disconnectButtonClicked) {
      disconnectGitTokens(undefined, {
        onSuccess: () => {
          displaySuccessToast(t(I18nKey.SETTINGS$SAVED));
        },
        onError: (error) => {
          const errorMessage = retrieveAxiosErrorMessage(error);
          displayErrorToast(errorMessage || t(I18nKey.ERROR$GENERIC));
        },
      });
      return;
    }

    const githubToken = (
      formData.get("github-token-input")?.toString() || ""
    ).trim();
    const gitlabToken = (
      formData.get("gitlab-token-input")?.toString() || ""
    ).trim();
    const azureDevOpsToken = (
      formData.get("azure-devops-token-input")?.toString() || ""
    ).trim();
    const forgejoToken = (
      formData.get("forgejo-token-input")?.toString() || ""
    ).trim();
    const githubHost = (
      formData.get("github-host-input")?.toString() || ""
    ).trim();
    const gitlabHost = (
      formData.get("gitlab-host-input")?.toString() || ""
    ).trim();
    const azureDevOpsHost = (
      formData.get("azure-devops-host-input")?.toString() || ""
    ).trim();
    const forgejoHost = (
      formData.get("forgejo-host-input")?.toString() || ""
    ).trim();

    const providerTokens: Record<string, { token: string; host: string }> = {
      github: { token: githubToken, host: githubHost },
      gitlab: { token: gitlabToken, host: gitlabHost },
      azure_devops: { token: azureDevOpsToken, host: azureDevOpsHost },
      forgejo: { token: forgejoToken, host: forgejoHost },
    };

    saveGitProviders(
      {
        providers: providerTokens,
      },
      {
        onSuccess: () => {
          displaySuccessToast(t(I18nKey.SETTINGS$SAVED));
        },
        onError: (error) => {
          const errorMessage = retrieveAxiosErrorMessage(error);
          displayErrorToast(errorMessage || t(I18nKey.ERROR$GENERIC));
        },
        onSettled: () => {
          setGithubTokenInputHasValue(false);
          setGitlabTokenInputHasValue(false);
          setAzureDevOpsTokenInputHasValue(false);
          setForgejoTokenInputHasValue(false);
          setGithubHostInputHasValue(false);
          setGitlabHostInputHasValue(false);
          setAzureDevOpsHostInputHasValue(false);
          setForgejoHostInputHasValue(false);
        },
      },
    );
  };

  const formIsClean =
    !githubTokenInputHasValue &&
    !gitlabTokenInputHasValue &&
    !azureDevOpsTokenInputHasValue &&
    !forgejoTokenInputHasValue &&
    !githubHostInputHasValue &&
    !gitlabHostInputHasValue &&
    !azureDevOpsHostInputHasValue &&
    !forgejoHostInputHasValue;

  return (
    <form
      data-testid="git-settings-screen"
      action={formAction}
      className="flex flex-col h-full justify-between"
    >
      {!isLoading && (
        <div className="flex flex-col gap-4">
          {shouldRenderGitHubConfigureButton && (
            <>
              <div className="pb-1 flex flex-col">
                <h3 className="text-xl font-medium text-white">
                  {t(I18nKey.SETTINGS$GITHUB)}
                </h3>
                <ConfigureGitHubRepositoriesAnchor
                  slug={config.github_app_slug!}
                />
              </div>
              <div className="w-1/2 border-b border-gray-200" />
            </>
          )}

          <GitHubTokenInput
            name="github-token-input"
            isGitHubTokenSet={isGitHubTokenSet}
            onChange={(value) => {
              setGithubTokenInputHasValue(!!value);
            }}
            onGitHubHostChange={(value) => {
              setGithubHostInputHasValue(!!value);
            }}
            githubHostSet={existingGithubHost}
          />

          <GitLabTokenInput
            name="gitlab-token-input"
            isGitLabTokenSet={isGitLabTokenSet}
            onChange={(value) => {
              setGitlabTokenInputHasValue(!!value);
            }}
            onGitLabHostChange={(value) => {
              setGitlabHostInputHasValue(!!value);
            }}
            gitlabHostSet={existingGitlabHost}
          />

          <AzureDevOpsTokenInput
            name="azure-devops-token-input"
            isAzureDevOpsTokenSet={isAzureDevOpsTokenSet}
            onChange={(value) => {
              setAzureDevOpsTokenInputHasValue(!!value);
            }}
            onAzureDevOpsHostChange={(value) => {
              setAzureDevOpsHostInputHasValue(!!value);
            }}
            azureDevOpsHostSet={existingAzureDevOpsHost}
          />

          <ForgejoTokenInput
            name="forgejo-token-input"
            isForgejoTokenSet={isForgejoTokenSet}
            onChange={(value) => {
              setForgejoTokenInputHasValue(!!value);
            }}
            onForgejoHostChange={(value) => {
              setForgejoHostInputHasValue(!!value);
            }}
            forgejoHostSet={existingForgejoHost}
          />
        </div>
      )}

      {isLoading && <GitSettingInputsSkeleton />}

      <div className="flex gap-6 p-6 justify-end">
        <BrandButton
          testId="disconnect-tokens-button"
          name="disconnect-tokens-button"
          type="submit"
          variant="secondary"
          isDisabled={
            isDisconnecting ||
            (!isGitHubTokenSet &&
              !isGitLabTokenSet &&
              !isAzureDevOpsTokenSet &&
              !isForgejoTokenSet)
          }
        >
          {t(I18nKey.GIT$DISCONNECT_TOKENS)}
        </BrandButton>
        <BrandButton
          testId="submit-button"
          type="submit"
          variant="primary"
          isDisabled={isPending || formIsClean}
        >
          {!isPending && t("SETTINGS$SAVE_CHANGES")}
          {isPending && t("SETTINGS$SAVING")}
        </BrandButton>
      </div>
    </form>
  );
}

export default GitSettingsScreen;
