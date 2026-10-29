import { Children, useCallback, useEffect, useRef, useState } from 'react';

const reducedMotion = () => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

/**
 * Horizontal carousel. Shows as many slides as fit (3 / 2 / 1 by screen width),
 * with arrows, dots, swipe/scroll and autoplay that pauses on hover or focus.
 */
export default function Carousel({ label, interval = 6000, children }) {
  const trackRef = useRef(null);
  const slides = Children.toArray(children);
  const [index, setIndex] = useState(0);
  const [maxIndex, setMaxIndex] = useState(0);
  const [paused, setPaused] = useState(false);

  // Width of one slide plus the gap between slides.
  const step = useCallback(() => {
    const track = trackRef.current;
    const first = track?.children[0];
    if (!first) return 1;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return first.getBoundingClientRect().width + gap;
  }, []);

  const measure = useCallback(() => {
    const track = trackRef.current;
    if (!track) return;
    const perView = Math.max(1, Math.round((track.clientWidth + 1) / step()));
    setMaxIndex(Math.max(0, slides.length - perView));
    setIndex(Math.round(track.scrollLeft / step()));
  }, [slides.length, step]);

  useEffect(() => {
    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [measure]);

  const goTo = useCallback((i) => {
    const target = Math.max(0, Math.min(i, maxIndex));
    trackRef.current?.scrollTo({ left: target * step(), behavior: reducedMotion() ? 'auto' : 'smooth' });
    setIndex(target);
  }, [maxIndex, step]);

  // Autoplay: next slide every `interval`, back to the start after the last one.
  useEffect(() => {
    if (paused || maxIndex === 0 || reducedMotion()) return undefined;
    const timer = setInterval(() => {
      if (document.hidden) return;
      goTo(index >= maxIndex ? 0 : index + 1);
    }, interval);
    return () => clearInterval(timer);
  }, [paused, index, maxIndex, interval, goTo]);

  const hasControls = maxIndex > 0;

  return (
    <div
      className="carousel"
      role="region"
      aria-roledescription="carousel"
      aria-label={label}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={(e) => { if (!e.currentTarget.contains(e.relatedTarget)) setPaused(false); }}
    >
      <div className="carousel-track" ref={trackRef} onScroll={measure}>
        {slides.map((slide, i) => (
          <div key={i} className="carousel-slide" role="group" aria-roledescription="slide"
            aria-label={`${i + 1} of ${slides.length}`}>
            {slide}
          </div>
        ))}
      </div>
      {hasControls && (
        <div className="carousel-controls">
          <button type="button" className="carousel-arrow" aria-label="Previous" onClick={() => goTo(index - 1)}
            disabled={index === 0}>‹</button>
          <div className="carousel-dots">
            {Array.from({ length: maxIndex + 1 }, (_, i) => (
              <button key={i} type="button" className={i === index ? 'active' : ''}
                aria-label={`Go to slide ${i + 1}`} aria-current={i === index}
                onClick={() => goTo(i)} />
            ))}
          </div>
          <button type="button" className="carousel-arrow" aria-label="Next" onClick={() => goTo(index + 1)}
            disabled={index === maxIndex}>›</button>
        </div>
      )}
    </div>
  );
}
