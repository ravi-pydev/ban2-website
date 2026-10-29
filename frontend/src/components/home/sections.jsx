import { Link } from 'react-router-dom';
import Icon from '../Icon.jsx';
import { SectionHead, Stats, Tags } from '../common.jsx';

export function Hero({ hero, profile, stats }) {
  return (
    <section className="biz-hero" style={{ '--hero-img': `url('${hero.image}')` }}>
      <div className="container biz-hero-inner">
        <div className="reveal">
          <span className="badge"><span className="dot" />Taking enquiries for {new Date().getFullYear()}</span>
          <h1>{hero.heading}</h1>
          <p className="biz-hero-text">{hero.text}</p>
          <div className="hero-actions">
            <a href="#contact" className="btn btn-primary">{hero.button || 'Plan my event'}</a>
            <a href="#services" className="btn btn-ghost">Explore services</a>
          </div>
        </div>
        <Link to="/about/" className="profile-card reveal">
          <img src={profile.image} alt={`Portrait of ${profile.name}`} width="72" height="72" />
          <div>
            <strong>{profile.name}</strong>
            <span>{profile.title}</span>
            <em>About me <Icon name="arrow" /></em>
          </div>
        </Link>
      </div>
      <Stats stats={stats} />
    </section>
  );
}

export function Ribbon({ clientTypes }) {
  // The list is rendered twice so the scrolling loop is seamless.
  const items = [...clientTypes, ...clientTypes];
  return (
    <div className="ribbon" aria-label="Who I work with">
      <div className="ribbon-track">
        {items.map((name, i) => <span key={i} aria-hidden={i >= clientTypes.length}>{name}</span>)}
      </div>
    </div>
  );
}

export function Intro({ intro }) {
  if (!intro) return null;
  return (
    <section className="section">
      <div className="container intro">
        <div className="intro-media reveal">
          <img src={intro.image} alt="Conference hall set up for an event" loading="lazy" />
          <div className="intro-badge"><strong>50+</strong><span>MNC events<br />delivered</span></div>
        </div>
        <div className="reveal">
          {intro.kicker && <p className="kicker">{intro.kicker}</p>}
          <h2 className="section-title">{intro.heading}</h2>
          {intro.paragraphs.map((text) => <p key={text} className="lead-text">{text}</p>)}
          {intro.items.length > 0 && (
            <ul className="checklist">
              {intro.items.map((item) => <li key={item}><Icon name="check" />{item}</li>)}
            </ul>
          )}
          {intro.button && (
            <Link to="/about/" className="text-link">{intro.button} <Icon name="arrow" /></Link>
          )}
        </div>
      </div>
    </section>
  );
}

export function Services({ services }) {
  return (
    <section id="services" className="section section-alt">
      <div className="container">
        <SectionHead center kicker="What I offer" title="Services"
          sub="Everything you need to plan, book and deliver a successful event — handled by one experienced professional." />
        <div className="service-grid">
          {services.map((s) => (
            <article key={s.title} className="service-card reveal">
              <div className="service-img">
                <div className="service-frame"><img src={s.image} alt="" loading="lazy" /></div>
                <div className="service-icon"><Icon name={s.icon} /></div>
              </div>
              <div className="service-body">
                <h3>{s.title}</h3>
                <p>{s.text}</p>
                <a href="#contact" className="text-link">Enquire <Icon name="arrow" /></a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Sessions({ sessions }) {
  return (
    <section id="sessions" className="section">
      <div className="container">
        <SectionHead center kicker="Portfolio" title="Successfully Organised Sessions"
          sub="Conferences, dinners, workshops and celebrations — a look at the kinds of events I have planned and delivered." />
        <div className="gallery">
          {sessions.map((s) => (
            <figure key={s.title} className="gallery-item reveal">
              <img src={s.image} alt={s.title} loading="lazy" />
              <figcaption><h3>{s.title}</h3><p>{s.text}</p></figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}

export function WhyMe({ points }) {
  return (
    <section className="section section-dark">
      <div className="container">
        <SectionHead center kicker="Why work with me" title="Experience you can rely on" />
        <div className="highlight-grid">
          {points.map((p) => (
            <article key={p.title} className="highlight reveal">
              <div className="icon-box"><Icon name={p.icon} /></div>
              <h3>{p.title}</h3>
              <p>{p.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Process({ steps }) {
  return (
    <section id="process" className="section">
      <div className="container">
        <SectionHead center kicker="How it works" title="From first call to final bill" />
        <ol className="process">
          {steps.map((step, i) => (
            <li key={step.title} className="process-step reveal">
              <span className="step-num">{String(i + 1).padStart(2, '0')}</span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

export function Clients({ testimonials, clientTypes }) {
  return (
    <section id="clients" className="section section-alt">
      <div className="container">
        <SectionHead center kicker="Testimonials" title="Happy Clients" sub="What clients say about working with me." />
        <div className="testimonial-grid">
          {testimonials.map((t, i) => (
            <figure key={i} className="testimonial reveal">
              {t.sample && <span className="sample-tag">Sample</span>}
              <Icon name="quote" className="quote-mark" />
              <div className="stars" aria-label={`${t.rating} out of 5`}>{'★'.repeat(t.rating)}</div>
              <blockquote>{t.quote}</blockquote>
              <figcaption>
                <span className="avatar"><Icon name="user" /></span>
                <span><strong>{t.name}</strong><small>{t.role}</small></span>
              </figcaption>
            </figure>
          ))}
        </div>
        <div className="client-types reveal">
          <p>Trusted by clients across</p>
          <Tags items={clientTypes} />
        </div>
      </div>
    </section>
  );
}

export function CtaBand({ cta, fallbackImage }) {
  if (!cta) return null;
  return (
    <section className="cta-band" style={{ '--cta-img': `url('${cta.image || fallbackImage}')` }}>
      <div className="container cta-inner reveal">
        <div>
          <h2>{cta.heading}</h2>
          {cta.text && <p>{cta.text}</p>}
        </div>
        <a href="#contact" className="btn btn-primary btn-lg">{cta.button || 'Get in touch'}</a>
      </div>
    </section>
  );
}

export function Faq({ faqs }) {
  return (
    <section id="faq" className="section">
      <div className="container faq-wrap">
        <div className="reveal">
          <p className="kicker">FAQ</p>
          <h2 className="section-title">Questions clients often ask</h2>
          <p className="lead-text">
            Can't find what you are looking for? <a href="#contact" className="text-link inline">Send me a message</a>.
          </p>
        </div>
        <div className="faq reveal">
          {faqs.map((f, i) => (
            <details key={f.q} open={i === 0}>
              <summary>{f.q}</summary>
              <p>{f.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
