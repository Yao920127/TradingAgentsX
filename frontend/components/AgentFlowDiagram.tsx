/**
 * Agent Flow Diagram Component
 * Visualizes the complete data flow through all 12 agents
 */
"use client";

import { Card } from "@/components/ui/card";
import { 
  ArrowDown, 
  Database, 
  MessageSquare, 
  Newspaper, 
  DollarSign, 
  TrendingUp,
  TrendingDown,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Users,
  Target,
  BarChart3,
  FileText,
  BookOpen
} from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

// Solid disc behind every flow icon so the white glyph is always visible.
const ICON_DISC_BASE = "inline-flex items-center justify-center rounded-full";
const ICON_DISC = `${ICON_DISC_BASE} bg-deep-green text-white dark:bg-pale-green dark:text-deep-green`;

// One accent per agent: coloured border + icon disc, card background stays neutral.
const CARD_TONES = {
  sky: {
    card: "border-sky-400 dark:border-sky-400/70",
    disc: "bg-sky-600 text-white dark:bg-sky-300 dark:text-sky-950",
  },
  violet: {
    card: "border-violet-400 dark:border-violet-400/70",
    disc: "bg-violet-600 text-white dark:bg-violet-300 dark:text-violet-950",
  },
  amber: {
    card: "border-amber-400 dark:border-amber-400/70",
    disc: "bg-amber-600 text-white dark:bg-amber-300 dark:text-amber-950",
  },
  emerald: {
    card: "border-emerald-500 dark:border-emerald-400/70",
    disc: "bg-emerald-700 text-white dark:bg-emerald-300 dark:text-emerald-950",
  },
  teal: {
    card: "border-teal-400 dark:border-teal-400/70",
    disc: "bg-teal-700 text-white dark:bg-teal-300 dark:text-teal-950",
  },
  lime: {
    card: "border-lime-500 dark:border-lime-400/70",
    disc: "bg-lime-700 text-white dark:bg-lime-300 dark:text-lime-950",
  },
  red: {
    card: "border-red-400 dark:border-red-400/70",
    disc: "bg-red-600 text-white dark:bg-red-300 dark:text-red-950",
  },
  indigo: {
    card: "border-indigo-400 dark:border-indigo-400/70",
    disc: "bg-indigo-600 text-white dark:bg-indigo-300 dark:text-indigo-950",
  },
  orange: {
    card: "border-orange-400 dark:border-orange-400/70",
    disc: "bg-orange-600 text-white dark:bg-orange-300 dark:text-orange-950",
  },
  slate: {
    card: "border-slate-400 dark:border-slate-400/70",
    disc: "bg-slate-600 text-white dark:bg-slate-300 dark:text-slate-950",
  },
  blue: {
    card: "border-blue-400 dark:border-blue-400/70",
    disc: "bg-blue-600 text-white dark:bg-blue-300 dark:text-blue-950",
  },
  rose: {
    card: "border-rose-400 dark:border-rose-400/70",
    disc: "bg-rose-600 text-white dark:bg-rose-300 dark:text-rose-950",
  },
  yellow: {
    card: "border-yellow-400 dark:border-yellow-400/70",
    disc: "bg-yellow-500 text-yellow-950 dark:bg-yellow-300",
  },
} as const;

type CardTone = keyof typeof CARD_TONES;

function toneStyles(tone: CardTone | undefined, fallbackCard: string) {
  if (!tone) return { card: fallbackCard, disc: ICON_DISC };
  return { card: CARD_TONES[tone].card, disc: `${ICON_DISC_BASE} ${CARD_TONES[tone].disc}` };
}

