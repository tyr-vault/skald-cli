export type Language = 'en' | 'pt';
export const copy = {
 en: {
  nav: ['How it works', 'Commands', 'Safety', 'Docs'], install: 'install', start: 'get started', readme: 'read the README',
  headline: ['Keep the story', 'of your', 'engineering work.'], intro: 'Skald is a local-first CLI that turns Git engineering activity into structured feature metadata, a SQLite knowledge catalog, and grounded Markdown drafts — not a hosted analytics SaaS and not an ungrounded article bot.',
  trust: ['local-first SQLite', 'evidence-backed drafts', 'Python 3.10+'],
  features: [
    ['01 · extract', 'Git activity in', 'Scan repository structure and commit history locally. Sensitive paths stay excluded; optional GitHub listing uses an env token only.'],
    ['02 · catalog', 'Features in SQLite', 'Deterministic grouping and knowledge extraction produce a feature catalog you can list, show, and export as YAML.'],
    ['03 · draft', 'Grounded content', 'Jinja templates write article, learning-note, and LinkedIn drafts from feature evidence — review before you publish.'],
  ],
  workflow: 'the workflow', workflowTitle: ['Scan. Analyze.', 'Draft from evidence.'], workflowText: 'Initialize a workspace, scan a repo and its git history, run analyze to discover features, then list or export metadata and generate a draft when you are ready.',
  reference: 'the CLI · v0.1.0', referenceTitle: ['Six commands.', 'Options, mapped.'], referenceText: 'Entry point: skald <command> [options]. Run skald init once so config and SQLite live under your workspace.',
  tableCommands: 'Commands', tableFlags: 'Options by command', tableSkips: 'Common blockers',
  colCommand: 'Command', colPurpose: 'What it does', colFlag: 'Option', colDefault: 'Default', colMeaning: 'Meaning', colReason: 'Reason',
  colKey: 'Key', colEffect: 'Effect', configLead: 'Created by skald init under ~/.config/devlog/config.yaml. Override paths with env vars — never commit secrets.',
  flagOn: 'yes', flagOff: '—',
  tags: ['init', 'scan', 'analyze', 'features', 'draft', 'report'], internal: 'local CLI · v0.1.0', demo: 'example session',
  scan: 'scanning sample-repo · tree + commit history', reconstructed: '12 commits stored', confidence: '3 features discovered', gaps: 'sensitive paths skipped', unassigned: '· .env keys excluded', total: 'catalog ready · confidence 0.82 avg', preview: 'article draft from feature evidence', nothing: 'written under workspace content/', rollback: 'terminal activity report · local only',
  footer: 'Turn engineering activity into reusable technical knowledge.', copyright: '© 2026 Skald. All rights reserved.', madeWith: 'made with', back: 'Back to home', copied: 'Copied', copy: 'Copy command',
  themeLight: 'Switch to light theme', themeDark: 'Switch to dark theme',
 },
 pt: {
  nav: ['Como funciona', 'Comandos', 'Segurança', 'Documentação'], install: 'instalar', start: 'começar agora', readme: 'ler o README',
  headline: ['Guarde a história', 'do seu', 'trabalho de engenharia.'], intro: 'Skald é um CLI local-first que transforma atividade de engenharia no Git em metadados de features, um catálogo SQLite e rascunhos Markdown baseados em evidência — não é um SaaS de analytics nem um gerador cego de artigos.',
  trust: ['SQLite local', 'rascunhos com evidência', 'Python 3.10+'],
  features: [
    ['01 · extrair', 'Atividade Git', 'Varre estrutura do repositório e histórico de commits localmente. Caminhos sensíveis ficam de fora; listagem GitHub opcional usa token só do ambiente.'],
    ['02 · catálogo', 'Features no SQLite', 'Agrupamento determinístico e extração de conhecimento geram um catálogo que você lista, inspeciona e exporta em YAML.'],
    ['03 · rascunho', 'Conteúdo fundamentado', 'Templates Jinja geram article, learning-note e LinkedIn a partir das evidências da feature — revise antes de publicar.'],
  ],
  workflow: 'o fluxo de trabalho', workflowTitle: ['Escaneie. Analise.', 'Rascunhe com evidência.'], workflowText: 'Inicialize o workspace, escaneie o repo e o histórico Git, rode analyze para descobrir features e então liste, exporte ou gere um rascunho quando estiver pronto.',
  reference: 'a CLI · v0.1.0', referenceTitle: ['Seis comandos.', 'Opções mapeadas.'], referenceText: 'Entrada: skald <command> [options]. Rode skald init uma vez para criar config e SQLite no workspace.',
  tableCommands: 'Comandos', tableFlags: 'Opções por comando', tableSkips: 'Bloqueios comuns',
  colCommand: 'Comando', colPurpose: 'O que faz', colFlag: 'Opção', colDefault: 'Padrão', colMeaning: 'Significado', colReason: 'Motivo',
  colKey: 'Chave', colEffect: 'Efeito', configLead: 'Criado por skald init em ~/.config/devlog/config.yaml. Sobrescreva caminhos via env — nunca versione segredos.',
  flagOn: 'sim', flagOff: '—',
  tags: ['init', 'scan', 'analyze', 'features', 'rascunho', 'relatório'], internal: 'CLI local · v0.1.0', demo: 'sessão de exemplo',
  scan: 'escaneando sample-repo · árvore + histórico', reconstructed: '12 commits armazenados', confidence: '3 features descobertas', gaps: 'caminhos sensíveis ignorados', unassigned: '· .env e chaves excluídos', total: 'catálogo pronto · confiança média 0,82', preview: 'rascunho article a partir da feature', nothing: 'gravado em content/ do workspace', rollback: 'relatório de atividade · só local',
  footer: 'Transforme atividade de engenharia em conhecimento técnico reutilizável.', copyright: '© 2026 Skald. Todos os direitos reservados.', madeWith: 'made with', back: 'Voltar ao início', copied: 'Copiado', copy: 'Copiar comando',
  themeLight: 'Mudar para tema claro', themeDark: 'Mudar para tema escuro',
 }
};
export const commands = [
 ['init', 'skald init'],
 ['scan repo', 'skald scan repo ./examples/sample-repo'],
 ['scan git', 'skald scan git ./examples/sample-repo'],
 ['analyze', 'skald analyze'],
 ['features', 'skald features list'],
 ['draft', 'skald content draft <FEATURE_ID> --format article'],
] as const;
export const navPaths = ['/how-it-works', '/commands', '/safety', '/docs'] as const;

