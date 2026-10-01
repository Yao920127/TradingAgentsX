# Style: Tech Minimal (S01)

## Overview
- **ID**: S01
- **Name**: Tech Minimal
- **Industries**: Tech, Professional
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: Neutral grays with a single accent color. Clean backgrounds, subtle borders.
- **Typography**: System fonts or geometric sans-serif. Clean hierarchy with consistent weights.
- **Radius Policy**: Small to medium radius (4-8px). Consistent across components.
- **Shadow Policy**: Subtle elevation shadows. Minimal depth.
- **Border Language**: Thin, subtle borders. Low contrast.
- **Patterns**: None. Pure flat surfaces.
- **Motion**: Subtle, quick transitions (150-200ms). Ease-out curves.

## Rules
### Do
- Use clean lines and ample whitespace
- Keep typography simple and readable
- Use subtle animations
- Maintain consistent spacing

### Don't
- Don't use excessive decorations
- Don't overcrowd the layout
- Don't use too many colors
- Don't use heavy shadows

---

## Complete Prompt

# Tech Minimal SaaS Landing Page Prompt (S01)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S01 Tech Minimal** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S01 — Tech Minimal
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

## Style DNA (S01 – Tech Minimal)

### Style Seeds
- **Palette strategy:** Neutral grays with a single accent color. Clean backgrounds, subtle borders.
- **Typography:** System fonts or geometric sans-serif. Clean hierarchy with consistent weights.
- **Radius policy:** Small to medium radius (4-8px). Consistent across components.
- **Shadow policy:** Subtle elevation shadows. Minimal depth.
- **Border language:** Thin, subtle borders. Low contrast.
- **Patterns/textures:** None. Pure flat surfaces.
- **Motion:** Subtle, quick transitions (150-200ms). Ease-out curves.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S01"
    style_name: "Tech Minimal"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F8F9FA"
    text:
      primary: "#1A1A1A"
      secondary: "#6B7280"
      muted: "#9CA3AF"
    brand:
      primary: "#3B82F6"
      accent: "#10B981"
    border:
      strong: "#E5E7EB"
      subtle: "#F3F4F6"
    state:
      success: "#10B981"
      warning: "#F59E0B"
      error: "#EF4444"
    focus:
      ring: "#3B82F6"
  radius:
    none: 0
    sm: 4
    md: 8
    lg: 12
  border:
    width:
      hairline: 1
      medium: 2
      strong: 3
  shadow:
    sm: "0 1px 2px rgba(0,0,0,0.05)"
    md: "0 4px 6px rgba(0,0,0,0.07)"
  layout:
    container:
      content: 1120
      wide: 1280
    grid:
      desktop: 12
      tablet: 8
      mobile: 4
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 150, normal: 200 }
    easing: ease-out
  typography:
    font:
      sans: { primary: "Inter", fallback: ["system-ui", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 600, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 600, tracking: -0.01 }
      h3: { size: 28, line: 36, weight: 600, tracking: -0.005 }
      body: { size: 16, line: 24, weight: 450, tracking: 0 }
      small: { size: 14, line: 20, weight: 450, tracking: 0 }
    measure: { hero_max: "48ch", body_max: "72ch" }
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