export function AgentFlowDiagram() {
  const { t } = useLanguage();

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6">
      {/* Data Sources Layer */}
      <div>
        <h3 className="text-center text-sm font-semibold text-muted-foreground mb-4">
          📥 {t.flowDiagram.layer1}
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <DataSourceCard
            icon={<Database className="w-5 h-5" />}
            name="yfinance / FinMind / Alpha Vantage"
            tone="sky"
            description={t.flowDiagram.priceAndFinancials}
          />
          <DataSourceCard
            icon={<Newspaper className="w-5 h-5" />}
            name="Finnhub · Marketaux · NewsAPI · GDELT"
            tone="amber"
            description={t.flowDiagram.multiSourceNews}
          />
          <DataSourceCard
            icon={<MessageSquare className="w-5 h-5" />}
            name="StockTwits · Reddit · Hacker News · PTT"
            tone="violet"
            description={t.flowDiagram.socialSentiment}
          />
          <DataSourceCard
            icon={<BookOpen className="w-5 h-5" />}
            name="Jina AI"
            tone="orange"
            description={t.flowDiagram.fullTextExtraction}
          />
        </div>
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.dataFetch} color="blue" />

      {/* Analysts Layer - 4 agents */}
      <div>
        <h3 className="text-center text-sm font-semibold text-muted-foreground mb-4">
          🤖 {t.flowDiagram.layer2}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <AgentCard
            name={t.agents.market_analyst}
            tone="sky"
            icon={<BarChart3 className="w-5 h-5" />}
            description={t.flowDiagram.technicalAnalysis}
            tasks={[t.flowDiagram.rsiIndicator, t.flowDiagram.macdMomentum, t.flowDiagram.priceTrend]}
          />
          <AgentCard
            name={t.agents.social_analyst}
            tone="violet"
            icon={<MessageSquare className="w-5 h-5" />}
            description={t.flowDiagram.sentimentAnalysis}
            tasks={[t.flowDiagram.bullBearRatio, t.flowDiagram.discussionHeat, t.flowDiagram.investorConfidence]}
          />
          <AgentCard
            name={t.agents.news_analyst}
            tone="amber"
            icon={<Newspaper className="w-5 h-5" />}
            description={t.flowDiagram.newsAnalysis}
            tasks={[t.flowDiagram.multiSourceNews, t.flowDiagram.fullTextReading, t.flowDiagram.eventAssessment]}
          />
          <AgentCard
            name={t.agents.fundamentals_analyst}
            tone="emerald"
            icon={<DollarSign className="w-5 h-5" />}
            description={t.flowDiagram.fundamentalsAnalysis}
            tasks={[t.flowDiagram.financialAnalysis, t.flowDiagram.valuationMetrics, t.flowDiagram.profitEvaluation]}
          />
        </div>
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.reportIntegration} color="amber" />

      {/* Report Summarizer */}
      <div className="max-w-md mx-auto">
        <ManagerCard
          name={t.agents.report_summarizer}
          tone="teal"
          icon={<FileText className="w-6 h-6" />}
          description={t.flowDiagram.summarizerDesc}
          tasks={[t.flowDiagram.keepKeyData, t.flowDiagram.structuredSummary, t.flowDiagram.saveTokens]}
        />
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.summaryHandoff} color="amber" />

      {/* Researchers Layer - 2 agents */}
      <div>
        <h3 className="text-center text-sm font-semibold text-muted-foreground mb-4">
          🔍 {t.flowDiagram.layer3}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
          <AgentCard
            name={t.agents.bull_researcher}
          tone="lime"
            icon={<TrendingUp className="w-5 h-5" />}
            description={t.flowDiagram.bullishResearch}
            tasks={[t.flowDiagram.positiveFactors, t.flowDiagram.growthOpportunities, t.flowDiagram.buyReasons]}
          />
          <AgentCard
            name={t.agents.bear_researcher}
          tone="red"
            icon={<TrendingDown className="w-5 h-5" />}
            description={t.flowDiagram.bearishResearch}
            tasks={[t.flowDiagram.negativeFactors, t.flowDiagram.riskAssessment, t.flowDiagram.sellReasons]}
          />
        </div>
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.researchPrep} color="green" />

      {/* Research Manager */}
      <div className="max-w-md mx-auto">
        <ManagerCard
          name={t.flowDiagram.researchManager}
          tone="indigo"
          icon={<Users className="w-6 h-6" />}
          description={t.flowDiagram.integrateViews}
          tasks={[t.flowDiagram.balanceArguments, t.flowDiagram.comprehensiveAdvice, t.flowDiagram.preliminaryStrategy]}
        />
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.handoffPlan} color="green" />

      {/* Trader: proposes only — the Risk Manager makes the final call */}
      <div className="max-w-md mx-auto">
        <ManagerCard
          name={t.flowDiagram.trader}
          tone="yellow"
          icon={<Target className="w-6 h-6" />}
          description={t.flowDiagram.proposeTrade}
          tasks={[t.flowDiagram.tradeSignal, t.flowDiagram.targetPrice, t.flowDiagram.tradeQuantity]}
        />
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.riskDebate} color="orange" />

      {/* Risk Debators Layer - 3 agents */}
      <div>
        <h3 className="text-center text-sm font-semibold text-muted-foreground mb-4">
          ⚖️ {t.flowDiagram.layer4}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <AgentCard
            name={t.agents.aggressive_debator}
          tone="orange"
            icon={<ShieldAlert className="w-5 h-5" />}
            description={t.flowDiagram.highRiskReward}
            tasks={[t.flowDiagram.aggressiveStrategy, t.flowDiagram.maximizeReturns, t.flowDiagram.calculatedRisk]}
          />
          <AgentCard
            name={t.agents.neutral_debator}
          tone="slate"
            icon={<Shield className="w-5 h-5" />}
            description={t.flowDiagram.balancedRisk}
            tasks={[t.flowDiagram.prudentStrategy, t.flowDiagram.riskBalance, t.flowDiagram.rationalDecision]}
          />
          <AgentCard
            name={t.agents.conservative_debator}
          tone="blue"
            icon={<ShieldCheck className="w-5 h-5" />}
            description={t.flowDiagram.lowRiskVol}
            tasks={[t.flowDiagram.conservativeStrategy, t.flowDiagram.capitalProtection, t.flowDiagram.riskReduction]}
          />
        </div>
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.finalDecision} color="red" />

      {/* Risk Manager: makes the final BUY/SELL/HOLD decision */}
      <div className="max-w-md mx-auto">
        <FinalDecisionCard
          name={t.flowDiagram.riskManager}
          tone="rose"
          icon={<Shield className="w-7 h-7" />}
          description={t.flowDiagram.integrateRisk}
          outputs={[t.flowDiagram.tradeSignal, t.flowDiagram.riskRating, t.flowDiagram.stopLossSettings, t.flowDiagram.finalRiskControl]}
        />
      </div>

      {/* Final Arrow */}
      <FlowArrow label={t.flowDiagram.generateReport} color="blue" />

      {/* Output Layer */}
      <div>
        <h3 className="text-center text-sm font-semibold text-muted-foreground mb-4">
          📊 {t.flowDiagram.finalOutput}
        </h3>
        <Card className="border-2 border-dashed border-border p-6">
          <div className="text-center mb-4">
            <div className={`${ICON_DISC} w-16 h-16 mb-3`}>
              <BarChart3 className="w-8 h-8" />
            </div>
            <h4 className="font-bold text-lg mb-2 gradient-text-primary">{t.flowDiagram.completeReportSet}</h4>
            <p className="text-sm text-muted-foreground ">
              {t.flowDiagram.comprehensiveSupport}
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <ReportSection
              title={t.flowDiagram.analystReports}
              items={[t.flowDiagram.technicalReport, t.flowDiagram.sentimentReport, t.flowDiagram.newsReport, t.flowDiagram.fundamentalsReport]}
              color="blue"
            />
            <ReportSection
              title={t.flowDiagram.researchReports}
              items={[t.flowDiagram.bullReport, t.flowDiagram.bearReport, t.flowDiagram.researchManagerReport]}
              color="green"
            />
            <ReportSection
              title={t.flowDiagram.riskTrading}
              items={[t.flowDiagram.aggressiveEval, t.flowDiagram.balancedEval, t.flowDiagram.conservativeEval, t.flowDiagram.riskManagerReport, t.flowDiagram.finalTradeDecision]}
              color="red"
            />
          </div>
        </Card>
      </div>
    </div>
  );
}

