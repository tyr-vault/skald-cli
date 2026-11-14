import { useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useLanguage } from './language';
export function CopyCommand({ command }: { command: string }) {
 const [copied, setCopied] = useState(false);
 const [failed, setFailed] = useState(false);
 const { t, language } = useLanguage();
 async function handleCopy() {
  try { await navigator.clipboard.writeText(command); setCopied(true); setFailed(false); setTimeout(() => setCopied(false), 2000); }
  catch { setFailed(true); }
 }
 return <div className="copy-command"><code><span className="text-primary">$ </span>{command}</code><Button variant="ghost" size="icon" onClick={handleCopy} aria-label={copied ? t.copied : t.copy} title={copied ? t.copied : t.copy}>{copied ? <Check /> : <Copy />}</Button>{failed && <span role="status">{language === 'en' ? 'Select the command to copy it.' : 'Selecione o comando para copiar.'}</span>}</div>;
}
