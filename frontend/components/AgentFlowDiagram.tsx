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
const ICON_DISC =
  "inline-flex items-center justify-center rounded-full bg-deep-green text-white dark:bg-pale-green dark:text-deep-green";

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
            description={t.flowDiagram.priceAndFinancials}
            color="blue"
          />
          <DataSourceCard
            icon={<Newspaper className="w-5 h-5" />}
            name="Finnhub · Marketaux · NewsAPI · GDELT"
            description={t.flowDiagram.multiSourceNews}
            color="green"
          />
          <DataSourceCard
            icon={<MessageSquare className="w-5 h-5" />}
            name="StockTwits · Reddit · Hacker News · PTT"
            description={t.flowDiagram.socialSentiment}
            color="orange"
          />
          <DataSourceCard
            icon={<BookOpen className="w-5 h-5" />}
            name="Jina AI"
            description={t.flowDiagram.fullTextExtraction}
            color="amber"
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
            icon={<BarChart3 className="w-5 h-5" />}
            description={t.flowDiagram.technicalAnalysis}
            tasks={[t.flowDiagram.rsiIndicator, t.flowDiagram.macdMomentum, t.flowDiagram.priceTrend]}
          />
          <AgentCard
            name={t.agents.social_analyst}
            icon={<MessageSquare className="w-5 h-5" />}
            description={t.flowDiagram.sentimentAnalysis}
            tasks={[t.flowDiagram.bullBearRatio, t.flowDiagram.discussionHeat, t.flowDiagram.investorConfidence]}
          />
          <AgentCard
            name={t.agents.news_analyst}
            icon={<Newspaper className="w-5 h-5" />}
            description={t.flowDiagram.newsAnalysis}
            tasks={[t.flowDiagram.multiSourceNews, t.flowDiagram.fullTextReading, t.flowDiagram.eventAssessment]}
          />
          <AgentCard
            name={t.agents.fundamentals_analyst}
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
            icon={<TrendingUp className="w-5 h-5" />}
            description={t.flowDiagram.bullishResearch}
            tasks={[t.flowDiagram.positiveFactors, t.flowDiagram.growthOpportunities, t.flowDiagram.buyReasons]}
          />
          <AgentCard
            name={t.agents.bear_researcher}
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
          icon={<Users className="w-6 h-6" />}
          description={t.flowDiagram.integrateViews}
          tasks={[t.flowDiagram.balanceArguments, t.flowDiagram.comprehensiveAdvice, t.flowDiagram.preliminaryStrategy]}
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
            icon={<ShieldAlert className="w-5 h-5" />}
            description={t.flowDiagram.highRiskReward}
            tasks={[t.flowDiagram.aggressiveStrategy, t.flowDiagram.maximizeReturns, t.flowDiagram.calculatedRisk]}
          />
          <AgentCard
            name={t.agents.neutral_debator}
            icon={<Shield className="w-5 h-5" />}
            description={t.flowDiagram.balancedRisk}
            tasks={[t.flowDiagram.prudentStrategy, t.flowDiagram.riskBalance, t.flowDiagram.rationalDecision]}
          />
          <AgentCard
            name={t.agents.conservative_debator}
            icon={<ShieldCheck className="w-5 h-5" />}
            description={t.flowDiagram.lowRiskVol}
            tasks={[t.flowDiagram.conservativeStrategy, t.flowDiagram.capitalProtection, t.flowDiagram.riskReduction]}
          />
        </div>
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.riskDebate} color="red" />

      {/* Risk Manager */}
      <div className="max-w-md mx-auto">
        <ManagerCard
          name={t.flowDiagram.riskManager}
          icon={<Shield className="w-6 h-6" />}
          description={t.flowDiagram.integrateRisk}
          tasks={[t.flowDiagram.riskRating, t.flowDiagram.stopLossSettings, t.flowDiagram.finalRiskControl]}
        />
      </div>

      {/* Arrow */}
      <FlowArrow label={t.flowDiagram.finalDecision} color="green" />

      {/* Trader */}
      <div className="max-w-md mx-auto">
        <TraderCard
          name={t.flowDiagram.trader}
          icon={<Target className="w-7 h-7" />}
          description={t.flowDiagram.executeTrade}
          outputs={[t.flowDiagram.tradeSignal, t.flowDiagram.targetPrice, t.flowDiagram.tradeQuantity, t.flowDiagram.riskParams]}
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
  color,
}: {
  icon: React.ReactNode;
  name: string;
  description: string;
  color: "blue" | "orange" | "green" | "amber";
}) {
  const colorClasses = {
    blue: "  border-border ",
    orange: "  border-coral/50 ",
    green: "  border-deep-green/30 dark:border-pale-green/30 ",
    amber: "  border-coral/50 ",
  };

  return (
    <Card className={`p-3 hover-lift animate-slide-up border-2 ${colorClasses[color]}`}>
      <div className="flex flex-col items-center justify-center">
        <div className={`${ICON_DISC} w-10 h-10 mb-2`}>
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
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  tasks: string[];
}) {
  return (
    <Card className="p-4 hover-lift animate-scale-up relative overflow-hidden group">
      
      <div className="relative z-10">
        <div className="text-center mb-3">
          <div className={`${ICON_DISC} w-10 h-10 mb-2`}>
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
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  tasks: string[];
}) {
  return (
    <Card className={`p-5 hover-lift relative overflow-hidden border-2 border-border`}>
      <div className="text-center mb-3">
        <div className={`${ICON_DISC} w-12 h-12 mb-2`}>
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

function TraderCard({
  name,
  icon,
  description,
  outputs,
}: {
  name: string;
  icon: React.ReactNode;
  description: string;
  outputs: string[];
}) {
  return (
    <Card className={`p-6 hover-lift relative overflow-hidden border-2 border-foreground`}>
            <div className="relative z-10">
        <div className="text-center mb-4">
          <div className={`${ICON_DISC} w-14 h-14 mb-3`}>
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
