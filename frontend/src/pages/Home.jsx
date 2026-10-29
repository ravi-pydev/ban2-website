import Contact from '../components/home/Contact.jsx';
import {
  Clients, CtaBand, Faq, Hero, Intro, Process, Ribbon, Services, Sessions, WhyMe,
} from '../components/home/sections.jsx';
import { PageError, PageLoader } from '../components/Status.jsx';
import { useApi, useDocumentTitle, useReveal, useScrollToHash } from '../hooks.js';

export default function Home({ site }) {
  const { data, error } = useApi('home/');
  useDocumentTitle(`${site.site_name} | Corporate Events, MICE & Venue Sourcing`);
  useReveal(!!data);
  useScrollToHash(!!data);

  if (error) return <PageError />;
  if (!data) return <PageLoader />;

  return (
    <>
      <Hero hero={data.hero} profile={site.profile} stats={data.stats} />
      <Ribbon clientTypes={data.client_types} />
      <Intro intro={data.intro} />
      <Services services={data.services} />
      <Sessions sessions={data.sessions} />
      <WhyMe points={data.why_me} />
      <Process steps={data.process} />
      <Clients testimonials={data.testimonials} clientTypes={data.client_types} />
      <CtaBand cta={data.cta} fallbackImage={data.hero.image} />
      <Faq faqs={data.faqs} />
      <Contact site={site} services={data.services} />
    </>
  );
}
