import { useQuery } from "@tanstack/react-query";
import React from "react";
import { usePostHog } from "posthog-js/react";
import { useConfig } from "./use-config";
import UserService from "#/api/user-service/user-service.api";
import { useShouldShowGitFeatures } from "#/hooks/use-should-show-git-features";

export const useGitUser = () => {
  const posthog = usePostHog();
  const { data: config } = useConfig();

  // Use the Git-specific hook to determine if we should fetch user data.
  // This requires a Git provider to be configured, not just authentication.
  const shouldFetchUser = useShouldShowGitFeatures();

  const user = useQuery({
    queryKey: ["user"],
    queryFn: UserService.getUser,
    enabled: shouldFetchUser,
    retry: false,
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 15, // 15 minutes
  });

  React.useEffect(() => {
    if (user.data) {
      posthog.identify(user.data.login, {
        company: user.data.company,
        name: user.data.name,
        email: user.data.email,
        user: user.data.login,
        mode: config?.app_mode || "oss",
      });
    }
  }, [user.data]);

  return user;
};
