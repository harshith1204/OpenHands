// xAI is the only LLM provider in this deployment.
export const MAP_PROVIDER = {
  xai: "xAI",
};

export const mapProvider = (provider: string) =>
  Object.keys(MAP_PROVIDER).includes(provider)
    ? MAP_PROVIDER[provider as keyof typeof MAP_PROVIDER]
    : provider;

export const getProviderId = (displayName: string): string => {
  const entry = Object.entries(MAP_PROVIDER).find(
    ([, value]) => value === displayName,
  );
  return entry ? entry[0] : displayName;
};
