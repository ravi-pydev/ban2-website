import { useEffect, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';

const LINKS = [
  { to: '/#services', label: 'Services' },
  { to: '/#sessions', label: 'Events' },
  { to: '/#clients', label: 'Clients' },
  { to: '/#process', label: 'Process' },
];

export function Brand({ site }) {
  return (
    <Link to="/" className="brand"><span className="brand-mark">B2</span>{site.site_name}</Link>
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
          <li><NavLink to="/about/" onClick={close}>About Me</NavLink></li>
          <li><Link to="/#contact" className="nav-cta" onClick={close}>Enquire</Link></li>
        </ul>
      </nav>
    </header>
  );
}
