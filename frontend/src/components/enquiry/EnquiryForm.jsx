import { useRef, useState } from 'react';
import { postJson } from '../../api.js';
import { whatsappUrl } from '../../whatsapp.js';

function firstError(body) {
  if (body.error) return body.error;
  if (body.detail) return body.detail;
  if (body.errors) {
    const field = Object.keys(body.errors)[0];
    return `${field}: ${[].concat(body.errors[field])[0]}`;
  }
  return 'Please check the form and try again.';
}

/**
 * The enquiry form. Sends to the API and opens WhatsApp with the same details.
 * onSuccess({ message, waUrl, waOpened }) is called after a successful send.
 */
export default function EnquiryForm({ site, eventTypes, defaultEventType, onSuccess }) {
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null); // { message, waUrl }
  const [showDetails, setShowDetails] = useState(false);
  const detailsRef = useRef(null);

  function toggleDetails() {
    const open = !showDetails;
    setShowDetails(open);
    // Focus the box once React has shown it.
    if (open) setTimeout(() => detailsRef.current?.focus(), 0);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const data = Object.fromEntries(new FormData(form));
    const waUrl = whatsappUrl(site.whatsapp_number, site.site_name, data);

    // Open WhatsApp straight away: browsers only allow new windows during the click.
    const waWindow = window.open(waUrl, '_blank');
    if (waWindow) waWindow.opener = null;

    setSending(true);
    setError(null);
    try {
      const result = await postJson('enquiries/', data);
      if (result.ok) {
        const message = result.body.email_sent === false
          ? 'Your enquiry has been received.'
          : 'Your enquiry has been emailed.';
        form.reset();
        setShowDetails(false);
        onSuccess({ message, waUrl, waOpened: !!waWindow });
      } else {
        setError({ message: firstError(result.body), waUrl });
      }
    } catch {
      setError({ message: 'Network error — the email was not sent.', waUrl });
    } finally {
      setSending(false);
    }
  }

  return (
    <form className="enquiry" noValidate onSubmit={handleSubmit}>
      <div className="hp" aria-hidden="true">
        <label>Website<input name="website" tabIndex={-1} autoComplete="off" /></label>
      </div>
      <div className="field-row">
        <label>Your name *<input name="name" required maxLength={100} autoComplete="name" /></label>
        <label>Company<input name="company" maxLength={120} autoComplete="organization" /></label>
      </div>
      <div className="field-row">
        <label>Email *<input name="email" type="email" required autoComplete="email" /></label>
        <label>Phone / WhatsApp<input name="phone" type="tel" maxLength={20} autoComplete="tel" /></label>
      </div>
      <div className="field-row">
        <label>Event type
          <select name="event_type" defaultValue={defaultEventType || eventTypes[0]}>
            {eventTypes.map((type) => <option key={type}>{type}</option>)}
          </select>
        </label>
        <label>Guests<input name="guests" type="number" min="1" inputMode="numeric" /></label>
      </div>
      <div className="field-row">
        <label>Preferred date<input name="date" type="date" /></label>
        <label>Event location
          <input name="event_location" maxLength={150} placeholder="City or venue, e.g. Gurugram" autoComplete="address-level2" />
        </label>
      </div>
      <div className="other-details">
        <button type="button" className="details-toggle" aria-expanded={showDetails}
          aria-controls="enquiry-details" onClick={toggleDetails}>
          <span aria-hidden="true">{showDetails ? '–' : '+'}</span>
          {showDetails ? 'Hide other details' : 'Other details'}
        </button>
        {/* Hidden rather than removed, so anything typed is kept and still sent. */}
        <textarea id="enquiry-details" name="message" ref={detailsRef} rows={4} maxLength={3000}
          aria-label="Other details" placeholder="Budget, theme, anything else I should know"
          hidden={!showDetails} />
      </div>
      <button type="submit" className="btn btn-primary" disabled={sending}>
        {sending ? 'Sending…' : 'Send enquiry'}
      </button>
      {error && (
        <output className="form-status error" aria-live="polite">
          {error.message}{' '}
          <a href={error.waUrl} target="_blank" rel="noopener noreferrer">Open WhatsApp</a> to reach me instead.
        </output>
      )}
      <p className="form-note">Your enquiry is emailed to me and WhatsApp opens with your message ready — just tap Send.</p>
    </form>
  );
}
