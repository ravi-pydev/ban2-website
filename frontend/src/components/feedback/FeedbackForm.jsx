import { useState } from 'react';
import { postJson } from '../../api.js';

const LABELS = { 1: 'Poor', 2: 'Fair', 3: 'Good', 4: 'Very good', 5: 'Excellent' };

function firstError(body) {
  if (body.detail) return body.detail;
  if (body.errors) {
    const field = Object.keys(body.errors)[0];
    return `${field}: ${[].concat(body.errors[field])[0]}`;
  }
  return 'Please check the form and try again.';
}

function StarInput({ value, onChange }) {
  const [hover, setHover] = useState(0);
  const shown = hover || value;
  return (
    <fieldset className="star-input" onMouseLeave={() => setHover(0)}>
      <legend>Your rating *</legend>
      <div className="star-row">
        {[1, 2, 3, 4, 5].map((n) => (
          <label key={n} className={n <= shown ? 'on' : ''} onMouseEnter={() => setHover(n)}>
            <input type="radio" name="rating" value={n} required checked={value === n}
              onChange={() => onChange(n)} />
            <span aria-hidden="true">★</span>
            <span className="sr-only">{n} star{n > 1 ? 's' : ''} – {LABELS[n]}</span>
          </label>
        ))}
        <span className="star-label">{shown ? LABELS[shown] : 'Tap to rate'}</span>
      </div>
    </fieldset>
  );
}

/** Feedback form for existing clients. onSuccess() is called after a successful send. */
export default function FeedbackForm({ events, onSuccess }) {
  const [rating, setRating] = useState(0);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const data = Object.fromEntries(new FormData(form));
    data.rating = Number(data.rating);
    data.consent = form.elements.consent.checked;

    setSending(true);
    setError(null);
    try {
      const result = await postJson('feedback/', data);
      if (result.ok) onSuccess();
      else setError(firstError(result.body));
    } catch {
      setError('Network error — your feedback was not sent. Please try again.');
    } finally {
      setSending(false);
    }
  }

  return (
    <form className="enquiry feedback-form" noValidate onSubmit={handleSubmit}>
      <div className="hp" aria-hidden="true">
        <label>Website<input name="website" tabIndex={-1} autoComplete="off" /></label>
      </div>
      <StarInput value={rating} onChange={setRating} />
      <div className="field-row">
        <label>Your name *<input name="name" required maxLength={100} autoComplete="name" /></label>
        <label>Email *<input name="email" type="email" required autoComplete="email" /></label>
      </div>
      <div className="field-row">
        <label>Company<input name="company" maxLength={150} autoComplete="organization" /></label>
        <label>Your role<input name="role" maxLength={100} placeholder="e.g. HR Manager" autoComplete="organization-title" /></label>
      </div>
      <label>Which event?
        <select name="event_session" defaultValue="">
          <option value="">Select an event (optional)</option>
          {events.map((e) => <option key={e.id} value={e.id}>{e.title}</option>)}
        </select>
      </label>
      <label>Your feedback *
        <textarea name="feedback" rows={4} required minLength={20} maxLength={1000}
          placeholder="What went well? What made the difference for you?" />
      </label>
      <label className="checkbox">
        <input type="checkbox" name="consent" />
        <span>You may publish my review with my name, role and company on this website.</span>
      </label>
      <button type="submit" className="btn btn-primary" disabled={sending}>
        {sending ? 'Sending…' : 'Submit feedback'}
      </button>
      {error && <output className="form-status error" aria-live="polite">{error}</output>}
      <p className="form-note">Your email is never shown on the site. Reviews are published only with your permission.</p>
    </form>
  );
}
