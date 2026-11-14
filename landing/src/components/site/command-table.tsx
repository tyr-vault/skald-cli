import { commandCatalog, flagCommands, flagRows, skipReasons } from '@/lib/site-content';
import { useLanguage } from './language';

export function CommandTable({ compact = false }: { compact?: boolean }) {
  const { language, t } = useLanguage();
  const commands = commandCatalog[language];
  const flags = flagRows[language];
  const skips = skipReasons[language];

  return (
    <div className="command-tables">
      <section className="command-table-block">
        <h2>{t.tableCommands}</h2>
        <div className="ref-table-wrap">
          <table className="ref-table">
            <thead>
              <tr>
                <th>{t.colCommand}</th>
                <th>{t.colPurpose}</th>
              </tr>
            </thead>
            <tbody>
              {commands.map(([name, purpose]) => (
                <tr key={name}>
                  <td><code>{name}</code></td>
                  <td>{purpose}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="command-table-block">
        <h2>{t.tableFlags}</h2>
        <div className="ref-table-wrap">
          <table className="ref-table ref-table-flags">
            <thead>
              <tr>
                <th>{t.colFlag}</th>
                {flagCommands.map((name) => (
                  <th key={name}><code>{name}</code></th>
                ))}
                <th>{t.colDefault}</th>
                <th>{t.colMeaning}</th>
              </tr>
            </thead>
            <tbody>
              {flags.map(([flag, analyze, report, exportCmd, submit, rollback, fallback, meaning]) => (
                <tr key={flag}>
                  <td><code>{flag}</code></td>
                  {[analyze, report, exportCmd, submit, rollback].map((on, i) => (
                    <td key={flagCommands[i]} className={on ? 'flag-on' : 'flag-off'}>
                      {on ? t.flagOn : t.flagOff}
                    </td>
                  ))}
                  <td><code>{fallback}</code></td>
                  <td>{meaning}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {!compact && (
        <section className="command-table-block">
          <h2>{t.tableSkips}</h2>
          <div className="ref-table-wrap">
            <table className="ref-table">
              <thead>
                <tr>
                  <th>{t.colReason}</th>
                  <th>{t.colMeaning}</th>
                </tr>
              </thead>
              <tbody>
                {skips.map(([reason, meaning]) => (
                  <tr key={reason}>
                    <td>{reason}</td>
                    <td>{meaning}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
