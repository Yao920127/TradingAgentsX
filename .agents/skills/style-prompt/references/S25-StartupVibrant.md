# Style: Startup Vibrant (S25)

## Overview
- **ID**: S25
- **Name**: Startup Vibrant
- **Industries**: Tech, Professional
- **Category**: Corporate

## Design DNA
- **Palette Strategy**: Vibrant startup design, energetic and modern. Bold accents.
- **Typography**: Modern sans-serif (Inter). Clean and approachable.
- **Radius Policy**: Medium rounding (8-12px).
- **Shadow Policy**: Soft, modern elevation.
- **Border Language**: Subtle borders for structural definition.
- **Patterns**: Modern geometric motifs.
- **Motion**: Energetic, fast transitions (150-250ms).

## Rules
### Do
- Use energetic accent colors
- Keep it fast-looking and modern
- Use consistent medium rounding
- Maintain clean, modern typography

### Don't
- Don't use dull, corporate grays
- Don't use complex serif fonts
- Don't use slow, heavy animations
- Don't overcrowd the layout

---

## Complete Prompt

# Startup Vibrant SaaS Landing Page Prompt (S25)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S25 Startup Vibrant** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S25 — Startup Vibrant
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

## Style DNA (S25 – Startup Vibrant)

### Style Seeds
- **Palette strategy:** Vibrant startup design, energetic and modern. Bold accents.
- **Typography:** Modern sans-serif (Inter). Clean and approachable.
- **Radius policy:** Medium rounding (8-12px).
- **Shadow policy:** Soft, modern elevation.
- **Border language:** Subtle borders for structural definition.
- **Patterns/textures:** Modern geometric motifs.
- **Motion:** Energetic, fast transitions (150-250ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S25"
    style_name: "Startup Vibrant"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F3F4F6"
    text:
      primary: "#111827"
      secondary: "#4B5563"
      muted: "#9CA3AF"
    brand:
      primary: "#3B82F6"
      secondary: "#10B981"
      accent: "#8B5CF6"
    border:
      strong: "#E5E7EB"
      subtle: "#F9FAFB"
    focus:
      ring: "#3B82F6"
  radius:
    none: 0
    sm: 4
    md: 8
    lg: 12
    xl: 20
    pill: 9999
  border:
    width: { hairline: 1, medium: 1, strong: 2 }
  shadow:
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 150, normal: 250, slow: 400 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Inter", fallback: ["system-ui", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 800, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 800, tracking: -0.01 }
      body: { size: 16, line: 24, weight: 400, tracking: 0 }
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
