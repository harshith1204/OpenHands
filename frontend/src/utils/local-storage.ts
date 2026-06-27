// Local storage keys used by the OSS frontend.
export const LOCAL_STORAGE_KEYS = {
  LOGIN_METHOD: "openhands_login_method",
};

// Login methods for git provider OAuth (legacy; OSS uses token-based git settings).
export enum LoginMethod {
  GITHUB = "github",
  GITLAB = "gitlab",
  AZURE_DEVOPS = "azure_devops",
}

export const setLoginMethod = (method: LoginMethod): void => {
  localStorage.setItem(LOCAL_STORAGE_KEYS.LOGIN_METHOD, method);
};

export const getLoginMethod = (): LoginMethod | null => {
  const method = localStorage.getItem(LOCAL_STORAGE_KEYS.LOGIN_METHOD);
  return method as LoginMethod | null;
};

export const clearLoginData = (): void => {
  localStorage.removeItem(LOCAL_STORAGE_KEYS.LOGIN_METHOD);
};
