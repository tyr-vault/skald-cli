import { createFileRoute } from '@tanstack/react-router';
import { DetailPage } from '@/components/site/detail-page';

export const Route = createFileRoute('/commands')({
  head: () => ({
    meta: [
      { title: 'CLI commands — Skald' },
      {
        name: 'description',
        content:
          'Accurate init, scan, analyze, features, content, and report commands for the Skald CLI.',
      },
      { property: 'og:title', content: 'CLI commands — Skald' },
      {
        property: 'og:description',
        content:
          'Accurate init, scan, analyze, features, content, and report commands for the Skald CLI.',
      },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
  }),
  component: Page,
});

function Page() {
  return <DetailPage kind="commands" />;
}
