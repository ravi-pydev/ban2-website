export function PageLoader() {
  return <div className="page-loader" role="status"><span />Loading…</div>;
}

export function PageError() {
  return (
    <section className="section page-error">
      <div className="container">
        <h1 className="section-title">Something went wrong</h1>
        <p className="lead-text">The page content could not be loaded. Please refresh, or try again in a moment.</p>
      </div>
    </section>
  );
}
