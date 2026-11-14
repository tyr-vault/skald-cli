import { createFileRoute } from '@tanstack/react-router';
import { DetailPage } from '@/components/site/detail-page';

export const Route = createFileRoute('/how-it-works')({
  head: () => ({
    meta: [
      { title: 'How it works — Skald' },
      {
        name: 'description',
        content:
          'Scan Git repositories, discover features, and generate grounded content drafts with the Skald CLI.',
      },
      { property: 'og:title', content: 'How it works — Skald' },
      {
        property: 'og:description',
        content:
          'Scan Git repositories, discover features, and generate grounded content drafts with the Skald CLI.',
      },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
  }),
  component: Page,
});

function Page() {
  return <DetailPage kind="workflow" />;
}
