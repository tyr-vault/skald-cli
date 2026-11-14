import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { copy, type Language } from '@/lib/site-content';
const LanguageContext = createContext<{ language: Language; setLanguage: (language: Language) => void }>({ language: 'en', setLanguage: () => {} });
export function LanguageProvider({ children }: { children: ReactNode }) {
 const [language, setLanguage] = useState<Language>('en');
 useEffect(() => { document.documentElement.lang = language === 'pt' ? 'pt-BR' : 'en'; }, [language]);
 return <LanguageContext.Provider value={{ language, setLanguage }}>{children}</LanguageContext.Provider>;
}
export function useLanguage() { const context = useContext(LanguageContext); return { ...context, t: copy[context.language] }; }
