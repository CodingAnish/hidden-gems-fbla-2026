import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from 'react';
import { getStoredUser, isAuthenticated, setAuth as storeAuth, logout as apiLogout, type AuthResponse } from '../api/client';

interface User {
  userId: number;
  username: string;
  email: string;
}

interface AuthContextValue {
  user: User | null;
  isAuth: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
  setAuth: (auth: AuthResponse) => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(() => getStoredUser());
  const isAuth = isAuthenticated();
  const setUser = useCallback((u: User | null) => setUserState(u), []);
  const setAuth = useCallback((auth: AuthResponse) => {
    storeAuth(auth);
    setUserState({ userId: auth.userId, username: auth.username, email: auth.email });
  }, []);
  const logout = useCallback(() => {
    apiLogout();
    setUserState(null);
  }, []);

  useEffect(() => {
    if (!isAuthenticated()) setUserState(null);
    else if (!user) setUserState(getStoredUser());
  }, [user]);

  return (
    <AuthContext.Provider value={{ user, isAuth, setUser, logout, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
