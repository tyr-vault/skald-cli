import { createFileRoute } from '@tanstack/react-router';
import { DetailPage } from '@/components/site/detail-page';

export const Route = createFileRoute('/safety')({
  head: () => ({
    meta: [
      { title: 'Safety — Skald' },
      {
        name: 'description',
        content:
          'Local-first workspace, sensitive-path exclusion, and environment-only tokens for the Skald CLI.',
      },
      { property: 'og:title', content: 'Safety — Skald' },
      {
        property: 'og:description',
        content:
          'Local-first workspace, sensitive-path exclusion, and environment-only tokens for the Skald CLI.',
      },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
  }),
  component: Page,
});

function Page() {
  return <DetailPage kind="safety" />;
}
