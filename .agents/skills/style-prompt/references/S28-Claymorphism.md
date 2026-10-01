# Style: Claymorphism (S28)

## Overview
- **ID**: S28
- **Name**: Claymorphism
- **Industries**: Creative, Professional
- **Category**: Unique

## Design DNA
- **Palette Strategy**: Soft, candy-like pastels. 3D depth without gradients.
- **Typography**: Friendly, rounded sans-serif (e.g., Nunito, Quicksand).
- **Radius Policy**: Extremely large radius (24-40px). Squircle/pill shapes.
- **Shadow Policy**: Inner shadows + drop shadows for 3D "clay" puffy effect. No borders.
- **Border Language**: None. Form defined by layered shadows.
- **Patterns**: None. Pure solid 3D forms.
- **Motion**: Squishy, elastic, bouncy animations (300-500ms).

## Rules
### Do
- Use multiple layered shadows for 3D effect
- Create soft, puffy clay-like forms
- Use bright pastel colors
- Maintain a playful and tactile feel

### Don't
- Don't use flat design exclusively
- Don't use sharp corners
- Don't use dark or gritty colors
- Don't use complex textures or borders

---

## Complete Prompt

# Claymorphism SaaS Landing Page Prompt (S28)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S28 Claymorphism** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S28 — Claymorphism
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

## Style DNA (S28 – Claymorphism)

### Style Seeds
- **Palette strategy:** Soft, candy-like pastels. 3D depth without gradients.
- **Typography:** Friendly, rounded sans-serif (e.g., Nunito, Quicksand).
- **Radius policy:** Extremely large radius (24-40px). Squircle/pill shapes.
- **Shadow policy:** Inner shadows + drop shadows for 3D "clay" puffy effect. No borders.
- **Border language:** None. Form defined by layered shadows.
- **Patterns/textures:** None. Pure solid 3D forms.
- **Motion:** Squishy, elastic, bouncy animations (300-500ms).

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S28"
    style_name: "Claymorphism"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#F3F6FD"
      secondary: "#E8EEF9"
    text:
      primary: "#2B3C5A"
      secondary: "#4A5D80"
      muted: "#8496B5"
    brand:
      primary: "#4E7CFF"
      secondary: "#FF6B8B"
      accent: "#FFD166"
    border:
      strong: transparent
      subtle: transparent
    focus:
      ring: "#4E7CFF"
  radius:
    none: 0
    sm: 16
    md: 24
    lg: 32
    xl: 40
    pill: 9999
  border:
    width: { hairline: 0, medium: 0, strong: 0 }
  shadow:
    clay: "8px 8px 16px rgba(166, 180, 200, 0.5), -8px -8px 16px rgba(255, 255, 255, 0.8), inset -4px -4px 8px rgba(166, 180, 200, 0.3), inset 4px 4px 8px rgba(255, 255, 255, 0.5)"
    clay_inset: "inset 8px 8px 16px rgba(166, 180, 200, 0.5), inset -8px -8px 16px rgba(255, 255, 255, 0.8)"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 200, normal: 400 }
    easing: "cubic-bezier(0.34, 1.56, 0.64, 1)"
  typography:
    font:
      sans: { primary: "Nunito", fallback: ["Varela Round", "sans-serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 800, tracking: -0.01 }
      h2: { size: 40, line: 48, weight: 800, tracking: 0 }
      body: { size: 16, line: 26, weight: 600, tracking: 0 }
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