export const commandCatalog = {
  en: [
    ['init', 'Create config, workspace, and SQLite catalog'],
    ['scan repo', 'Scan repository structure, docs, deps, and CI hints'],
    ['scan git', 'Ingest commit history (incremental, truncated diffs)'],
    ['scan github', 'List public repositories for a GitHub user (optional token)'],
    ['analyze', 'Normalize data, discover features, extract knowledge'],
    ['features list|show|export', 'Browse the feature catalog or export YAML'],
    ['content draft', 'Generate a Markdown draft (article, learning-note, linkedin)'],
    ['report', 'Print a terminal activity summary'],
  ],
  pt: [
    ['init', 'Cria config, workspace e catálogo SQLite'],
    ['scan repo', 'Varre estrutura, docs, deps e pistas de CI'],
    ['scan git', 'Ingere histórico de commits (incremental, diffs truncados)'],
    ['scan github', 'Lista repositórios públicos de um usuário GitHub (token opcional)'],
    ['analyze', 'Normaliza dados, descobre features e extrai conhecimento'],
    ['features list|show|export', 'Navega o catálogo ou exporta YAML'],
    ['content draft', 'Gera rascunho Markdown (article, learning-note, linkedin)'],
    ['report', 'Imprime resumo de atividade no terminal'],
  ],
} as const;

export const flagRows = {
  en: [
    ['PATH', true, false, false, false, false, 'required', 'Local git repository path (scan repo / scan git)'],
    ['--limit N', true, false, false, false, false, 'config', 'Max commits for scan git'],
    ['--since-sha SHA', true, false, false, false, false, 'off', 'Scan commits after SHA (incremental)'],
    ['--user NAME', true, false, false, false, false, 'required', 'GitHub username for scan github'],
    ['--repository-id ID', false, true, false, false, false, 'all', 'Limit analyze to one repository'],
    ['FEATURE_ID', false, false, true, true, false, 'required', 'Target feature for show, export, or draft'],
    ['--format F', false, false, true, true, false, 'yaml|article', 'Export YAML or draft format (article|learning-note|linkedin)'],
    ['--config PATH', false, false, false, false, false, '~/.config/devlog/config.yaml', 'Override config path on init'],
  ],
  pt: [
    ['PATH', true, false, false, false, false, 'obrigatório', 'Caminho do repositório git (scan repo / scan git)'],
    ['--limit N', true, false, false, false, false, 'config', 'Máximo de commits em scan git'],
    ['--since-sha SHA', true, false, false, false, false, 'off', 'Escaneia commits após o SHA (incremental)'],
    ['--user NAME', true, false, false, false, false, 'obrigatório', 'Usuário GitHub para scan github'],
    ['--repository-id ID', false, true, false, false, false, 'todos', 'Limita analyze a um repositório'],
    ['FEATURE_ID', false, false, true, true, false, 'obrigatório', 'Feature alvo para show, export ou draft'],
    ['--format F', false, false, true, true, false, 'yaml|article', 'Export YAML ou formato do rascunho'],
    ['--config PATH', false, false, false, false, false, '~/.config/devlog/config.yaml', 'Sobrescreve o caminho da config no init'],
  ],
} as const;

