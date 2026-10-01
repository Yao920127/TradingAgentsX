# Style: Minimalist Serif (S24)

## Overview
- **ID**: S24
- **Name**: Minimalist Serif
- **Industries**: Luxury, Creative
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: High-end fashion editorial. Creams, subtle golds, stark black and white. (Adapted for Serif)
- **Typography**: Ultra-refined serif (Didot/Bodoni) with high stroke contrast.
- **Radius Policy**: Strict sharp edges (0px).
- **Shadow Policy**: Subtle, elegant drop shadows.
- **Border Language**: Minimally used borders, hairline weight.
- **Patterns**: High-end editorial grids.
- **Motion**: Slow, graceful transitions.

## Rules
### Do
- Use high-stroke-contrast serifs
- Keep whitespace expansive
- Maintain architectural precision
- Use refined, muted colors

### Don't
- Don't use rounded corners
- Don't use casual fonts
- Don't overcrowd the design
- Don't use fast or bouncy animations

---

## Complete Prompt

# Minimalist Serif SaaS Landing Page Prompt (S24)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S24 Minimalist Serif** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S24 — Minimalist Serif
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

## Style DNA (S24 – Minimalist Serif)

### Style Seeds
- **Palette strategy:** High-end fashion editorial. Creams, subtle golds, stark black and white. (Adapted for Serif)
- **Typography:** Ultra-refined serif (Didot/Bodoni) with high stroke contrast.
- **Radius policy:** Strict sharp edges (0px).
- **Shadow policy:** Subtle, elegant drop shadows.
- **Border language:** Minimally used borders, hairline weight.
- **Patterns/textures:** High-end editorial grids.
- **Motion:** Slow, graceful transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S24"
    style_name: "Minimalist Serif"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FAFAFA"
      secondary: "#FFFFFF"
    text:
      primary: "#000000"
      secondary: "#333333"
      muted: "#999999"
    brand:
      primary: "#000000"
      accent: "#000000"
    border:
      strong: "#000000"
      subtle: "#E5E5E5"
    focus:
      ring: "#000000"
  radius:
    none: 0
  border:
    width: { hairline: 0.5, medium: 1 }
  shadow:
    none: none
    soft: "0 10px 30px rgba(0,0,0,0.05)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 300, normal: 600 }
    easing: "cubic-bezier(0.2, 0, 0, 1)"
  typography:
    font:
      serif: { primary: "Bodoni MT", fallback: ["Didot", "serif"] }
    scale:
      h1: { size: 64, line: 72, weight: 400, tracking: -0.01 }
      h2: { size: 44, line: 52, weight: 400, tracking: 0 }
      body: { size: 16, line: 26, weight: 400, tracking: 0.02 }
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
