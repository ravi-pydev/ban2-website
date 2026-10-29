import { EnquireButton } from '../components/popups.jsx';
import Icon from '../components/Icon.jsx';
import { SectionHead, Stats, Tags } from '../components/common.jsx';
import { PageError, PageLoader } from '../components/Status.jsx';
import { useApi, useDocumentTitle, useReveal, useScrollToHash } from '../hooks.js';

function AboutHero({ profile, stats }) {
  return (
    <section className="hero">
      <div className="hero-glow hero-glow-1" />
      <div className="hero-glow hero-glow-2" />
      <div className="container hero-inner">
        <div className="hero-text reveal">
          <span className="badge"><span className="dot" />Currently at Welcomhotel by ITC Hotels</span>
          <h1>{profile.name}</h1>
          <p className="hero-title">{profile.title} <em>· Hospitality, Sales &amp; Events</em></p>
          <p className="hero-summary">{profile.summary}</p>
          <div className="hero-actions">
            <EnquireButton>Plan an event with me</EnquireButton>
            <a href="#experience" className="btn btn-ghost">View experience</a>
          </div>
        </div>
        <div className="hero-photo reveal">
          <div className="photo-ring">
            <img src={profile.image} alt={`Portrait of ${profile.name}`} width="320" height="320" />
          </div>
          <div className="photo-chip"><Icon name="award" />Associate of the Quarter</div>
        </div>
      </div>
      <Stats stats={stats} />
    </section>
  );
}

function Experience({ jobs }) {
  return (
    <section id="experience" className="section">
      <div className="container">
        <SectionHead kicker="Career" title="Work Experience" />
        <ol className="timeline">
          {jobs.map((job, i) => (
            <li key={job.period} className="timeline-item reveal">
              <div className="timeline-meta">
                <span className="period">{job.period}</span>
                <span className="place">{job.location}</span>
              </div>
              <div className={`card job-card${i === 0 ? ' is-current' : ''}`}>
                {i === 0 && <span className="current-tag">Current role</span>}
                <h3>{job.role}</h3>
                <p className="company">{job.company}</p>
                <ul className="points">
                  {job.points.map((point) => <li key={point}>{point}</li>)}
                </ul>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

function Highlights({ items }) {
  return (
    <section id="highlights" className="section section-dark">
      <div className="container">
        <SectionHead kicker="Recognition" title="Highlights" />
        <div className="highlight-grid">
          {items.map((h) => (
            <article key={h.title} className="highlight reveal">
              <div className="icon-box"><Icon name={h.icon} /></div>
              <h3>{h.title}</h3>
              <p>{h.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function Education({ items }) {
  return (
    <section id="education" className="section section-alt">
      <div className="container">
        <SectionHead kicker="Learning" title="Education" />
        <div className="grid">
          {items.map((e) => (
            <article key={e.degree} className="card edu-card reveal">
              <div className="edu-top">
                <div className="icon-box icon-box-sm"><Icon name="grad" /></div>
                <span className="period">{e.date}</span>
              </div>
              <h3>{e.degree}</h3>
              {e.school && <p className="company">{e.school}</p>}
              {e.note && <p className="note">{e.note}</p>}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function Skills({ skills, languages, interests }) {
  return (
    <section id="skills" className="section">
      <div className="container split">
        <div className="reveal">
          <p className="kicker">Strengths</p>
          <h2 className="section-title">Skills</h2>
          <Tags items={skills} solid />
        </div>
        <div className="reveal">
          <p className="kicker">Communication</p>
          <h2 className="section-title">Languages</h2>
          <ul className="languages">
            {languages.map((l) => (
              <li key={l.name}>
                <div className="lang-row"><strong>{l.name}</strong><span>{l.level}</span></div>
                <div className="meter"><span style={{ width: `${l.percent}%` }} /></div>
              </li>
            ))}
          </ul>
        </div>
        <div className="reveal">
          <p className="kicker">Beyond work</p>
          <h2 className="section-title">Interests</h2>
          <Tags items={interests} />
        </div>
      </div>
    </section>
  );
}

function ContactCard({ icon, label, value, href }) {
  const inner = <><div className="icon-box"><Icon name={icon} /></div><span>{label}</span>{value}</>;
  return <li>{href ? <a href={href} className="contact-card">{inner}</a> : <div className="contact-card">{inner}</div>}</li>;
}

function AboutContact({ profile }) {
  return (
    <section className="section contact">
      <div className="hero-glow hero-glow-2" />
      <div className="container contact-inner reveal">
        <p className="kicker">Contact</p>
        <h2>Let's work together</h2>
        <p className="contact-lead">Corporate, MICE, travel trade or event enquiries are welcome.</p>
        <ul className="contact-cards">
          <ContactCard icon="mail" label="Email" value={profile.email} href={`mailto:${profile.email}`} />
          <ContactCard icon="pin" label="Location" value={profile.location} />
          {profile.dob && <ContactCard icon="cake" label="Date of birth" value={profile.dob} />}
        </ul>
        <EnquireButton className="btn btn-primary btn-lg">Send an enquiry</EnquireButton>
      </div>
    </section>
  );
}

export default function About({ site }) {
  const { data, error } = useApi('about/');
  useDocumentTitle(`About ${site.profile.name} | ${site.site_name}`);
  useReveal(!!data);
  useScrollToHash(!!data);

  if (error) return <PageError />;
  if (!data) return <PageLoader />;

  return (
    <>
      <AboutHero profile={site.profile} stats={data.stats} />
      <Experience jobs={data.experience} />
      <Highlights items={data.highlights} />
      <Education items={data.education} />
      <Skills skills={data.skills} languages={data.languages} interests={data.interests} />
      <AboutContact profile={site.profile} />
    </>
  );
}
