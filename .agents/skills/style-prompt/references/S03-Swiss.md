# Style: Swiss Design (S03)

## Overview
- **ID**: S03
- **Name**: Swiss Design
- **Industries**: Creative, Professional
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: High contrast, limited palette. Essential colors, often pure black/white with one or two vibrant accents.
- **Typography**: Strict grid alignment. Helvetica or similar grotesque sans-serifs. Highly structured.
- **Radius Policy**: Zero radius (0px). Sharp, crisp, unyielding edges.
- **Shadow Policy**: None. Complete absence of depth. Flat blocks only.
- **Border Language**: Prominent, thick, structural black lines acting as grid dividers.
- **Patterns**: Mathematical grids, modular structures.
- **Motion**: Instantaneous or rigid linear transitions. No playful bounces.

## Rules
### Do
- Use a strict modular grid
- Employ high-contrast typography
- Use clear, unambiguous iconography
- Maximize negative space systematically

### Don't
- Don't use gradients or drop shadows
- Don't use rounded corners
- Don't center-align text unnecessarily
- Don't use decorative elements

---

## Complete Prompt

# Swiss Design SaaS Landing Page Prompt (S03)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S03 Swiss Design** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S03 — Swiss Design
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

## Style DNA (S03 – Swiss Design)

### Style Seeds
- **Palette strategy:** High contrast, limited palette. Essential colors, often pure black/white with one or two vibrant accents.
- **Typography:** Strict grid alignment. Helvetica or similar grotesque sans-serifs. Highly structured.
- **Radius policy:** Zero radius (0px). Sharp, crisp, unyielding edges.
- **Shadow policy:** None. Complete absence of depth. Flat blocks only.
- **Border language:** Prominent, thick, structural black lines acting as grid dividers.
- **Patterns/textures:** Mathematical grids, modular structures.
- **Motion:** Instantaneous or rigid linear transitions. No playful bounces.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S03"
    style_name: "Swiss Design"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#F5F5F0"
      secondary: "#EAEAEA"
    text:
      primary: "#1A1A1A"
      secondary: "#4A4A4A"
      muted: "#8A8A8A"
    brand:
      primary: "#E02424"
      accent: "#0055FF"
    border:
      strong: "#000000"
      subtle: "#000000"
    state:
      success: "#0E9F6E"
      warning: "#E3A008"
      error: "#E02424"
    focus:
      ring: "#000000"
  radius:
    none: 0
    sm: 0
    md: 0
    lg: 0
  border:
    width:
      hairline: 1
      medium: 2
      strong: 4
  shadow:
    none: none
  layout:
    container:
      content: 1120
      wide: 1280
    grid:
      desktop: 12
      tablet: 6
      mobile: 4
    gutter: { mobile: 16, desktop: 32 }
  motion:
    duration: { fast: 100, normal: 200 }
    easing: "linear"
  typography:
    font:
      sans: { primary: "Helvetica Neue", fallback: ["Arial", "sans-serif"] }
      mono: { primary: "Space Mono", fallback: ["monospace"] }
    scale:
      h1: { size: 64, line: 72, weight: 700, tracking: -0.02 }
      h2: { size: 48, line: 56, weight: 700, tracking: -0.01 }
      h3: { size: 32, line: 40, weight: 600, tracking: 0 }
      body: { size: 18, line: 28, weight: 400, tracking: 0 }
      small: { size: 14, line: 20, weight: 400, tracking: 0 }
  spacing:
    base: 8
    section_py: { mobile: [64, 80], desktop: [128, 160] }
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
