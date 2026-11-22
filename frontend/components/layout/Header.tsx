/**
 * Header component with mobile-responsive design and i18n support
 */
"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { ApiSettingsDialog } from "@/components/settings/ApiSettingsDialog";
import { LanguageSwitcher } from "@/components/settings/LanguageSwitcher";
import { LoginButton } from "@/components/auth/login-button";
import { Button } from "@/components/ui/button";
import { useLanguage } from "@/contexts/LanguageContext";
import { usePathname } from "next/navigation";

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { t } = useLanguage();
  const pathname = usePathname();

  if (pathname === "/history/chat") return null;

  // The analysis results page renders already-generated report text, which
  // stays fixed in whichever language it was produced in. Switching the UI
  // locale there would leave the page showing report content and chrome in
  // two different languages, so the switcher is locked while it's open.
  const isReportDetailPage = pathname === "/analysis/results";

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background pwa-safe-header">
      <div className="container mx-auto px-4 py-4 md:py-5">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <div className="font-display text-xl md:text-2xl tracking-tight text-foreground">
              TradingAgentsX
            </div>
            <div className="hidden lg:block type-mono-label text-xs text-muted-foreground">
              {t.nav.tagline}
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-1 lg:gap-2 items-center">
            <Link
              href="/"
              className="px-3 py-2 text-sm text-foreground/80 underline-offset-8 hover:text-foreground hover:underline decoration-1 transition-colors"
            >
              {t.nav.home}
            </Link>
            <Link
              href="/analysis"
              className="px-3 py-2 text-sm text-foreground/80 underline-offset-8 hover:text-foreground hover:underline decoration-1 transition-colors"
            >
              {t.nav.analysis}
            </Link>
            <Link
              href="/history"
              className="px-3 py-2 text-sm text-foreground/80 underline-offset-8 hover:text-foreground hover:underline decoration-1 transition-colors"
            >
              {t.nav.history}
            </Link>
            <Link
              href="/demo"
              className="px-3 py-2 text-sm text-foreground/80 underline-offset-8 hover:text-foreground hover:underline decoration-1 transition-colors"
            >
              {t.demo.nav}
            </Link>
            <ApiSettingsDialog />
            <LanguageSwitcher disabled={isReportDetailPage} />
            <ThemeToggle />
            <LoginButton />
          </nav>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center gap-2">
            <LanguageSwitcher disabled={isReportDetailPage} />
            <ThemeToggle />
            <Button
              variant="ghost"
              size="icon"
              className="text-foreground/80"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-4 pt-4 border-t border-border space-y-1">
            <Link
              href="/"
              className="block px-3 py-2 text-foreground/80 hover:text-foreground hover:underline underline-offset-8 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.home}
            </Link>
            <Link
              href="/analysis"
              className="block px-3 py-2 text-foreground/80 hover:text-foreground hover:underline underline-offset-8 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.analysis}
            </Link>
            <Link
              href="/history"
              className="block px-3 py-2 text-foreground/80 hover:text-foreground hover:underline underline-offset-8 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.nav.history}
            </Link>
            <Link
              href="/demo"
              className="block px-3 py-2 text-foreground/80 hover:text-foreground hover:underline underline-offset-8 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              {t.demo.nav}
            </Link>
            <div className="flex items-center gap-3 pt-2">
              <ApiSettingsDialog />
              <LoginButton />
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}
