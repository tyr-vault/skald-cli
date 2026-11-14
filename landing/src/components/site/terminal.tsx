import { useLanguage } from './language';

export function Terminal() {
  const { t } = useLanguage();
  return (
    <div className="terminal-stage">
      <div className="terminal-backplate" aria-hidden="true" />
      <div className="terminal-frame">
        <div className="terminal-title">
          <span className="terminal-dots">
            <i />
            <i />
            <i />
          </span>
          <span>~/skald</span>
          <span className="terminal-example">{t.demo}</span>
        </div>
        <div className="terminal-body">
          <div className="terminal-command">
            <span>$</span> skald init
          </div>
          <div className="terminal-output">workspace · config · sqlite ready</div>
          <div className="terminal-command terminal-next">
            <span>$</span> skald scan repo <span>./examples/sample-repo</span>
          </div>
          <div className="terminal-command">
            <span>$</span> skald scan git <span>./examples/sample-repo</span>
          </div>
          <div className="terminal-output">{t.scan}</div>
          <div>
            {t.reconstructed} · <span className="text-primary">{t.confidence}</span>
          </div>
          <div>
            {t.gaps} <span className="text-muted-foreground">{t.unassigned}</span>
          </div>
          <div className="terminal-command terminal-next">
            <span>$</span> skald analyze
          </div>
          <div className="terminal-output">{t.total}</div>
          <div className="terminal-command terminal-next">
            <span>$</span> skald content draft <span>feat_01</span>{' '}
            <span className="text-muted-foreground">--format</span> <span>article</span>
          </div>
          <div>
            <span className="text-accent">[draft]</span> {t.preview}
          </div>
          <div className="terminal-output">
            {t.nothing} <span className="text-foreground">article.md</span>
          </div>
          <div className="terminal-command terminal-next">
            <span>$</span> skald report
          </div>
          <div className="terminal-output">{t.rollback}</div>
          <div className="terminal-prompt">
            <span>$ </span>
            <span className="cursor">▍</span>
          </div>
        </div>
      </div>
    </div>
  );
}
