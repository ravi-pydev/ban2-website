import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { getJson } from './api.js';

/** Fetch an API path. Returns { data, error }. */
export function useApi(path) {
  const [state, setState] = useState({ data: null, error: null });

  useEffect(() => {
    let cancelled = false;
    setState({ data: null, error: null });
    getJson(path)
      .then((data) => !cancelled && setState({ data, error: null }))
      .catch((error) => {
        console.error(error);
        if (!cancelled) setState({ data: null, error });
      });
    return () => { cancelled = true; };
  }, [path]);

  return state;
}

export function useDocumentTitle(title) {
  useEffect(() => {
    if (title) document.title = title;
  }, [title]);
}

/** Fade elements with class "reveal" in as they scroll into view, once `ready` is true. */
export function useReveal(ready) {
  useEffect(() => {
    if (!ready || !('IntersectionObserver' in window)) return undefined;
    document.documentElement.classList.add('js-reveal');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      // Anything already on screen is shown straight away; the rest fades in on scroll.
      if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('visible');
      else observer.observe(el);
    });
    return () => observer.disconnect();
  }, [ready]);
}

/** Scroll to the element named in the URL hash (e.g. /#services) once the page has rendered. */
export function useScrollToHash(ready) {
  const location = useLocation();
  useEffect(() => {
    if (!ready) return;
    if (!location.hash) {
      window.scrollTo(0, 0);
      return;
    }
    const target = document.getElementById(location.hash.slice(1));
    if (target) target.scrollIntoView();
  }, [ready, location.pathname, location.hash, location.key]);
}
