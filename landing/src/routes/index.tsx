import { createFileRoute, Link } from '@tanstack/react-router';
import { ArrowUpRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useLanguage } from '@/components/site/language';
import { Terminal } from '@/components/site/terminal';
import { CommandList } from '@/components/site/command-list';
import { CommandTable } from '@/components/site/command-table';
import { toolReadmeUrl } from '@/lib/site-config';

export const Route = createFileRoute('/')({
  head: () => ({
    meta: [
      { title: 'Skald — Local-first developer knowledge pipeline' },
      {
        name: 'description',
        content:
          'Skald turns Git engineering activity into structured feature metadata and grounded content drafts. Local-first CLI for Python 3.10+.',
      },
      { property: 'og:title', content: 'Skald — Local-first developer knowledge pipeline' },
      {
        property: 'og:description',
        content:
          'A developer CLI for evidence-backed feature catalogs and drafts from Git history. Available in English and Português do Brasil.',
      },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
  }),
  component: Index,
});

function Index() {
  const { t } = useLanguage();
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="status-dot" />
            CLI · Python 3.10+ · pip
          </div>
          <h1>
            {t.headline.map((line) => (
              <span key={line}>{line}</span>
            ))}
          </h1>
          <p className="hero-intro">{t.intro}</p>
          <div className="hero-buttons">
            <Button asChild variant="action">
              <Link to="/docs">
                <span className="font-mono">$</span>
                {t.start}
                <ArrowUpRight />
              </Link>
            </Button>
            <Button asChild variant="technical">
              <a href={toolReadmeUrl} target="_blank" rel="noopener noreferrer">
                {t.readme}
              </a>
            </Button>
          </div>
          <div className="trust-line">
            {t.trust.map((item, i) => (
              <span key={item}>
                {i > 0 && <i className="mr-3">/</i>}
                {item}
              </span>
            ))}
          </div>
        </div>
        <Terminal />
      </section>
      <section className="features">
        {t.features.map(([label, title, body]) => (
          <article className="feature-card" key={label}>
            <span className="eyebrow">{label}</span>
            <h3>{title}</h3>
            <p>{body}</p>
          </article>
        ))}
      </section>
      <section className="workflow">
        <div>
          <span className="eyebrow">{t.workflow}</span>
          <h2>
            {t.workflowTitle.map((line) => (
              <span key={line}>{line}</span>
            ))}
          </h2>
          <p>{t.workflowText}</p>
        </div>
        <CommandList />
      </section>
      <section className="reference">
        <div className="reference-copy">
          <span className="eyebrow">{t.reference}</span>
          <h2>
            {t.referenceTitle.map((line) => (
              <span key={line}>{line}</span>
            ))}
          </h2>
          <p>{t.referenceText}</p>
        </div>
        <CommandTable compact />
      </section>
    </>
  );
}