function DataSourceCard({
  icon,
  name,
  description,
  tone,
}: {
  icon: React.ReactNode;
  name: string;
  description: string;
  tone?: CardTone;
}) {
  const styles = toneStyles(tone, "border-border");
  return (
    <Card className={`p-3 hover-lift animate-slide-up border-2 ${styles.card}`}>
      <div className="flex flex-col items-center justify-center">
        <div className={`${styles.disc} w-10 h-10 mb-2`}>
          {icon}
        </div>
        <h4 className="font-semibold text-xs mb-0.5 text-center">{name}</h4>
        <p className="text-xs text-muted-foreground text-center">{description}</p>
      </div>
    </Card>
  );
}

function AgentCard({
  name,
  icon,
  description,
  tasks,
  tone,
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  tasks: string[];
  tone?: CardTone;
}) {
  const styles = toneStyles(tone, "");
  return (
    <Card className={`p-4 hover-lift animate-scale-up relative overflow-hidden group border-2 ${styles.card}`}>
      
      <div className="relative z-10">
        <div className="text-center mb-3">
          <div className={`${styles.disc} w-10 h-10 mb-2`}>
            {icon}
          </div>
          <h4 className="font-bold text-sm mb-0.5">{name}</h4>
          <p className="text-xs text-muted-foreground ">{description}</p>
        </div>

        <div className="space-y-0.5">
          {tasks.map((task, index) => (
            <div key={index} className="flex items-start text-xs text-muted-foreground ">
              <span className="mr-1">•</span>
              <span>{task}</span>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

function ManagerCard({
  name,
  icon,
  description,
  tasks,
  tone,
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  tasks: string[];
  tone?: CardTone;
}) {
  const styles = toneStyles(tone, "border-border");
  return (
    <Card className={`p-5 hover-lift relative overflow-hidden border-2 ${styles.card}`}>
      <div className="text-center mb-3">
        <div className={`${styles.disc} w-12 h-12 mb-2`}>
          {icon}
        </div>
        <h4 className="font-bold text-base mb-1">{name}</h4>
        <p className="text-sm text-muted-foreground ">{description}</p>
      </div>

      <div className="space-y-1">
        {tasks.map((task, index) => (
          <div key={index} className="flex items-start text-sm text-foreground ">
            <span className="mr-2">✓</span>
            <span>{task}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}

function FinalDecisionCard({
  name,
  icon,
  description,
  outputs,
  tone,
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  outputs: string[];
  tone?: CardTone;
}) {
  const styles = toneStyles(tone, "border-foreground");
  return (
    <Card className={`p-6 hover-lift relative overflow-hidden border-2 ${styles.card}`}>
            <div className="relative z-10">
        <div className="text-center mb-4">
          <div className={`${styles.disc} w-14 h-14 mb-3`}>
            {icon}
          </div>
          <h4 className="font-bold text-lg mb-1 gradient-text-primary">{name}</h4>
          <p className="text-sm text-muted-foreground font-medium">{description}</p>
        </div>

        <div className="space-y-2 bg-muted p-3 rounded-lg">
          <div className="text-xs font-semibold text-foreground mb-2">最終輸出:</div>
          {outputs.map((output, index) => (
            <div key={index} className="flex items-start text-sm font-medium text-foreground ">
              <span className="mr-2 text-deep-green dark:text-pale-green ">▸</span>
              <span>{output}</span>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

function FlowArrow({ label, color }: { label: string; color: string }) {
  const colorClasses = {
    blue: "text-deep-green dark:text-pale-green ",
    amber: "text-foreground ",
    green: "text-deep-green dark:text-pale-green ",
    orange: "text-foreground ",
    red: "text-destructive ",
  };

  return (
    <div className="flex justify-center">
      <div className="flex flex-col items-center">
        <div className="text-xs text-muted-foreground mb-1 font-medium">{label}</div>
        <ArrowDown className={`w-7 h-7 ${colorClasses[color as keyof typeof colorClasses]} motion-safe:animate-pulse`} />
      </div>
    </div>
  );
}

function ReportSection({
  title,
  items,
  color,
}: {
  title: string;
  items: string[];
  color: "blue" | "green" | "red";
}) {
  const colorClasses = {
    blue: "bg-secondary  border-border ",
    green: "bg-pale-green dark:bg-deep-green/40  border-deep-green/30 dark:border-pale-green/30 ",
    red: "bg-coral-soft/20 dark:bg-destructive/15  border-destructive/30 ",
  };

  return (
    <div className={`p-3 rounded-lg border ${colorClasses[color]}`}>
      <h5 className="font-semibold text-xs mb-2 text-foreground ">{title}</h5>
      <div className="space-y-1">
        {items.map((item, index) => (
          <div key={index} className="text-xs text-muted-foreground flex items-start">
            <span className="mr-1">•</span>
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
