import { useEffect, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { EnquireButton } from './popups.jsx';

const LINKS = [
  { to: '/#services', label: 'Services' },
  { to: '/#sessions', label: 'Events' },
  { to: '/#process', label: 'Process' },
];

export function Brand({ site }) {
  // "Event & Experience by Ban2" -> main name + smaller "by Ban2"
  const name = site.site_name;
  const at = name.lastIndexOf(' by ');
  const main = at > 0 ? name.slice(0, at) : name;
  const by = at > 0 ? name.slice(at + 1) : '';
  return (
    <Link to="/" className="brand" aria-label={name}>
      <span className="brand-mark">B2</span>
      <span className="brand-name">{main}{by && <small className="brand-by">{by}</small>}</span>
    </Link>
  );
}

export default function Header({ site }) {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const close = () => setOpen(false);

  return (
    <header className={`site-header${scrolled ? ' scrolled' : ''}`}>
      <nav className="nav container" aria-label="Main">
        <Brand site={site} />
        <button
          className={`nav-toggle${open ? ' open' : ''}`}
          aria-label={open ? 'Close menu' : 'Open menu'}
          aria-expanded={open}
          aria-controls="nav-links"
          onClick={() => setOpen(!open)}
        >
          <span /><span /><span />
        </button>
        <ul className={`nav-links${open ? ' open' : ''}`} id="nav-links">
          {LINKS.map((link) => (
            <li key={link.to}><Link to={link.to} onClick={close}>{link.label}</Link></li>
          ))}
          <li><NavLink to="/reviews/" onClick={close}>Reviews</NavLink></li>
          <li><NavLink to="/about/" onClick={close}>About Me</NavLink></li>
          <li><EnquireButton className="nav-cta" onClick={close}>Enquire</EnquireButton></li>
        </ul>
      </nav>
    </header>
  );
}
