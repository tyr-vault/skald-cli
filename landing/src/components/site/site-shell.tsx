import { Link } from '@tanstack/react-router';
import { ArrowUpRight, Menu, Moon, Sun, X } from 'lucide-react';
import { useState, type ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { brandSubtitle, productName } from '@/lib/brand';
import { navPaths } from '@/lib/site-content';
import { useLanguage } from './language';
import { useTheme } from './theme';

function Logo() {
  return (
    <span className="logo-mark" aria-hidden="true">
      <img src={`${import.meta.env.BASE_URL}favicon.ico`} alt="" width={38} height={38} />
    </span>
  );
}

export function SiteShell({ children }: { children: ReactNode }) {
  const { language, setLanguage, t } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const [open, setOpen] = useState(false);
  const themeLabel = theme === 'dark' ? t.themeLight : t.themeDark;

  return (
    <div className="site">
      <div className="site-grid" aria-hidden="true" />
      <div className="site-container">
        <header className="site-header">
          <Link to="/" className="brand" onClick={() => setOpen(false)}>
            <Logo />
            <span className="brand-name">
              {productName} <span>{brandSubtitle[language]}</span>
            </span>
            <span className="version">v0.1.0</span>
          </Link>
          <nav
            className="desktop-nav"
            aria-label={language === 'en' ? 'Main navigation' : 'Navegação principal'}
          >
            {navPaths.map((path, i) => (
              <Link key={path} to={path} activeProps={{ className: 'active' }}>
                {t.nav[i]}
              </Link>
            ))}
          </nav>
          <div className="header-actions">
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="theme-switch"
              aria-label={themeLabel}
              title={themeLabel}
              onClick={toggleTheme}
            >
              {theme === 'dark' ? <Sun /> : <Moon />}
            </Button>
            <div className="language-switch" aria-label="Language">
              <Button
                variant="language"
                data-active={language === 'en'}
                aria-pressed={language === 'en'}
                onClick={() => setLanguage('en')}
              >
                EN
              </Button>
              <Button
                variant="language"
                data-active={language === 'pt'}
                aria-pressed={language === 'pt'}
                onClick={() => setLanguage('pt')}
              >
                PT-BR
              </Button>
            </div>
            <Button asChild variant="action" className="header-install">
              <Link to="/docs">
                <span className="font-mono">$</span>
                {t.install}
                <ArrowUpRight />
              </Link>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="mobile-toggle"
              aria-label={open ? 'Close menu' : 'Open menu'}
              aria-expanded={open}
              onClick={() => setOpen(!open)}
            >
              {open ? <X /> : <Menu />}
            </Button>
          </div>
        </header>
        {open && (
          <nav className="mobile-nav">
            {navPaths.map((path, i) => (
              <Link key={path} to={path} onClick={() => setOpen(false)}>
                {t.nav[i]}
              </Link>
            ))}
          </nav>
        )}
        <main>{children}</main>
        <footer className="site-footer">
          <span className="copyright">{t.copyright}</span>
          <span className="made-with">
            {t.madeWith}{' '}
            <span className="made-heart" aria-hidden="true">
              ♥
            </span>{' '}
            rdvid
          </span>
        </footer>
      </div>
    </div>
  );
}
