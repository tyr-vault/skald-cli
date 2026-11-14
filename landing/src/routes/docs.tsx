import { createFileRoute } from '@tanstack/react-router';
import { DetailPage } from '@/components/site/detail-page';

export const Route = createFileRoute('/docs')({
  head: () => ({
    meta: [
      { title: 'Setup and documentation — Skald' },
      {
        name: 'description',
        content:
          'Install and configure the local Skald CLI with Python 3.10+, pip, Git, and optional GitHub credentials.',
      },
      { property: 'og:title', content: 'Setup and documentation — Skald' },
      {
        property: 'og:description',
        content:
          'Install and configure the local Skald CLI with Python 3.10+, pip, Git, and optional GitHub credentials.',
      },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
  }),
  component: Page,
});

function Page() {
  return <DetailPage kind="docs" />;
}
