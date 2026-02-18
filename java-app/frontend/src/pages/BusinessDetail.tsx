import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { businessById, type BusinessDto } from '../api/client';

export default function BusinessDetail() {
  const { id } = useParams<{ id: string }>();
  const [business, setBusiness] = useState<BusinessDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    businessById(Number(id))
      .then(setBusiness)
      .catch((err) => setError(err instanceof Error ? err.message : 'Not found'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="max-w-content mx-auto px-6 py-8">Loading…</div>;
  if (error || !business) {
    return (
      <div className="max-w-content mx-auto px-6 py-8">
        <p className="error-message">{error || 'Business not found.'}</p>
        <Link to="/" className="btn btn-secondary mt-4 inline-block">Back to directory</Link>
      </div>
    );
  }

  return (
    <div className="max-w-content mx-auto px-6 py-6 sm:py-8">
      <Link to="/" className="inline-block mb-4 text-primary text-sm font-medium hover:underline">← Back to directory</Link>
      <div className="card">
        <h1 className="text-2xl font-bold text-slate-900 m-0 mb-2">{business.name}</h1>
        {business.category && <p className="text-slate-500 text-sm m-0 mb-4">{business.category}</p>}
        {business.rating != null && (
          <p className="m-0 mb-4">★ {business.rating} {business.reviewCount != null ? `(${business.reviewCount} reviews)` : ''}</p>
        )}
        {business.address && (
          <p className="text-sm m-0 mb-1">
            {business.address}
            {business.city && `, ${business.city}`}
            {business.state && ` ${business.state}`}
            {business.zip && ` ${business.zip}`}
          </p>
        )}
        {business.phone && (
          <p className="text-sm m-0 mb-4"><a href={`tel:${business.phone}`} className="text-primary hover:underline">{business.phone}</a></p>
        )}
        {business.description && <p className="m-0 text-slate-600 leading-relaxed">{business.description}</p>}
      </div>
    </div>
  );
}
