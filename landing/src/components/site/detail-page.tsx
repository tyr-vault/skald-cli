import { Link } from '@tanstack/react-router';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { commands } from '@/lib/site-content';
import { toolReadmeUrl } from '@/lib/site-config';
import { useLanguage } from './language';
import { CommandTable } from './command-table';
import { ConfigTable } from './config-table';
import { CopyCommand } from './copy-command';

export type DetailKind = 'workflow' | 'commands' | 'safety' | 'docs';

const content = {
  en: {
    workflow: [
      'From commits to drafts.',
      'Six steps from a local workspace to grounded Markdown — always review drafts before you publish.',
    ],
    commands: [
      'Your repo. Six commands.',
      'Entry point: skald plus a command and options. Run skald init so the workspace and SQLite catalog resolve correctly.',
    ],
    safety: [
      'Local-first by design.',
      'Scans stay on your machine. Tokens come from the environment. Drafts are files you choose to share.',
    ],
    docs: [
      'Set up Skald.',
      'Python 3.10+, Git, and pip. Optional GITHUB_TOKEN for public repo listing — credentials stay on your machine.',
    ],
  },
  pt: {
    workflow: [
      'De commits a rascunhos.',
      'Seis passos do workspace local ao Markdown fundamentado — sempre revise rascunhos antes de publicar.',
    ],
    commands: [
      'Seu repo. Seis comandos.',
      'Entrada: skald com um comando e opções. Rode skald init para o workspace e o SQLite resolverem corretamente.',
    ],
    safety: [
      'Local-first por desenho.',
      'Scans ficam na sua máquina. Tokens vêm do ambiente. Rascunhos são arquivos que você decide compartilhar.',
    ],
    docs: [
      'Configure o Skald.',
      'Python 3.10+, Git e pip. GITHUB_TOKEN opcional para listar repos públicos — credenciais ficam na sua máquina.',
    ],
  },
};

