import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { AnalysisProvider } from "@/context/AnalysisContext";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { AuthProvider } from "@/contexts/auth-context";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { SyncInitializer } from "@/components/providers/SyncInitializer";

// Documented fallbacks for the proprietary Unica77 (UI) / CohereText (display) faces.
const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });
const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  display: "swap",
});

export const metadata: Metadata = {
  title: "TradingAgentsX - 多代理 LLM 金融交易",
  description: "由 AI 驅動的多代理 LLM 金融交易框架",
  icons: {
    icon: [
      { url: "/favicon-v8.png?t=20241220-v8", sizes: "32x32" },
      {
        url: "/icon-192-v8.png?t=20241220-v8",
        sizes: "192x192",
        type: "image/png",
      },
      {
        url: "/icon-512-v8.png?t=20241220-v8",
        sizes: "512x512",
        type: "image/png",
      },
      {
        url: "/icon-v8.png?t=20241220-v8",
        sizes: "1024x1024",
        type: "image/png",
      },
    ],
    apple: [
      {
        url: "/apple-touch-icon-v8.png?t=20241220-v8",
        sizes: "180x180",
        type: "image/png",
      },
    ],
    shortcut: "/favicon-v8.png?t=20241220-v8",
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "TAgentsX",
  },
  openGraph: {
    title: "TradingAgentsX - 多代理 LLM 金融交易",
    description: "由 AI 驅動的多代理 LLM 金融交易框架",
    siteName: "TradingAgentsX",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, viewport-fit=cover"
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              name: "TradingAgentsX",
              alternateName: "TradingAgentsX - 多代理 LLM 金融交易",
              url: "https://tradingagentsx.up.railway.app",
            }),
          }}
        />
        <link rel="manifest" href="/manifest.json?v=20241220-v8" />
        <meta
          name="google-site-verification"
          content="rKjd_gPy-7vtsGRcwVzAbAIYyIwVM9ezyXZOoXkC1KA"
        />
        <meta name="theme-color" content="#17171c" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta
          name="apple-mobile-web-app-status-bar-style"
          content="black-translucent"
        />
        <meta name="apple-mobile-web-app-title" content="TAgentsX" />
        {/* Timestamp forces iOS Safari to reload new icons */}
        {/* Precomposed version for iOS Safari Favorites */}
        <link
          rel="apple-touch-icon-precomposed"
          href="/apple-touch-icon-v8.png?t=20241220-v8"
        />
        <link
          rel="apple-touch-icon"
          href="/apple-touch-icon-v8.png?t=20241220-v8"
        />
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon-v8.png?t=20241220-v8"
        />
        <link
          rel="apple-touch-icon"
          sizes="152x152"
          href="/apple-touch-icon-v8.png?t=20241220-v8"
        />
        <link
          rel="apple-touch-icon"
          sizes="120x120"
          href="/apple-touch-icon-v8.png?t=20241220-v8"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-v8.png?t=20241220-v8"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="192x192"
          href="/icon-192-v8.png?t=20241220-v8"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="512x512"
          href="/icon-512-v8.png?t=20241220-v8"
        />
      </head>
      <body className={`${inter.variable} ${spaceGrotesk.variable} font-sans antialiased`}>
        <ThemeProvider>
          <LanguageProvider>
            <AuthProvider>
              <SyncInitializer />
              <AnalysisProvider>
                <div className="flex flex-col min-h-screen bg-background relative isolate">
                  <Header />
                  <main className="flex-1">{children}</main>
                  <Footer />
                </div>
              </AnalysisProvider>
            </AuthProvider>
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
