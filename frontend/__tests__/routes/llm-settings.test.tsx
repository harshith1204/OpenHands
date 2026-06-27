import { render, screen } from "@testing-library/react";
import { createRoutesStub } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import i18next from "i18next";
import { I18nextProvider } from "react-i18next";
import LlmSettingsScreen from "#/routes/llm-settings";
import { MOCK_DEFAULT_USER_SETTINGS } from "#/mocks/handlers";

vi.mock("#/hooks/query/use-provider-models", () => ({
  useProviderModels: () => ({
    data: [
      { name: "grok-4.3", verified: true, hidden: false },
      { name: "grok-build-0.1", verified: true, hidden: false },
    ],
    isLoading: false,
    error: null,
  }),
  providerModelsQueryOptions: () => ({ queryKey: ["provider-models", "xai"] }),
}));

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

const LlmSettingsRouterStub = createRoutesStub([
  {
    Component: LlmSettingsScreen,
    path: "/settings/llm",
  },
]);

const renderLlmSettingsScreen = () =>
  render(
    <QueryClientProvider client={queryClient}>
      <I18nextProvider i18n={i18next}>
        <LlmSettingsRouterStub initialEntries={["/settings/llm"]} />
      </I18nextProvider>
    </QueryClientProvider>,
  );

describe("LlmSettingsScreen", () => {
  beforeEach(() => {
    i18next.init({ lng: "en", resources: {} });
    queryClient.setQueryData(
      ["settings", "personal", null],
      MOCK_DEFAULT_USER_SETTINGS,
    );
    queryClient.setQueryData(
      ["agent-settings-schema"],
      MOCK_DEFAULT_USER_SETTINGS.agent_settings_schema,
    );
  });

  it("renders direct xAI model and API key fields without profiles UI", () => {
    renderLlmSettingsScreen();

    expect(screen.getByTestId("llm-settings-form-basic")).toBeInTheDocument();
    expect(screen.getByTestId("llm-model-input")).toBeInTheDocument();
    expect(screen.getByTestId("llm-api-key-input")).toBeInTheDocument();
    expect(screen.queryByTestId("llm-provider-input")).not.toBeInTheDocument();
    expect(screen.queryByTestId("add-llm-profile")).not.toBeInTheDocument();
    expect(screen.queryByTestId("llm-back-to-profiles")).not.toBeInTheDocument();
  });
});
