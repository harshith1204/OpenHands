import { openHands } from "../open-hands-axios";
import {
  AzureDevOpsWebhookStatus,
  AzureDevOpsWebhookInstallationResult,
  GitLabResourcesResponse,
  ReinstallWebhookRequest,
  ResourceIdentifier,
  ResourceInstallationResult,
} from "./integration-service.types";

export const integrationService = {
  getGitLabResources: async (): Promise<GitLabResourcesResponse> => {
    const { data } = await openHands.get<GitLabResourcesResponse>(
      "/integration/gitlab/resources",
    );
    return data;
  },

  reinstallGitLabWebhook: async ({
    resource,
  }: {
    resource: ResourceIdentifier;
  }): Promise<ResourceInstallationResult> => {
    const requestBody: ReinstallWebhookRequest = { resource };
    const { data } = await openHands.post<ResourceInstallationResult>(
      "/integration/gitlab/reinstall-webhook",
      requestBody,
    );
    return data;
  },

  getAzureDevOpsResources: async (): Promise<AzureDevOpsWebhookStatus> => {
    const { data } = await openHands.get<AzureDevOpsWebhookStatus>(
      "/integration/azure-devops/resources",
    );
    return data;
  },

  reinstallAzureDevOpsWebhook:
    async (): Promise<AzureDevOpsWebhookInstallationResult> => {
      const { data } =
        await openHands.post<AzureDevOpsWebhookInstallationResult>(
          "/integration/azure-devops/reinstall-webhook",
        );
      return data;
    },

  uninstallAzureDevOpsWebhook:
    async (): Promise<AzureDevOpsWebhookInstallationResult> => {
      const { data } =
        await openHands.post<AzureDevOpsWebhookInstallationResult>(
          "/integration/azure-devops/uninstall-webhook",
        );
      return data;
    },
};
