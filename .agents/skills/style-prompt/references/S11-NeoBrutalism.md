# Style: Neo-Brutalism (S11)

## Overview
- **ID**: S11
- **Name**: Neo-Brutalism
- **Industries**: Creative, Tech
- **Category**: Artistic

## Design DNA
- **Palette Strategy**: High contrast, vibrant colors. Stark black and white base with bold primary accents.
- **Typography**: Bold, oversized sans-serif (e.g., Archivo, Lexend). Strong character.
- **Radius Policy**: Zero or very minimal (0-4px). Hard edges.
- **Shadow Policy**: Hard, offset black shadows (no blur). Deep contrast.
- **Border Language**: Thick black borders (4-8px). High visibility.
- **Patterns**: None. Pure solid colors.
- **Motion**: Instant or very fast linear transitions.

## Rules
### Do
- Use thick black borders
- Apply hard offset shadows
- Use vibrant, high-saturation colors
- Emphasize oversized typography

### Don't
- Don't use soft gradients or blurs
- Don't use rounded corners
- Don't use subtle colors
- Don't use delicate fonts

---

## Complete Prompt

# Neo-Brutalism SaaS Landing Page Prompt (S11)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S11 Neo-Brutalism** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S11 — Neo-Brutalism
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

## Style DNA (S11 – Neo-Brutalism)

### Style Seeds
- **Palette strategy:** High contrast, vibrant colors. Stark black and white base with bold primary accents.
- **Typography:** Bold, oversized sans-serif (e.g., Archivo, Lexend). Strong character.
- **Radius policy:** Zero or very minimal (0-4px). Hard edges.
- **Shadow policy:** Hard, offset black shadows (no blur). Deep contrast.
- **Border language:** Thick black borders (4-8px). High visibility.
- **Patterns/textures:** None. Pure solid colors.
- **Motion:** Instant or very fast linear transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S11"
    style_name: "Neo-Brutalism"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#F3F3F3"
    text:
      primary: "#000000"
      secondary: "#000000"
      muted: "#555555"
    brand:
      primary: "#A3E635"
      secondary: "#818CF8"
      accent: "#FB7185"
    border:
      strong: "#000000"
      subtle: "#000000"
    focus:
      ring: "#000000"
  radius:
    none: 0
    sm: 2
    md: 4
  border:
    width:
      hairline: 2
      medium: 4
      strong: 6
  shadow:
    hard: "4px 4px 0 #000000"
    extreme: "8px 8px 0 #000000"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 100, normal: 200 }
    easing: "linear"
  typography:
    font:
      sans: { primary: "Lexend", fallback: ["Archivo", "system-ui"] }
    scale:
      h1: { size: 60, line: 64, weight: 800, tracking: -0.04 }
      h2: { size: 44, line: 48, weight: 800, tracking: -0.02 }
      body: { size: 18, line: 26, weight: 500, tracking: 0 }
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
