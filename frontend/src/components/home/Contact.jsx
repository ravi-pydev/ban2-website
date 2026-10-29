import { useState } from 'react';
import { postJson } from '../../api.js';
import { whatsappUrl } from '../../whatsapp.js';
import Icon from '../Icon.jsx';

function firstError(body) {
  if (body.error) return body.error;
  if (body.detail) return body.detail;
  if (body.errors) {
    const field = Object.keys(body.errors)[0];
    return `${field}: ${[].concat(body.errors[field])[0]}`;
  }
  return 'Please check the form and try again.';
}

function EnquiryForm({ site, services }) {
  const [sending, setSending] = useState(false);
  // { kind: 'success' | 'error', message, waUrl, waOpened }
  const [status, setStatus] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const data = Object.fromEntries(new FormData(form));
    const waUrl = whatsappUrl(site.whatsapp_number, data);

    // Open WhatsApp straight away: browsers only allow new windows during the click.
    const waWindow = window.open(waUrl, '_blank');
    if (waWindow) waWindow.opener = null;

    setSending(true);
    setStatus(null);
    try {
      const result = await postJson('enquiries/', data);
      if (result.ok) {
        setStatus({ kind: 'success', message: 'Thank you! Your enquiry has been emailed.', waUrl, waOpened: !!waWindow });
        form.reset();
      } else {
        setStatus({ kind: 'error', message: firstError(result.body), waUrl });
      }
    } catch {
      setStatus({ kind: 'error', message: 'Network error — the email was not sent.', waUrl });
    } finally {
      setSending(false);
    }
  }

  return (
    <form className="enquiry reveal" noValidate onSubmit={handleSubmit}>
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
          <select name="event_type">
            {services.map((s) => <option key={s.title}>{s.title}</option>)}
            <option>Other</option>
          </select>
        </label>
        <label>Guests<input name="guests" type="number" min="1" inputMode="numeric" /></label>
      </div>
      <label>Preferred date<input name="date" type="date" /></label>
      <label>Details
        <textarea name="message" rows={4} maxLength={3000} placeholder="City, budget, anything else I should know" />
      </label>
      <button type="submit" className="btn btn-primary" disabled={sending}>
        {sending ? 'Sending…' : 'Send enquiry'}
      </button>
      {status && (
        <output className={`form-status ${status.kind}`} aria-live="polite">
          {status.message}{' '}
          {status.kind === 'success' && status.waOpened
            ? 'Tap Send in WhatsApp to share it there too.'
            : <><a href={status.waUrl} target="_blank" rel="noopener noreferrer">Open WhatsApp</a>{status.kind === 'success' ? ' to send it there too.' : ' to reach me instead.'}</>}
        </output>
      )}
      <p className="form-note">Your enquiry is emailed to me and WhatsApp opens with your message ready — just tap Send.</p>
    </form>
  );
}

export default function Contact({ site, services }) {
  const p = site.profile;
  return (
    <section id="contact" className="section contact contact-split">
      <div className="hero-glow hero-glow-1" />
      <div className="container contact-grid">
        <div className="reveal">
          <p className="kicker">Enquire</p>
          <h2>Let's plan your next event</h2>
          <p className="contact-lead">Tell me a little about your event and I will get back to you within one working day.</p>
          <ul className="contact-points">
            <li><span className="icon-box icon-box-sm"><Icon name="mail" /></span><a href={`mailto:${p.email}`}>{p.email}</a></li>
            <li><span className="icon-box icon-box-sm"><Icon name="pin" /></span>{p.service_area}</li>
            <li><span className="icon-box icon-box-sm"><Icon name="clock" /></span>Reply within 1 working day</li>
          </ul>
        </div>
        <EnquiryForm site={site} services={services} />
      </div>
    </section>
  );
}