/** Columns in the options matrix (left to right). */
export const flagCommands = ['scan', 'analyze', 'features', 'content', 'report'] as const;

export const skipReasons = {
  en: [
    ['Not initialized', 'Run skald init before scan, analyze, features, content, or report'],
    ['Empty catalog', 'No features yet — scan a repo and git history, then skald analyze'],
    ['Sensitive paths', 'Scans skip patterns such as .env and key material by design'],
  ],
  pt: [
    ['Não inicializado', 'Rode skald init antes de scan, analyze, features, content ou report'],
    ['Catálogo vazio', 'Sem features — escaneie o repo e o git, depois skald analyze'],
    ['Caminhos sensíveis', 'Scans ignoram padrões como .env e material de chave de propósito'],
  ],
} as const;

export type ConfigYamlLine = {
  indent: number;
  key?: string;
  value?: string;
  item?: string;
  effect?: string;
};

export const configYaml: Record<'en' | 'pt', ConfigYamlLine[]> = {
  en: [
    { indent: 0, key: 'workspace', effect: 'Local workspace root for artifacts and content' },
    { indent: 1, key: 'path', value: '"~/.devlog"', effect: 'Override with SKALD_WORKSPACE' },
    { indent: 0, key: 'storage' },
    { indent: 1, key: 'database', value: '"~/.devlog/skald.db"', effect: 'SQLite knowledge catalog' },
    { indent: 0, key: 'analysis', effect: 'Grouping and extraction thresholds' },
    { indent: 1, key: 'max_diff_size', value: '50000' },
    { indent: 1, key: 'default_history_limit', value: '1000' },
    { indent: 1, key: 'grouping_window_hours', value: '72' },
    { indent: 1, key: 'minimum_group_confidence', value: '0.65' },
    { indent: 0, key: 'github' },
    { indent: 1, key: 'token_env', value: '"GITHUB_TOKEN"', effect: 'Env var name only — never commit the token' },
    { indent: 0, key: 'llm' },
    { indent: 1, key: 'provider', value: '"mock"', effect: 'Offline mock by default; real LLM is planned' },
    { indent: 0, key: 'content' },
    { indent: 1, key: 'default_language', value: '"en"' },
    { indent: 1, key: 'output_directory', value: '"~/.devlog/content"' },
  ],
  pt: [
    { indent: 0, key: 'workspace', effect: 'Raiz local para artefatos e conteúdo' },
    { indent: 1, key: 'path', value: '"~/.devlog"', effect: 'Sobrescreva com SKALD_WORKSPACE' },
    { indent: 0, key: 'storage' },
    { indent: 1, key: 'database', value: '"~/.devlog/skald.db"', effect: 'Catálogo SQLite de conhecimento' },
    { indent: 0, key: 'analysis', effect: 'Limiares de agrupamento e extração' },
    { indent: 1, key: 'max_diff_size', value: '50000' },
    { indent: 1, key: 'default_history_limit', value: '1000' },
    { indent: 1, key: 'grouping_window_hours', value: '72' },
    { indent: 1, key: 'minimum_group_confidence', value: '0.65' },
    { indent: 0, key: 'github' },
    { indent: 1, key: 'token_env', value: '"GITHUB_TOKEN"', effect: 'Só o nome da variável — nunca versione o token' },
    { indent: 0, key: 'llm' },
    { indent: 1, key: 'provider', value: '"mock"', effect: 'Mock offline por padrão; LLM real é planejado' },
    { indent: 0, key: 'content' },
    { indent: 1, key: 'default_language', value: '"en"' },
    { indent: 1, key: 'output_directory', value: '"~/.devlog/content"' },
  ],
};
