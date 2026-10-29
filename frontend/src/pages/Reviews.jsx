import { useState } from 'react';
import Contact from '../components/home/Contact.jsx';
import { ReviewList, ReviewSummary, Stars } from '../components/home/Reviews.jsx';
import { FeedbackButton } from '../components/popups.jsx';
import { PageError, PageLoader } from '../components/Status.jsx';
import { useApi, useDocumentTitle, useReveal, useScrollToHash } from '../hooks.js';

const FILTERS = [null, 5, 4, 3, 2, 1];

export default function ReviewsPage({ site }) {
  const { data, error } = useApi('reviews/');
  const [filter, setFilter] = useState(null);
  useDocumentTitle(`Client Reviews | ${site.site_name}`);
  useReveal(!!data);
  useScrollToHash(!!data);

  if (error) return <PageError />;
  if (!data) return <PageLoader />;

  const { summary, reviews } = data;
  const counts = Object.fromEntries(summary.breakdown.map((b) => [b.stars, b.count]));
  const shown = filter ? reviews.filter((r) => r.rating === filter) : reviews;

  return (
    <>
      <section className="page-hero">
        <div className="hero-glow hero-glow-1" />
        <div className="container page-hero-inner reveal">
          <p className="kicker">Testimonials</p>
          <h1>Client Reviews</h1>
          <p className="page-hero-text">
            What clients say about working with {site.profile.name} — every published review, highest rated first.
          </p>
          {summary.count > 0 && (
            <div className="page-hero-rating">
              <strong>{summary.average.toFixed(1)}</strong>
              <Stars rating={summary.average} size="lg" />
              <span>{summary.count} review{summary.count === 1 ? '' : 's'}</span>
            </div>
          )}
        </div>
      </section>

      <section id="all-reviews" className="section">
        <div className="container">
          {summary.count === 0 ? (
            <div className="reviews-empty">
              <p className="lead-text">No reviews yet — be the first to share your experience.</p>
              <FeedbackButton className="btn btn-primary btn-lg">Write a review</FeedbackButton>
            </div>
          ) : (
            <div className="reviews-layout">
              <ReviewSummary summary={summary} filter={filter} onFilter={setFilter} />
              <div>
                <div className="review-filters" role="group" aria-label="Filter by rating">
                  {FILTERS.map((stars) => {
                    const count = stars ? counts[stars] : summary.count;
                    return (
                      <button key={stars ?? 'all'} type="button" disabled={!count}
                        className={`tag${filter === stars ? ' tag-solid' : ''}`}
                        aria-pressed={filter === stars} onClick={() => setFilter(stars)}>
                        {stars ? `${stars}★` : 'All'} <span className="filter-count">{count}</span>
                      </button>
                    );
                  })}
                </div>
                <p className="review-showing" aria-live="polite">
                  Showing {shown.length} {filter ? `${filter}-star ` : ''}review{shown.length === 1 ? '' : 's'}, highest rated first
                </p>
                <ReviewList reviews={shown} />
              </div>
            </div>
          )}
        </div>
      </section>


      <Contact />
    </>
  );
}