export function DetailPage({ kind }: { kind: DetailKind }) {
  const { language, t } = useLanguage();
  const pt = language === 'pt';
  const [title, lead] = content[language][kind];

  return (
    <div className="detail-page">
      <Button asChild variant="link" className="px-0">
        <Link to="/">
          <ArrowLeft />
          {t.back}
        </Link>
      </Button>
      <h1>{title}</h1>
      <p className="detail-lead">{lead}</p>

      {kind === 'workflow' && (
        <>
          <div className="steps">
            {[
              [
                pt ? '1 · Inicialize o workspace' : '1 · Initialize the workspace',
                pt ? 'Config, SQLite e diretórios locais:' : 'Config, SQLite, and local directories:',
                'skald init',
              ],
              [
                pt ? '2 · Escaneie o repositório' : '2 · Scan the repository',
                pt ? 'Metadados da árvore e do histórico:' : 'Tree metadata and commit history:',
                null,
              ],
              [
                pt ? '3 · Analise' : '3 · Analyze',
                pt
                  ? 'Normalização, descoberta de features e extração de conhecimento:'
                  : 'Normalization, feature discovery, and knowledge extraction:',
                'skald analyze',
              ],
              [
                pt ? '4 · Explore o catálogo' : '4 · Browse the catalog',
                pt ? 'Liste e inspecione features:' : 'List and inspect features:',
                'skald features list',
              ],
              [
                pt ? '5 · Exporte metadados (opcional)' : '5 · Export metadata (optional)',
                pt ? 'YAML a partir de uma feature:' : 'YAML from a feature:',
                'skald features export <FEATURE_ID> --format yaml',
              ],
              [
                pt ? '6 · Gere um rascunho' : '6 · Generate a draft',
                pt ? 'Markdown fundamentado na evidência:' : 'Markdown grounded in evidence:',
                'skald content draft <FEATURE_ID> --format article',
              ],
            ].map(([heading, body, command]) => (
              <section className="step" key={heading}>
                <div>
                  <h2>{heading}</h2>
                  <p>{body}</p>
                  {command && <CopyCommand command={command} />}
                  {heading.startsWith('2') && (
                    <>
                      <CopyCommand command="skald scan repo ./examples/sample-repo" />
                      <CopyCommand command="skald scan git ./examples/sample-repo" />
                    </>
                  )}
                </div>
              </section>
            ))}
          </div>
          <section className="detail-section">
            <h2>{pt ? 'Artefatos locais' : 'Local artifacts'}</h2>
            <ul>
              <li>
                <code>~/.config/devlog/config.yaml</code> —{' '}
                {pt ? 'configuração do workspace' : 'workspace configuration'}
              </li>
              <li>
                <code>~/.devlog/skald.db</code> — {pt ? 'catálogo SQLite' : 'SQLite catalog'}
              </li>
              <li>
                <code>~/.devlog/content/</code> — {pt ? 'rascunhos Markdown' : 'Markdown drafts'}
              </li>
            </ul>
          </section>
          <div className="notice">
            {pt
              ? 'Um commit não é um artigo. O Skald propõe metadados e rascunhos a partir de evidências — revise antes de publicar.'
              : 'A commit is not an article. Skald proposes metadata and drafts from evidence — review before you publish.'}
          </div>
        </>
      )}

      {kind === 'commands' && (
        <>
          <CommandTable />
          {commands.map(([name, command], i) => (
            <section className="detail-section" key={name}>
              <h2 className="font-mono">{name}</h2>
              <p>
                {(pt
                  ? [
                      'Cria config, workspace e banco SQLite.',
                      'Varre estrutura e metadados do repositório.',
                      'Ingere histórico de commits (incremental).',
                      'Normaliza, agrupa e extrai conhecimento em features.',
                      'Lista features descobertas no catálogo.',
                      'Gera rascunho Markdown (article por padrão).',
                    ]
                  : [
                      'Create config, workspace, and SQLite database.',
                      'Scan repository structure and metadata.',
                      'Ingest commit history (incremental).',
                      'Normalize, group, and extract knowledge into features.',
                      'List discovered features in the catalog.',
                      'Generate a Markdown draft (article by default).',
                    ])[i]}
              </p>
              <CopyCommand command={command} />
            </section>
          ))}
        </>
      )}

      {kind === 'safety' && (
        <>
          {[
            [
              pt ? 'Local-first' : 'Local-first',
              pt
                ? 'O workspace, o SQLite e os rascunhos ficam na sua máquina por padrão. Não há envio automático para serviços remotos.'
                : 'Workspace, SQLite, and drafts stay on your machine by default. There is no automatic remote submit.',
            ],
            [
              pt ? 'Caminhos sensíveis' : 'Sensitive paths',
              pt
                ? 'Scans excluem padrões como .env e material de chave. Não aponte o scanner a segredos de propósito.'
                : 'Scans exclude patterns such as .env and key material. Do not point the scanner at secrets on purpose.',
            ],
            [
              pt ? 'Tokens só no ambiente' : 'Tokens from the environment only',
              pt
                ? 'GITHUB_TOKEN é lido do ambiente para listagem pública opcional. Nunca versione tokens nem os registre em logs.'
                : 'GITHUB_TOKEN is read from the environment for optional public listing. Never commit tokens or log them.',
            ],
            [
              pt ? 'Rascunhos são arquivos' : 'Drafts are files',
              pt
                ? 'content draft grava Markdown local. Publicar, copiar ou descartar é decisão sua.'
                : 'content draft writes local Markdown. Publishing, copying, or discarding is your choice.',
            ],
            [
              pt ? 'LLM mock por padrão' : 'Mock LLM by default',
              pt
                ? 'O provedor de enriquecimento padrão é mock/offline. Um LLM real é planejado — não trate rascunhos como publicação automática.'
                : 'The default enrichment provider is mock/offline. A real LLM is planned — do not treat drafts as auto-publish.',
            ],
            [
              pt ? 'Proteja dados locais' : 'Protect local data',
              pt
                ? 'Não versione .env, tokens ou dumps com segredos. Use .env.example só com placeholders.'
                : 'Do not commit .env, tokens, or dumps with secrets. Use .env.example with placeholders only.',
            ],
          ].map(([heading, body]) => (
            <section className="detail-section" key={heading}>
              <h2>{heading}</h2>
              <p>{body}</p>
            </section>
          ))}
          <CopyCommand command="skald init" />
          <div className="notice">
            {pt
              ? 'Revise features export e content draft antes de compartilhar qualquer artefato fora da sua máquina.'
              : 'Review features export and content draft before sharing any artifact off your machine.'}
          </div>
        </>
      )}

      {kind === 'docs' && (
        <>
          <div className="notice">
            {pt ? 'Referência completa da CLI: ' : 'Full CLI reference: '}
            <a href={toolReadmeUrl} target="_blank" rel="noopener noreferrer">
              {pt ? 'README no GitHub' : 'README on GitHub'}
              <ArrowRight className="inline ml-1" />
            </a>
          </div>
          <section className="detail-section">
            <h2>{pt ? '01 · Instale' : '01 · Install'}</h2>
            <CopyCommand command="cd skald" />
            <CopyCommand command="python3 -m venv .venv" />
            <CopyCommand command="source .venv/bin/activate" />
            <CopyCommand command='pip install -e ".[dev]"' />
          </section>
          <section className="detail-section">
            <h2>{pt ? '02 · Ambiente (.env)' : '02 · Environment (.env)'}</h2>
            <CopyCommand command="cp .env.example .env" />
            <ul>
              <li>
                <code>SKALD_WORKSPACE</code> —{' '}
                {pt ? 'override opcional do workspace (~/.devlog)' : 'optional workspace override (~/.devlog)'}
              </li>
              <li>
                <code>GITHUB_TOKEN</code> —{' '}
                {pt
                  ? 'opcional: listagem pública via skald scan github'
                  : 'optional: public listing via skald scan github'}
              </li>
              <li>
                <code>SKALD_DATABASE_URL</code> —{' '}
                {pt ? 'override avançado / Alembic' : 'advanced / Alembic override'}
              </li>
            </ul>
            <p>
              {pt
                ? 'Nunca versione .env com segredos reais. Use apenas placeholders no exemplo.'
                : 'Never commit a .env with real secrets. Keep placeholders only in the example file.'}
            </p>
          </section>
          <section className="detail-section">
            <h2>{pt ? '03 · config.yaml' : '03 · config.yaml'}</h2>
            <p>{t.configLead}</p>
            <ConfigTable />
          </section>
          <section className="detail-section">
            <h2>{pt ? '04 · Fluxo inicial' : '04 · First run'}</h2>
            <CopyCommand command={commands[0][1]} />
            <CopyCommand command={commands[1][1]} />
            <CopyCommand command={commands[2][1]} />
            <CopyCommand command={commands[3][1]} />
            <CopyCommand command={commands[4][1]} />
            <p>
              {pt
                ? 'Depois use features show / export e content draft com um FEATURE_ID real.'
                : 'Then use features show / export and content draft with a real FEATURE_ID.'}
            </p>
          </section>
          <section className="detail-section">
            <h2>{pt ? 'Solução de problemas' : 'Troubleshooting'}</h2>
            <ul>
              <li>
                <strong>NotInitializedError</strong> —{' '}
                {pt ? 'rode skald init primeiro' : 'run skald init first'}
              </li>
              <li>
                <strong>No features</strong> —{' '}
                {pt
                  ? 'confirme scan repo + scan git antes de analyze'
                  : 'confirm scan repo + scan git before analyze'}
              </li>
              <li>
                <strong>GitHub listing empty</strong> —{' '}
                {pt
                  ? 'confira --user e se GITHUB_TOKEN é necessário para rate limit'
                  : 'check --user and whether GITHUB_TOKEN is needed for rate limits'}
              </li>
            </ul>
          </section>
          <section className="detail-section">
            <h2>{pt ? 'Limitações' : 'Limitations'}</h2>
            <ul>
              <li>
                {pt
                  ? 'Agrupamento semântico por embeddings ainda é planejado.'
                  : 'Semantic embedding-based grouping is still planned.'}
              </li>
              <li>
                {pt
                  ? 'Ingestão completa de commits/PRs do GitHub ainda é planejada.'
                  : 'Full GitHub commit/PR ingestion is still planned.'}
              </li>
              <li>
                {pt
                  ? 'O provedor LLM real ainda não está implementado (mock offline).'
                  : 'A real LLM provider is not implemented yet (offline mock).'}
              </li>
              <li>
                {pt
                  ? 'Rascunhos exigem revisão humana antes de qualquer publicação.'
                  : 'Drafts require human review before any publication.'}
              </li>
            </ul>
          </section>
        </>
      )}
    </div>
  );
}
