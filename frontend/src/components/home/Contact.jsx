import { EnquireButton } from '../popups.jsx';

/** "Let's plan your next event" call-to-action. Contact details live in the footer. */
export default function Contact() {
  return (
    <section id="contact" className="section contact contact-split">
      <div className="hero-glow hero-glow-1" />
      <div className="container contact-grid">
        <div className="reveal">
          <p className="kicker">Enquire</p>
          <h2>Let's plan your next event</h2>
          <p className="contact-lead">Tell me a little about your event and I will get back to you within one working day.</p>
        </div>
        <div className="contact-cta reveal">
          <h3>Have an event in mind?</h3>
          <p>Share your date, guest count and location — it takes about a minute. Your enquiry is emailed to me and WhatsApp opens with your message ready.</p>
          <EnquireButton className="btn btn-primary btn-lg">Send an enquiry</EnquireButton>
        </div>
      </div>
    </section>
  );
}
