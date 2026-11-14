import { configYaml } from '@/lib/site-content';
import { useLanguage } from './language';

export function ConfigTable() {
  const { language } = useLanguage();

  return (
    <div className="yaml-doc" aria-label="config.yaml">
      {configYaml[language].map((line, index) => (
        <div className="yaml-line" key={`${line.key ?? line.item}-${line.indent}-${index}`} style={{ paddingLeft: `${line.indent * 22}px` }}>
          {line.item != null ? (
            <span className="yaml-item"><span className="yaml-dash">-</span> {line.item}</span>
          ) : (
            <>
              <span className="yaml-key">{line.key}</span>
              {line.value != null && <span className="yaml-colon">: </span>}
              {line.value != null && <span className="yaml-value">{line.value}</span>}
              {line.value == null && <span className="yaml-colon">:</span>}
            </>
          )}
          {line.effect && <span className="yaml-effect"> # {line.effect}</span>}
        </div>
      ))}
    </div>
  );
}
