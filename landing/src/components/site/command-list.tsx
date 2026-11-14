import { commands } from '@/lib/site-content';
import { useLanguage } from './language';
export function CommandList() {
 const { t } = useLanguage();
 return <div className="command-list">{commands.map(([name, command], index) => <div className="command-row" key={name}><span className={name === 'submit' ? 'text-accent' : 'text-primary'}>{name}</span><code>{command}</code><span className="command-tag">{t.tags[index]}</span></div>)}</div>;
}
