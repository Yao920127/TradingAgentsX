# Style: Brutalist (S04)

## Overview
- **ID**: S04
- **Name**: Brutalist
- **Industries**: Creative, Tech
- **Category**: Artistic

## Design DNA
- **Palette Strategy**: High contrast black and white. Raw, unrefined color choices. Occasional primary yellow or red as accents.
- **Typography**: Heavyweight sans-serif (e.g., Helvetica, Archivo Black). Large, overlapping headlines. Monospaced secondary text.
- **Radius Policy**: Strict zero radius (0px). Everything is sharp and rectangular.
- **Shadow Policy**: Hard, opaque drop shadows (no blur, 100% opacity). Multi-layered shadows create depth.
- **Border Language**: Thick, prominent black borders (1-3px) on all containers and buttons.
- **Patterns**: High contrast grid lines, raw material textures.
- **Motion**: Instant transitions. No easing or very aggressive, fast cubic-beziers.

## Rules
### Do
- Use thick black borders
- Prioritize raw typography over imagery
- Keep everything 100% sharp
- Use high-contrast black/white layouts

### Don't
- Don't use border-radius
- Don't use soft shadows or blurs
- Don't use subtle gradients
- Don't use delicate or script fonts

---

## Complete Prompt

# Brutalist SaaS Landing Page Prompt (S04)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S04 Brutalist** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S04 — Brutalist
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

## Style DNA (S04 – Brutalist)

### Style Seeds
- **Palette strategy:** High contrast black and white. Raw, unrefined color choices. Occasional primary yellow or red as accents.
- **Typography:** Heavyweight sans-serif (e.g., Helvetica, Archivo Black). Large, overlapping headlines. Monospaced secondary text.
- **Radius policy:** Strict zero radius (0px). Everything is sharp and rectangular.
- **Shadow policy:** Hard, opaque drop shadows (no blur, 100% opacity). Multi-layered shadows create depth.
- **Border language:** Thick, prominent black borders (1-3px) on all containers and buttons.
- **Patterns/textures:** High contrast grid lines, raw material textures.
- **Motion:** Instant transitions. No easing or very aggressive, fast cubic-beziers.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S04"
    style_name: "Brutalist"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#EAEAEA"
    text:
      primary: "#000000"
      secondary: "#1A1A1A"
      muted: "#666666"
    brand:
      primary: "#000000"
      accent: "#FF3E00"
    border:
      strong: "#000000"
      subtle: "#1A1A1A"
    state:
      success: "#000000"
      warning: "#FF3E00"
      error: "#000000"
    focus:
      ring: "#000000"
  radius:
    none: 0
    sm: 0
    md: 0
    lg: 0
  border:
    width:
      hairline: 1
      medium: 2
      strong: 4
  shadow:
    hard: "4px 4px 0 #000000"
    extreme: "8px 8px 0 #000000"
  layout:
    container:
      content: 1120
      wide: 1400
    grid:
      desktop: 12
      tablet: 8
      mobile: 4
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 100, normal: 200 }
    easing: "cubic-bezier(0,0,1,1)"
  typography:
    font:
      sans: { primary: "Archivo Black", fallback: ["Helvetica", "Arial", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 60, line: 64, weight: 900, tracking: -0.04 }
      h2: { size: 44, line: 48, weight: 900, tracking: -0.02 }
      h3: { size: 32, line: 36, weight: 900, tracking: -0.01 }
      body: { size: 18, line: 26, weight: 500, tracking: 0 }
      small: { size: 14, line: 20, weight: 500, tracking: 0 }
    measure: { hero_max: "44ch", body_max: "64ch" }
  spacing:
    base: 8
    section_py: { mobile: [64, 80], desktop: [112, 128] }
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
