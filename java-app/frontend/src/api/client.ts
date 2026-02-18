const API_BASE = '/api';

function getToken(): string | null {
  return localStorage.getItem('token');
}

function getAuthHeaders(): HeadersInit {
  const token = getToken();
  const headers: HeadersInit = { 'Content-Type': 'application/json' };
  if (token) (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  return headers;
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: { ...getAuthHeaders(), ...(options.headers as Record<string, string>) },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const message = (data as { error?: string })?.error || res.statusText;
    throw new Error(message);
  }
  return data as T;
}

export interface AuthResponse {
  token: string;
  type: string;
  userId: number;
  username: string;
  email: string;
}

export interface LoginRequest {
  emailOrUsername: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export function authLogin(body: LoginRequest) {
  return request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify(body) });
}

export function authRegister(body: RegisterRequest) {
  return request<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify(body) });
}

export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/';
}

export function setAuth(auth: AuthResponse) {
  localStorage.setItem('token', auth.token);
  localStorage.setItem('user', JSON.stringify({ userId: auth.userId, username: auth.username, email: auth.email }));
}

export function getStoredUser(): { userId: number; username: string; email: string } | null {
  const raw = localStorage.getItem('user');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as { userId: number; username: string; email: string };
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export interface BusinessDto {
  id: number;
  name: string;
  category: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  zip: string | null;
  phone: string | null;
  description: string | null;
  rating: number | null;
  reviewCount: number | null;
  favorited: boolean | null;
}

export interface PageResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
}

export function businessesList(page = 0, size = 20) {
  return request<PageResponse<BusinessDto>>(`/businesses?page=${page}&size=${size}`);
}

export function businessById(id: number) {
  return request<BusinessDto>(`/businesses/${id}`);
}

export function businessesSearch(q: string, page = 0) {
  const params = new URLSearchParams({ q, page: String(page), size: '20' });
  return request<PageResponse<BusinessDto>>(`/businesses/search?${params}`);
}

export function businessesByCity(city: string, page = 0) {
  return request<PageResponse<BusinessDto>>(`/businesses/city/${encodeURIComponent(city)}?page=${page}&size=20`);
}
