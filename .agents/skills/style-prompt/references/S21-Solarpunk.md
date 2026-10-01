# Style: Solarpunk (S21)

## Overview
- **ID**: S21
- **Name**: Solarpunk
- **Industries**: Professional
- **Category**: Unique

## Design DNA
- **Palette Strategy**: Natural greens, warm yellows, white/cream. Organic feel.
- **Typography**: Rounded sans-serif or soft serif.
- **Radius Policy**: Organic, heavily rounded corners.
- **Shadow Policy**: Soft, diffused sunlight shadows.
- **Border Language**: Subtle, natural borders.
- **Patterns**: Nature-inspired patterns, leaves, sun rays.
- **Motion**: Calm, smooth transitions (300-600ms). Organic curves.

## Rules
### Do
- Use nature-inspired colors
- Emphasize sustainability
- Use organic shapes and rounded corners
- Incorporate solar/nature motifs

### Don't
- Don't use industrial grays
- Don't use sharp, aggressive shapes
- Don't use heavy, solid borders
- Don't use fast, mechanical animations

---

## Complete Prompt

# Solarpunk SaaS Landing Page Prompt (S21)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S21 Solarpunk** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S21 — Solarpunk
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

## Style DNA (S21 – Solarpunk)

### Style Seeds
- **Palette strategy:** Natural greens, warm yellows, white/cream. Organic feel.
- **Typography:** Rounded sans-serif or soft serif.
- **Radius policy:** Organic, heavily rounded corners.
- **Shadow policy:** Soft, diffused sunlight shadows.
- **Border language:** Subtle, natural borders.
- **Patterns/textures:** Nature-inspired patterns, leaves, sun rays.
- **Motion:** Calm, smooth transitions (300-600ms). Organic curves.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S21"
    style_name: "Solarpunk"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FDFCF8"
      secondary: "#F0FDF4"
    text:
      primary: "#064E3B"
      secondary: "#065F46"
      muted: "#A7F3D0"
    brand:
      primary: "#10B981"
      accent: "#F59E0B"
    border:
      strong: "#D1FAE5"
      subtle: "#F0FDF4"
    focus:
      ring: "#10B981"
  radius:
    none: 0
    sm: 8
    md: 16
    lg: 24
    xl: 32
    organic: "60% 40% 50% 50% / 40% 60% 50% 50%"
  border:
    width: { hairline: 1, medium: 2 }
  shadow:
    soft: "0 10px 25px rgba(16,185,129,0.1)"
    sunlight: "0 20px 40px rgba(245,158,11,0.1)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 300, normal: 600 }
    easing: "cubic-bezier(0.23, 1, 0.32, 1)"
  typography:
    font:
      sans: { primary: "Outfit", fallback: ["sans-serif"] }
      serif: { primary: "Fraunces", fallback: ["serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 600, tracking: -0.01 }
      h2: { size: 40, line: 48, weight: 600, tracking: 0 }
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
