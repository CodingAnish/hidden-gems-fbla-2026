import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authLogin } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [emailOrUsername, setEmailOrUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setAuth } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await authLogin({ emailOrUsername: emailOrUsername.trim(), password });
      setAuth(res);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-content mx-auto px-6 py-8 sm:py-12">
      <div className="card max-w-md mx-auto">
        <h1 className="text-2xl font-bold text-slate-900 mb-1">Hidden Gems</h1>
        <p className="text-slate-500 text-sm mb-6">Discover local businesses in Richmond, VA</p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="label">Email or username</label>
            <input
              className="input"
              type="text"
              value={emailOrUsername}
              onChange={(e) => setEmailOrUsername(e.target.value)}
              required
              autoComplete="username"
              placeholder="you@example.com or username"
            />
          </div>
          <div className="form-group">
            <label className="label">Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="btn btn-primary w-full mt-3" disabled={loading}>
            {loading ? 'Signing in…' : 'Log in'}
          </button>
        </form>
        <p className="mt-6 text-sm text-slate-500">
          Don't have an account? <Link to="/register" className="text-primary hover:underline font-medium">Create account</Link>
        </p>
      </div>
    </div>
  );
}
