import {
  useQuery,
  useInfiniteQuery,
  InfiniteData,
} from "@tanstack/react-query";
import { SecretsService } from "#/api/secrets-service";
import { useIsAuthed } from "#/hooks/query/use-is-authed";
import { CustomSecretPage } from "#/api/secrets-service.types";

/**
 * @deprecated Use useSearchSecrets instead for paginated access
 */
export const useGetSecrets = () => {
  const { data: isAuthed } = useIsAuthed();

  return useQuery({
    queryKey: ["secrets"],
    queryFn: SecretsService.getSecrets,
    enabled: !!isAuthed,
  });
};

interface UseSearchSecretsOptions {
  nameContains?: string;
  pageSize?: number;
  enabled?: boolean;
}

export const useSearchSecrets = (options: UseSearchSecretsOptions = {}) => {
  const { nameContains, pageSize = 30, enabled = true } = options;
  const { data: isAuthed } = useIsAuthed();

  const isEnabled = enabled && !!isAuthed;

  const query = useInfiniteQuery<
    CustomSecretPage,
    Error,
    InfiniteData<CustomSecretPage>,
    [string, string | undefined, number],
    string | null
  >({
    queryKey: ["secrets-search", nameContains, pageSize],
    queryFn: async ({ pageParam }) =>
      SecretsService.searchSecrets({
        name__contains: nameContains,
        page_id: pageParam ?? undefined,
        limit: pageSize,
      }),
    getNextPageParam: (lastPage) => lastPage.next_page_id,
    initialPageParam: null,
    enabled: isEnabled,
    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 15,
  });

  const onLoadMore = () => {
    if (query.hasNextPage && !query.isFetchingNextPage) {
      query.fetchNextPage();
    }
  };

  const secrets = query.data?.pages?.flatMap((page) => page.items) ?? [];

  return {
    data: secrets,
    isLoading: query.isLoading,
    isError: query.isError,
    hasNextPage: query.hasNextPage ?? false,
    isFetchingNextPage: query.isFetchingNextPage,
    fetchNextPage: query.fetchNextPage,
    onLoadMore,
    refetch: query.refetch,
  };
};
