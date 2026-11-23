export type Account = {
  id: string;
  email: string;
  display_name: string;
  is_administrator: boolean;
  is_menu_maintainer: boolean;
};
export type Identity = { account: Account; csrf_token: string };

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...options,
    credentials: 'same-origin',
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      body.detail || 'Could not reach the office. Try again.',
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

export const api = {
  session: () => request<Identity>('/auth/session'),
  home: () => request<{ active_run: null; history: [] }>('/office/home'),
  async login(email: string, password: string) {
    const { csrf_token } = await request<{ csrf_token: string }>('/auth/csrf');
    return request<Identity>('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrf_token,
      },
      body: JSON.stringify({ email, password }),
    });
  },
  logout: (csrf: string) =>
    request<void>('/auth/logout', {
      method: 'POST',
      headers: { 'X-CSRF-Token': csrf },
    }),
};
