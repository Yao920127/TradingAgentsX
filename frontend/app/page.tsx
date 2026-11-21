"use client";

import Link from "next/link";
import Image from "next/image";
import {
  Bot,
  Globe,
  Wrench,
  BarChart3,
  RefreshCw,
  Brain,
  Palette,
  Container,
  Download,
  TrendingUp,
  TrendingDown,
  Users,
  Shield,
  Zap,
  Database,
  Lock,
  CheckCircle2,
  Map as MapIcon,
  ExternalLink,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { AgentFlowDiagram } from "@/components/AgentFlowDiagram";
import { Hero } from "@/components/home/Hero";
import { InteractiveCard } from "@/components/home/InteractiveCard";
import { ScrollReveal } from "@/components/home/ScrollReveal";
import { useLanguage } from "@/contexts/LanguageContext";

const ARCHITECTURE_MAP_URL = "https://floorplan-tradinganentsx.up.railway.app";

export default function HomePage() {
  const { t } = useLanguage();

  return (
    <div>
      <Hero />

            <div className="relative z-10 overflow-x-clip">
        <div className="container mx-auto px-4 pt-16 pb-12">

        {/* Core Features Section */}
        <ScrollReveal from="left" className="mb-24 md:mb-section">
          <SectionHeading eyebrow={t.home.subtitle} title={t.home.coreFeatures} />
          <p className="text-center text-muted-foreground mb-10 max-w-3xl mx-auto text-lg">
            {t.home.coreFeaturesDesc}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard title={t.home.features.multiAgent} description={t.home.features.multiAgentDesc} icon={<Bot className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.multiModel} description={t.home.features.multiModelDesc} icon={<Globe className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.customEndpoint} description={t.home.features.customEndpointDesc} icon={<Wrench className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.fullAnalysis} description={t.home.features.fullAnalysisDesc} icon={<BarChart3 className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.structuredDecision} description={t.home.features.structuredDecisionDesc} icon={<RefreshCw className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.longTermMemory} description={t.home.features.longTermMemoryDesc} icon={<Brain className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.modernUI} description={t.home.features.modernUIDesc} icon={<Palette className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.oneClickDeploy} description={t.home.features.oneClickDeployDesc} icon={<Container className="w-6 h-6" />} />
            <FeatureCard title={t.home.features.reportDownload} description={t.home.features.reportDownloadDesc} icon={<Download className="w-6 h-6" />} />
          </div>
        </ScrollReveal>

        {/* 12 Professional Agents Section */}
        <ScrollReveal from="right" className="mb-24 md:mb-section">
          <SectionHeading eyebrow={t.home.subtitle} title={t.home.professionalAgents} />
          <p className="text-center text-muted-foreground mb-10 max-w-3xl mx-auto text-lg">
            {t.home.professionalAgentsDesc}
          </p>

          {/* Analyst Team */}
          <div className="mb-8">
            <h3 className="font-display text-2xl mb-4 text-foreground flex items-center gap-2">
              <BarChart3 className="w-5 h-5" />
              {t.home.analystsTeamTitle}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <AgentCard name={t.agents.market_analyst} role={t.agents.market_analyst_role} description={t.agents.market_analyst_desc} />
              <AgentCard name={t.agents.social_analyst} role={t.agents.social_analyst_role} description={t.agents.social_analyst_desc} />
              <AgentCard name={t.agents.news_analyst} role={t.agents.news_analyst_role} description={t.agents.news_analyst_desc} />
              <AgentCard name={t.agents.fundamentals_analyst} role={t.agents.fundamentals_analyst_role} description={t.agents.fundamentals_analyst_desc} />
              <AgentCard name={t.agents.report_summarizer} role={t.agents.report_summarizer_role} description={t.agents.report_summarizer_desc} />
            </div>
          </div>

          {/* Research Team */}
          <div className="mb-8">
            <h3 className="font-display text-2xl mb-4 text-foreground flex items-center gap-2">
              <Brain className="w-5 h-5" />
              {t.home.researchTeamTitle}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <AgentCard name={t.agents.bull_researcher} role={t.agents.bull_researcher_role} description={t.agents.bull_researcher_desc} accent="bull" />
              <AgentCard name={t.agents.bear_researcher} role={t.agents.bear_researcher_role} description={t.agents.bear_researcher_desc} accent="bear" />
              <AgentCard name={t.agents.research_manager} role={t.agents.research_manager_role} description={t.agents.research_manager_desc} />
            </div>
          </div>

          {/* Trading Team */}
          <div className="mb-8">
            <h3 className="font-display text-2xl mb-4 text-foreground flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              {t.home.tradingTeamTitle}
            </h3>
            <div className="grid grid-cols-1 gap-4 max-w-md mx-auto">
              <AgentCard name={t.agents.trader} role={t.agents.trader_role} description={t.agents.trader_desc} />
            </div>
          </div>

          {/* Risk Management Team */}
          <div className="mb-8">
            <h3 className="font-display text-2xl mb-4 text-foreground flex items-center gap-2">
              <Shield className="w-5 h-5" />
              {t.home.riskTeamTitle}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <AgentCard name={t.agents.aggressive_debator} role={t.agents.aggressive_debator_role} description={t.agents.aggressive_debator_desc} />
              <AgentCard name={t.agents.conservative_debator} role={t.agents.conservative_debator_role} description={t.agents.conservative_debator_desc} />
              <AgentCard name={t.agents.neutral_debator} role={t.agents.neutral_debator_role} description={t.agents.neutral_debator_desc} />
              <AgentCard name={t.agents.risk_manager} role={t.agents.risk_manager_role} description={t.agents.risk_manager_desc} />
            </div>
          </div>
        </ScrollReveal>

        {/* Agent Flow Diagram Section */}
        <ScrollReveal from="left" className="mb-24 md:mb-section">
          <SectionHeading title={t.home.workflowTitle} />
          <p className="text-center text-muted-foreground mb-10 max-w-3xl mx-auto text-lg">
            {t.home.workflowDescription}
          </p>
          <AgentFlowDiagram />
        </ScrollReveal>

        {/* LLM Support Section */}
        <ScrollReveal from="right" className="mb-24 md:mb-section">
          <SectionHeading title={t.home.llmSupport} />
          <p className="text-center text-muted-foreground mb-10 max-w-3xl mx-auto text-lg">
            {t.home.llmSupportDesc}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <LLMProviderCard name="OpenAI" models={["GPT-6 Astra", "GPT-6.1 Sol","GPT-6.1 Terra", "GPT-6 Luna"]} />
            <LLMProviderCard name="Anthropic" models={["Claude Fable 5.2","Claude Opus 5.5","Claude Sonnet 5.5","Claude Haiku 5.5"]} />
            <LLMProviderCard name="Google Gemini" models={["Gemini 4 Carbon","Gemini 4 Argon","Gemini 4 Hydrogen"]} />
            <LLMProviderCard name="Grok (xAI)" models={["Grok 4.7","Grok 4.6","Grok 4.5","Grok 4.3"]} />
            <LLMProviderCard name="DeepSeek" models={["DeepSeek-V4-Pro", "DeepSeek-V4.1-Flash"]} />
            <LLMProviderCard name="Qwen (Alibaba)" models={["Qwen3.8-Max","Qwen3.8-Flash","Qwen3.7-Plus"]} />
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-muted-foreground">
              {t.home.llmFeatures}
            </p>
          </div>
        </ScrollReveal>

        {/* Workflow Section */}
        <ScrollReveal from="left" className="mb-24 md:mb-section">
          <SectionHeading title={t.home.workflowTitle} />
          <Card className="rounded-sm">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <WorkflowStep number={1} title={t.home.processSteps.dataCollection.title} description={t.home.processSteps.dataCollection.description} />
                <WorkflowStep number={2} title={t.home.processSteps.analysts.title} description={t.home.processSteps.analysts.description} />
                <WorkflowStep number={3} title={t.home.processSteps.researchers.title} description={t.home.processSteps.researchers.description} />
                <WorkflowStep number={4} title={t.home.processSteps.trader.title} description={t.home.processSteps.trader.description} />
                <WorkflowStep number={5} title={t.home.processSteps.risk.title} description={t.home.processSteps.risk.description} />
                <WorkflowStep number={6} title={t.home.processSteps.finalDecision.title} description={t.home.processSteps.finalDecision.description} />
              </div>
            </CardContent>
          </Card>
        </ScrollReveal>

        {/* Technical Highlights */}
        <ScrollReveal from="right" className="mb-24 md:mb-section">
          <SectionHeading title={t.home.techHighlights} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TechnicalCard title={t.home.dynamicResearch} features={t.home.dynamicResearchFeatures} icon={<Zap className="w-5 h-5" />} />
            <TechnicalCard title={t.home.memorySystem} features={t.home.memorySystemFeatures} icon={<Database className="w-5 h-5" />} />
            <TechnicalCard title={t.home.realTimeData} features={t.home.realTimeDataFeatures} icon={<TrendingUp className="w-5 h-5" />} />
            <TechnicalCard title={t.home.fullApiSupport} features={t.home.fullApiSupportFeatures} icon={<Lock className="w-5 h-5" />} />
          </div>
        </ScrollReveal>

        {/* Architecture Map Section */}
        <ScrollReveal from="left" className="mb-24 md:mb-section">
          <SectionHeading title={t.home.architectureMapTitle} />
          <InteractiveCard>
            <Card className="max-w-3xl mx-auto rounded-sm">
              <CardContent className="pt-6 flex flex-col items-center text-center gap-6">
                <MapIcon className="w-8 h-8 text-deep-green dark:text-pale-green" />
                <p className="text-muted-foreground max-w-2xl">
                  {t.home.architectureMapDesc}
                </p>
                <a href={ARCHITECTURE_MAP_URL} target="_blank" rel="noopener noreferrer">
                  <Button size="lg" className="gap-2">
                    {t.home.architectureMapButton}
                    <ExternalLink className="w-4 h-4" />
                  </Button>
                </a>
              </CardContent>
            </Card>
          </InteractiveCard>
        </ScrollReveal>

        {/* Call to Action — deep-green feature band */}
        <ScrollReveal className="rounded-lg bg-deep-green px-6 py-20 text-center text-white md:py-section">
          <h2 className="font-display text-4xl sm:text-section mb-6 tracking-[-0.02em] leading-none">
            {t.home.readyToStart}
          </h2>
          <p className="mx-auto mb-10 max-w-2xl text-lg text-white/80">{t.home.ctaDescription}</p>
          <Button asChild size="lg" className="bg-white text-near-black hover:bg-white/85">
            <Link href="/analysis">{t.home.startAnalysis} →</Link>
          </Button>
        </ScrollReveal>
        </div>
      </div>
    </div>
  );
}

/* ── Shared sub-components ── */

const CHECK_ICON = "text-deep-green dark:text-pale-green flex-shrink-0";

function SectionHeading({ title, eyebrow }: { title: string; eyebrow?: string }) {
  return (
    <div className="text-center mb-6">
      {eyebrow && <span className="type-mono-label mb-3 inline-block text-muted-foreground">{eyebrow}</span>}
      <h2 className="font-display text-3xl sm:text-5xl md:text-heading leading-tight tracking-[-0.01em] text-foreground">
        {title}
      </h2>
    </div>
  );
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: React.ReactNode }) {
  return (
    <InteractiveCard>
      <Card className="h-full rounded-sm">
        <CardHeader>
          <div className="mb-2 text-deep-green dark:text-pale-green">{icon}</div>
          <CardTitle className="text-xl">{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">{description}</p>
        </CardContent>
      </Card>
    </InteractiveCard>
  );
}

function AgentCard({ name, role, description, accent }: { name: string; role: string; description: string; accent?: "bull" | "bear" }) {
  const accentClass =
    accent === "bull"
      ? "border-deep-green dark:border-pale-green/50"
      : accent === "bear"
      ? "border-coral"
      : "";

  return (
    <InteractiveCard>
      <Card className={`h-full rounded-sm ${accentClass}`}>
        <CardHeader>
          <div className="flex items-center gap-2">
            {accent === "bull" && <TrendingUp className="w-4 h-4 text-deep-green dark:text-pale-green" />}
            {accent === "bear" && <TrendingDown className="w-4 h-4 text-coral" />}
            {!accent && <Users className="w-4 h-4 text-muted-foreground" />}
            <CardTitle className="text-base">{name}</CardTitle>
          </div>
          <CardDescription className="type-mono-label text-xs">{role}</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground">{description}</p>
        </CardContent>
      </Card>
    </InteractiveCard>
  );
}

function LLMProviderCard({ name, models }: { name: string; models: string[] }) {
  const logoMap: Record<string, string> = {
    OpenAI: "/logos/openai.svg",
    Anthropic: "/logos/claude-color.svg",
    "Google Gemini": "/logos/gemini-color.svg",
    "Grok (xAI)": "/logos/grok.svg",
    DeepSeek: "/logos/deepseek-color.svg",
    "Qwen (Alibaba)": "/logos/qwen-color.svg",
  };
  const logoSrc = logoMap[name];
  // OpenAI / Grok marks are single-colour black glyphs: flip to white on dark backgrounds
  const logoClass = name === "OpenAI" || name === "Grok (xAI)" ? "object-contain dark:invert" : "object-contain";

  return (
    <InteractiveCard>
      <Card className="h-full rounded-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-sm bg-soft-stone dark:bg-secondary flex items-center justify-center flex-shrink-0">
              {logoSrc ? (
                <Image src={logoSrc} alt={`${name} logo`} width={28} height={28} className={logoClass} />
              ) : (
                <Globe className="w-5 h-5 text-muted-foreground" />
              )}
            </div>
            <CardTitle className="text-xl">{name}</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ul className="space-y-1.5">
            {models.map((model, i) => (
              <li key={i} className="flex items-center gap-2 text-xs text-muted-foreground">
                <CheckCircle2 className={`w-3.5 h-3.5 ${CHECK_ICON}`} />
                {model}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </InteractiveCard>
  );
}

function TechnicalCard({ title, features, icon }: { title: string; features: string[]; icon: React.ReactNode }) {
  return (
    <InteractiveCard>
      <Card className="h-full rounded-sm">
        <CardHeader>
          <div className="flex items-center gap-2 text-deep-green dark:text-pale-green">
            {icon}
            <CardTitle className="text-xl text-foreground">{title}</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {features.map((feature, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                <CheckCircle2 className={`w-4 h-4 mt-0.5 ${CHECK_ICON}`} />
                {feature}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </InteractiveCard>
  );
}

function WorkflowStep({ number, title, description }: { number: number; title: string; description: string }) {
  return (
    <div className="flex gap-4 items-start border-t border-border pt-4 first:border-t-0 first:pt-0">
      <div className="flex-shrink-0 w-9 h-9 rounded-xs border border-foreground flex items-center justify-center font-mono text-sm">
        {number}
      </div>
      <div>
        <h4 className="font-display text-lg mb-1 text-foreground">{title}</h4>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
