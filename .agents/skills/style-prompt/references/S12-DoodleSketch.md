# Style: Doodle Sketch (S12)

## Overview
- **ID**: S12
- **Name**: Doodle Sketch
- **Industries**: Creative, Professional
- **Category**: Artistic

## Design DNA
- **Palette Strategy**: Clean, neutral base with playful accents. Hand-drawn feel.
- **Typography**: Clean, sans-serif mixed with sketch-style fonts. Approachesable feel.
- **Radius Policy**: Soft, irregular (12-20px). Natural feel.
- **Shadow Policy**: Subtle, soft shadows.
- **Border Language**: Irregular, hand-drawn lines.
- **Patterns**: Doodle-style patterns, squiggles, stars.
- **Motion**: Playful, bouncing animations (300-500ms).

## Rules
### Do
- Use hand-drawn elements
- Maintain a playful tone
- Use irregular borders
- Add whimsical touches

### Don't
- Don't be too rigid or corporate
- Don't use straight lines exclusively
- Don't over-animate
- Don't use cold colors

---

## Complete Prompt

# Doodle Sketch SaaS Landing Page Prompt (S12)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S12 Doodle Sketch** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S12 — Doodle Sketch
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

## Style DNA (S12 – Doodle Sketch)

### Style Seeds
- **Palette strategy:** Clean, neutral base with playful accents. Hand-drawn feel.
- **Typography:** Clean, sans-serif mixed with sketch-style fonts. Approachesable feel.
- **Radius policy:** Soft, irregular (12-20px). Natural feel.
- **Shadow policy:** Subtle, soft shadows.
- **Border language:** Irregular, hand-drawn lines.
- **Patterns/textures:** Doodle-style patterns, squiggles, stars.
- **Motion:** Playful, bouncing animations (300-500ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S12"
    style_name: "Doodle Sketch"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#FFFBEB"
    text:
      primary: "#1A1A1A"
      secondary: "#4A4A4A"
      muted: "#9CA3AF"
    brand:
      primary: "#F59E0B"
      accent: "#EC4899"
    border:
      strong: "#1A1A1A"
      subtle: "rgba(0,0,0,0.1)"
    focus:
      ring: "#F59E0B"
  radius:
    none: 0
    sm: 8
    md: 16
    lg: 24
    irregular: "255px 15px 225px 15px/15px 225px 15px 255px"
  border:
    width: { hairline: 1, medium: 2, strong: 3 }
  shadow:
    soft: "0 4px 14px 0 rgba(0,0,0,0.05)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 200, normal: 400 }
    easing: "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
  typography:
    font:
      sans: { primary: "Indie Flower", fallback: ["Quicksand", "sans-serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 400, tracking: 0.02 }
      h2: { size: 40, line: 48, weight: 400, tracking: 0.01 }
      body: { size: 18, line: 28, weight: 400, tracking: 0 }
  spacing:
    base: 10
    section_py: { mobile: [80, 100], desktop: [120, 160] }
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
