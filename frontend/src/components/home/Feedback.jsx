import Icon from '../Icon.jsx';
import { FeedbackButton } from '../popups.jsx';

/** "Worked with me?" call-to-action. The form itself opens in a popup. */
export default function Feedback() {
  return (
    <section id="feedback" className="section section-alt">
      <div className="container feedback-grid">
        <div className="reveal">
          <p className="kicker">Existing clients</p>
          <h2 className="section-title">Worked with me? Share your feedback</h2>
          <p className="lead-text">
            Your review helps other hosts and companies plan with confidence, and helps me keep improving.
          </p>
        </div>
        <div className="feedback-cta reveal">
          <ul className="checklist checklist-single">
            <li><Icon name="check" />Takes less than two minutes</li>
            <li><Icon name="check" />Your email is never shown on the site</li>
            <li><Icon name="check" />Reviews are published only with your permission</li>
          </ul>
          <FeedbackButton className="btn btn-primary btn-lg">Write a review</FeedbackButton>
        </div>
      </div>
    </section>
  );
}
