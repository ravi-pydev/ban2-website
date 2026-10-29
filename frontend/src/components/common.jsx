export function SectionHead({ kicker, title, sub, center = false }) {
  return (
    <div className={`section-head${center ? ' center' : ''} reveal`}>
      <p className="kicker">{kicker}</p>
      <h2 className="section-title">{title}</h2>
      {sub && <p className="section-sub">{sub}</p>}
    </div>
  );
}

export function Stats({ stats }) {
  return (
    <div className="container">
      <ul className="stats reveal">
        {stats.map((s) => (
          <li key={s.label}><strong>{s.value}</strong><span>{s.label}</span></li>
        ))}
      </ul>
    </div>
  );
}

export function Tags({ items, solid = false }) {
  return (
    <ul className="tags">
      {items.map((item) => (
        <li key={item} className={`tag${solid ? ' tag-solid' : ''}`}>{item}</li>
      ))}
    </ul>
  );
}
