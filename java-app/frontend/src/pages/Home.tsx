import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { businessesList, type BusinessDto } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const { user, isAuth, logout } = useAuth();
  const [businesses, setBusinesses] = useState<BusinessDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    businessesList(0, 20)
      .then((page) => setBusinesses(page.content))
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-content mx-auto px-6 py-6 sm:py-8">
      <header className="flex flex-wrap justify-between items-center gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 m-0">Hidden Gems</h1>
          <p className="text-slate-500 text-sm mt-1">Discover small local businesses in Richmond, VA</p>
        </div>
        <div className="flex gap-2 items-center">
          {isAuth && user && (
            <span className="text-sm text-slate-500">Logged in as <strong>{user.username}</strong></span>
          )}
          {isAuth ? (
            <button type="button" className="btn btn-secondary" onClick={logout}>Exit</button>
          ) : (
            <>
              <Link to="/login" className="btn btn-primary">Log in</Link>
              <Link to="/register" className="btn btn-secondary">Create account</Link>
            </>
          )}
        </div>
      </header>

      {loading && <p className="text-slate-500">Loading businesses…</p>}
      {error && <p className="error-message">{error}</p>}
      {!loading && !error && businesses.length === 0 && (
        <div className="card text-center text-slate-500">
          No businesses in the directory yet. Run the backend with the default seeder to load sample data.
        </div>
      )}
      {!loading && businesses.length > 0 && (
        <ul className="list-none p-0 m-0 flex flex-col gap-4">
          {businesses.map((b) => (
            <li key={b.id}>
              <Link to={`/businesses/${b.id}`} className="no-underline text-inherit block">
                <div className="card hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <h2 className="text-lg font-semibold text-slate-900 m-0 mb-1">{b.name}</h2>
                      {b.category && <span className="text-sm text-slate-500">{b.category}</span>}
                      {b.rating != null && (
                        <p className="text-sm m-0 mt-1">★ {b.rating} {b.reviewCount != null ? `(${b.reviewCount} reviews)` : ''}</p>
                      )}
                    </div>
                    <span className="text-primary font-semibold text-sm shrink-0">View →</span>
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
