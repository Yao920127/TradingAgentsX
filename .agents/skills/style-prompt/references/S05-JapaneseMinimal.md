# Style: Japanese Minimal (S05)

## Overview
- **ID**: S05
- **Name**: Japanese Minimal
- **Industries**: Luxury, Creative
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: Muted, natural colors. Lots of white space. Subtle accents.
- **Typography**: Clean, minimal fonts. Light weights. Generous spacing.
- **Radius Policy**: Subtle (2-6px). Soft but not round.
- **Shadow Policy**: Very subtle or none. Rely on space.
- **Border Language**: Minimal, delicate borders.
- **Patterns**: None. Emphasis on negative space (Ma).
- **Motion**: Slow, deliberate. Zen-like.

## Rules
### Do
- Embrace whitespace (ma)
- Use subtle, natural colors
- Create balance and harmony
- Use delicate typography

### Don't
- Don't overcrowd the design
- Don't use bold, loud colors
- Don't add unnecessary elements
- Don't break the zen

---

## Complete Prompt

# Japanese Minimal SaaS Landing Page Prompt (S05)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S05 Japanese Minimal** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S05 — Japanese Minimal
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

## Style DNA (S05 – Japanese Minimal)

### Style Seeds
- **Palette strategy:** Muted, natural colors. Lots of white space. Subtle accents.
- **Typography:** Clean, minimal fonts. Light weights. Generous spacing.
- **Radius policy:** Subtle (2-6px). Soft but not round.
- **Shadow policy:** Very subtle or none. Rely on space.
- **Border language:** Minimal, delicate borders.
- **Patterns/textures:** None. Emphasis on negative space (Ma).
- **Motion:** Slow, deliberate. Zen-like.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S05"
    style_name: "Japanese Minimal"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#FAF9F6"
    text:
      primary: "#2D2D2D"
      secondary: "#5A5A5A"
      muted: "#9CA3AF"
    brand:
      primary: "#2D2D2D"
      accent: "#C5A059"
    border:
      strong: "#E5E7EB"
      subtle: "#F3F4F6"
    focus:
      ring: "#2D2D2D"
  radius:
    none: 0
    sm: 2
    md: 4
    lg: 8
  border:
    width: { hairline: 1, medium: 1 }
  shadow:
    none: none
  layout:
    container: { content: 1000, wide: 1200 }
  motion:
    duration: { fast: 300, normal: 500 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Noto Sans JP", fallback: ["Inter", "sans-serif"] }
      serif: { primary: "Noto Serif JP", fallback: ["serif"] }
    scale:
      h1: { size: 48, line: 60, weight: 300, tracking: 0.05 }
      h2: { size: 36, line: 44, weight: 300, tracking: 0.02 }
      h3: { size: 24, line: 32, weight: 400, tracking: 0.02 }
      body: { size: 16, line: 28, weight: 300, tracking: 0.05 }
      small: { size: 14, line: 22, weight: 300, tracking: 0.05 }
  spacing:
    base: 8
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

---
