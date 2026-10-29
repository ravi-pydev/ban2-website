import { Link } from 'react-router-dom';
import { Brand } from './Header.jsx';
import Icon from './Icon.jsx';
import { FeedbackButton } from './popups.jsx';

export default function Footer({ site }) {
  const p = site.profile;
  return (
    <footer className="site-footer">
      <div className="container footer-grid">
        <div>
          <Brand site={site} />
          <p className="footer-text">
            {p.tagline} by {p.name} — corporate events, MICE, venue sourcing and celebrations
            across {p.service_area}.
          </p>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><Link to="/#services">Services</Link></li>
            <li><Link to="/#sessions">Events</Link></li>
            <li><Link to="/reviews/">Client reviews</Link></li>
            <li><FeedbackButton className="footer-link">Give feedback</FeedbackButton></li>
            <li><Link to="/#faq">FAQ</Link></li>
            <li><Link to="/about/">About Me</Link></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul className="footer-contact">
            <li><Icon name="mail" /><a href={`mailto:${p.email}`}>{p.email}</a></li>
            <li><Icon name="pin" />{p.service_area}</li>
            <li><Icon name="clock" />Reply within 1 working day</li>
          </ul>
        </div>
      </div>
      <div className="container footer-bottom">
        <span>&copy; {new Date().getFullYear()} {site.site_name}</span>
        <a href="#top" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
          Back to top ↑
        </a>
      </div>
    </footer>
  );
}
