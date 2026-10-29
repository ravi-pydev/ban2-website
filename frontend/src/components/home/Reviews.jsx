import Icon from '../Icon.jsx';
import { FeedbackButton } from '../popups.jsx';

/* Review building blocks, used by the Reviews page and the Happy Clients cards. */

export function Stars({ rating, size }) {
  return (
    <span className={`stars${size ? ` stars-${size}` : ''}`} role="img" aria-label={`${rating} out of 5 stars`}>
      {[1, 2, 3, 4, 5].map((n) => (
        <span key={n} className={n <= Math.round(rating) ? 'on' : 'off'} aria-hidden="true">★</span>
      ))}
    </span>
  );
}

/** Average rating card with the 5★–1★ breakdown. Bars become filter buttons when onFilter is given. */
export function ReviewSummary({ summary, filter, onFilter }) {
  const max = Math.max(1, ...summary.breakdown.map((b) => b.count));
  return (
    <aside className="review-summary reveal">
      <p className="review-average">{summary.average.toFixed(1)}</p>
      <Stars rating={summary.average} size="lg" />
      <p className="review-count">Based on {summary.count} review{summary.count === 1 ? '' : 's'}</p>
      <ul className="review-bars">
        {summary.breakdown.map((b) => {
          const row = (
            <>
              <span>{b.stars}★</span>
              <div className="bar"><span style={{ width: `${(b.count / max) * 100}%` }} /></div>
              <span>{b.count}</span>
            </>
          );
          return (
            <li key={b.stars}>
              {onFilter
                ? <button type="button" className={`bar-filter${filter === b.stars ? ' active' : ''}`}
                    disabled={!b.count} aria-pressed={filter === b.stars}
                    aria-label={`Show ${b.stars}-star reviews (${b.count})`}
                    onClick={() => onFilter(filter === b.stars ? null : b.stars)}>{row}</button>
                : row}
            </li>
          );
        })}
      </ul>
      <FeedbackButton>Write a review</FeedbackButton>
    </aside>
  );
}

export function ReviewList({ reviews }) {
  return (
    <ol className="review-list">
      {reviews.map((r, i) => (
        <li key={`${r.name}-${i}`} className="review-item">
          <div className="review-head">
            <span className="avatar"><Icon name="user" /></span>
            <div>
              <strong>{r.name}</strong>
              <small>{r.role}</small>
            </div>
            <Stars rating={r.rating} />
          </div>
          <p>{r.quote}</p>
          <div className="review-meta">
            {r.event && <span>{r.event}</span>}
            {r.date && <span>{r.date}</span>}
            {r.sample && <span className="sample-tag">Sample</span>}
          </div>
        </li>
      ))}
    </ol>
  );
}
