# Style: Gothic (S15)

## Overview
- **ID**: S15
- **Name**: Gothic
- **Industries**: Lifestyle, Creative
- **Category**: Artistic

## Design DNA
- **Palette Strategy**: High contrast dark palette. Black, deep purples, and blood reds.
- **Typography**: Blackletter or sharp, dramatic serifs.
- **Radius Policy**: Sharp edges or pointed arcs.
- **Shadow Policy**: Deep, dramatic shadows.
- **Border Language**: Ornate, gothic-style borders.
- **Patterns**: Damask, gothic arches, intricate lace.
- **Motion**: Dramatic, slow transitions. Mystery feel.

## Rules
### Do
- Use dramatic lighting and shadows
- Apply deep, mysterious colors
- Use sharp, ornate borders
- Emphasize gothic architecture

### Don't
- Don't use bright, happy colors
- Don't use rounded pill shapes
- Don't use casual sans-serifs exclusively
- Don't use playful animations

---

## Complete Prompt

# Gothic SaaS Landing Page Prompt (S15)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S15 Gothic** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S15 — Gothic
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

## Style DNA (S15 – Gothic)

### Style Seeds
- **Palette strategy:** High contrast dark palette. Black, deep purples, and blood reds.
- **Typography:** Blackletter or sharp, dramatic serifs.
- **Radius policy:** Sharp edges or pointed arcs.
- **Shadow policy:** Deep, dramatic shadows.
- **Border language:** Ornate, gothic-style borders.
- **Patterns/textures:** Damask, gothic arches, intricate lace.
- **Motion:** Dramatic, slow transitions. Mystery feel.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S15"
    style_name: "Gothic"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#000000"
      secondary: "#0D0D0D"
    text:
      primary: "#E0E0E0"
      secondary: "#8A8A8A"
      muted: "#4A4A4A"
    brand:
      primary: "#800000"
      accent: "#4B0082"
    border:
      strong: "#333333"
      subtle: "#1A1A1A"
    focus:
      ring: "#800000"
  radius:
    none: 0
    sm: 0
    md: 0
  border:
    width: { hairline: 1, medium: 2, strong: 4 }
  shadow:
    dramatic: "0 10px 40px rgba(0,0,0,0.9)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      serif: { primary: "Cinzel Decorative", fallback: ["serif"] }
      sans: { primary: "UnifrakturMaguntia", fallback: ["serif"] }
    scale:
      h1: { size: 60, line: 68, weight: 400, tracking: 0.1 }
      h2: { size: 44, line: 52, weight: 400, tracking: 0.05 }
      body: { size: 18, line: 30, weight: 400, tracking: 0.02 }
  spacing:
    base: 12
    section_py: { mobile: [100, 120], desktop: [180, 240] }
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
