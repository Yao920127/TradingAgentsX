# Style: Corporate Clean (S09)

## Overview
- **ID**: S09
- **Name**: Corporate Clean
- **Industries**: Professional
- **Category**: Corporate

## Design DNA
- **Palette Strategy**: Clean, professional palette. Deep blues, crisp whites, and trustworthy accents.
- **Typography**: Highly readable sans-serif (e.g., Inter, Roboto). Clear hierarchy for corporate trust.
- **Radius Policy**: Conservative rounding (4-6px). Sharp enough for professionalism, soft enough for modern tech.
- **Shadow Policy**: Subtle, professional elevation. No heavy glows.
- **Border Language**: Refined, thin gray borders to define structure.
- **Patterns**: Subtle geometric patterns or none at all.
- **Motion**: Polished, standard easing (ease-in-out). Professional delivery.

## Rules
### Do
- Use whitespace effectively
- Keep palette professional (Blue/Gray/White)
- Ensure high legibility
- Use consistent spacing and grids

### Don't
- Don't use playful/clashing colors
- Don't use rounded corners excessively
- Don't use decorative fonts
- Don't over-animate transitions

---

## Complete Prompt

# Corporate Clean SaaS Landing Page Prompt (S09)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S09 Corporate Clean** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S09 — Corporate Clean
- **Industry:** SaaS
- **Use:** Full Landing Page

## Assumptions
- Product name placeholder: **[Automatic naming]**
- Core value prop placeholder: **[One-line Value Proposition]**
- Primary CTA: **Start free trial**
- Secondary CTA: **Book a demo**
- Target audience: **B2B teams and developers**
- No real metrics, certifications, or customer logos are claimed; all proof uses placeholders
- Target stack: **React + Next.js (App Router) + TypeScript + Tailwind CSS** using **CSS variables** for theming

---

## Style DNA (S09 – Corporate Clean)

### Style Seeds
- **Palette strategy:** Clean, professional palette. Deep blues, crisp whites, and trustworthy accents.
- **Typography:** Highly readable sans-serif (e.g., Inter, Roboto). Clear hierarchy for corporate trust.
- **Radius policy:** Conservative rounding (4-6px). Sharp enough for professionalism, soft enough for modern tech.
- **Shadow policy:** Subtle, professional elevation. No heavy glows.
- **Border language:** Refined, thin gray borders to define structure.
- **Patterns/textures:** Subtle geometric patterns or none at all.
- **Motion:** Polished, standard easing (ease-in-out). Professional delivery.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S09"
    style_name: "Corporate Clean"
    industry: "Enterprise SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F9FAFB"
    text:
      primary: "#111827"
      secondary: "#374151"
      muted: "#6B7280"
    brand:
      primary: "#1E40AF"
      accent: "#3B82F6"
    border:
      strong: "#D1D5DB"
      subtle: "#F3F4F6"
    state: { success: "#059669", warning: "#D97706", error: "#DC2626" }
    focus: { ring: "#2563EB" }
  radius:
    none: 0
    sm: 4
    md: 6
    lg: 8
  border:
    width: { hairline: 1, medium: 1, strong: 2 }
  shadow:
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
  layout:
    container: { content: 1120, wide: 1280 }
    grid: { desktop: 12, tablet: 8, mobile: 4 }
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 150, normal: 300 }
    easing: ease-in-out
  typography:
    font:
      sans: { primary: "Inter", fallback: ["system-ui", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["monospace"] }
    scale:
      h1: { size: 48, line: 56, weight: 700, tracking: -0.02 }
      h2: { size: 36, line: 44, weight: 700, tracking: -0.01 }
      h3: { size: 24, line: 32, weight: 600, tracking: 0 }
      body: { size: 16, line: 24, weight: 400, tracking: 0 }
      small: { size: 14, line: 20, weight: 400, tracking: 0 }
  spacing:
    base: 8
    section_py: { mobile: [64, 80], desktop: [96, 128] }
```

---

## Deliverables
- Full hero section with high-impact product visualization
- Multi-column features grid with icon/illustration slots
- Social proof/customer logo strip (using placeholders)
- Pricing table with monthly/annual toggle
- FAQ accordion system
- Final conversion CTA module
- Responsive footer with site map

---

## Accessibility & Responsive
- WCAG AA contrast
- Visible focus rings
- Reduced motion support
- Touch targets ≥ 44px
- Mobile-first layout

---

## Engineering Notes
- CSS variables for all tokens
- Tailwind config mapping tokens
- Use semantic HTML5 elements
- Implement responsive design with mobile-first approach
- Ensure all interactive elements are keyboard accessible
- Include loading states and error handling

---

## Acceptance Checklist
- Clear hierarchy and visual discipline
- Primary CTA visible above the fold
- No fake metrics or certifications
- Trust modules included
- Fully responsive
- Accessible by keyboard
