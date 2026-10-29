import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import Footer from './components/Footer.jsx';
import Header from './components/Header.jsx';
import { IconSprite } from './components/Icon.jsx';
import { PageError, PageLoader } from './components/Status.jsx';
import { useApi } from './hooks.js';
import About from './pages/About.jsx';
import Home from './pages/Home.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <IconSprite />
      <Layout />
    </BrowserRouter>
  );
}

function Layout() {
  const { data: site, error } = useApi('site/');

  if (error) return <main id="top"><PageError /></main>;
  if (!site) return <main id="top"><PageLoader /></main>;

  return (
    <>
      <Header site={site} />
      <main id="top">
        <Routes>
          <Route path="/" element={<Home site={site} />} />
          <Route path="/about" element={<About site={site} />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer site={site} />
    </>
  );
}

function NotFound() {
  return (
    <section className="section page-error">
      <div className="container">
        <h1 className="section-title">Page not found</h1>
        <p className="lead-text">The page you are looking for doesn't exist. <Link to="/" className="text-link inline">Go to the home page</Link>.</p>
      </div>
    </section>
  );
}
