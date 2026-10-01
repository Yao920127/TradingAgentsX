# Style: Bauhaus Modernism (S06)

## Overview
- **ID**: S06
- **Name**: Bauhaus Modernism
- **Industries**: Creative, Professional
- **Category**: Artistic

## Design DNA
- **Palette Strategy**: Primary colors only. Red, blue, yellow. Bold contrasts.
- **Typography**: Geometric sans-serif. Bold. Grid-aligned.
- **Radius Policy**: Mixed. Circles and rectangles.
- **Shadow Policy**: None or hard shadows.
- **Border Language**: Thick black borders. Geometric.
- **Patterns**: Geometric shapes. Circles, squares, triangles.
- **Motion**: Linear transitions. No easing.

## Rules
### Do
- Use bold geometry and rules
- Keep copy concise
- Treat layout like a poster
- Use primary colors for impact

### Don't
- Don't use gradients or glassmorphism
- Don't over-animate
- Don't round everything
- Don't use decorative fonts

---

## Complete Prompt

# Bauhaus Modernism SaaS Landing Page Prompt (S06)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S06 Bauhaus Modernism** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S06 — Bauhaus Modernism
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

## Style DNA (S06 – Bauhaus Modernism)

### Style Seeds
- **Palette strategy:** Primary colors only. Red, blue, yellow. Bold contrasts.
- **Typography:** Geometric sans-serif. Bold. Grid-aligned.
- **Radius policy:** Mixed. Circles and rectangles.
- **Shadow policy:** None or hard shadows.
- **Border language:** Thick black borders. Geometric.
- **Patterns/textures:** Geometric shapes. Circles, squares, triangles.
- **Motion:** Linear transitions. No easing.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S06"
    style_name: "Bauhaus Modernism"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F5F5F5"
    text:
      primary: "#000000"
      secondary: "#333333"
      muted: "#666666"
    brand:
      primary: "#FF0000"
      secondary: "#0000FF"
      accent: "#FFFF00"
    border:
      strong: "#000000"
      subtle: "#E0E0E0"
    state:
      success: "#0000FF"
      warning: "#FFFF00"
      error: "#FF0000"
    focus:
      ring: "#000000"
  radius:
    none: 0
    sm: 0
    md: 0
    circle: 9999
  border:
    width:
      hairline: 2
      medium: 4
      strong: 6
  shadow:
    none: none
    hard: "4px 4px 0 #000000"
  layout:
    container: { content: 1120, wide: 1280 }
    grid: { desktop: 12, tablet: 8, mobile: 4 }
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 100, normal: 200 }
    easing: linear
  typography:
    font:
      sans: { primary: "Helvetica Now", fallback: ["Bebas Neue", "Arial", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 700, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 700, tracking: -0.01 }
      h3: { size: 28, line: 36, weight: 700, tracking: -0.005 }
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
