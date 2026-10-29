import { Link } from 'react-router-dom';
import { Brand } from './Header.jsx';

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
            <li><Link to="/#faq">FAQ</Link></li>
            <li><Link to="/about/">About Me</Link></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <li><a href={`mailto:${p.email}`}>{p.email}</a></li>
            <li>{p.location}</li>
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
