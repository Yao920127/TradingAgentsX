# Style: Nature Organic (S20)

## Overview
- **ID**: S20
- **Name**: Nature Organic
- **Industries**: Lifestyle, Commerce
- **Category**: Unique

## Design DNA
- **Palette Strategy**: Natural organic style. Earthy tones (greens, browns, soft creams).
- **Typography**: Soft, rounded fonts (e.g., Quicksand, Montserrat). Organic feel.
- **Radius Policy**: Large, organic rounding (16-32px).
- **Shadow Policy**: Soft, natural deep shadows.
- **Border Language**: Subtle, organic borders with natural textures.
- **Patterns**: Leaves, waves, organic shapes.
- **Motion**: Slow, graceful, natural-feeling transitions.

## Rules
### Do
- Use earthy, natural color palettes
- Apply soft, natural shadow effects
- Use large rounded corners and organic shapes
- Incorporate nature-inspired motifs

### Don't
- Don't use cold, industrial colors exclusively
- Don't use sharp, industrial corners
- Don't use heavy, rigid borders
- Don't use fast, mechanical animations

---

## Complete Prompt

# Nature Organic SaaS Landing Page Prompt (S20)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S20 Nature Organic** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S20 — Nature Organic
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

## Style DNA (S20 – Nature Organic)

### Style Seeds
- **Palette strategy:** Natural organic style. Earthy tones (greens, browns, soft creams).
- **Typography:** Soft, rounded fonts (e.g., Quicksand, Montserrat). Organic feel.
- **Radius policy:** Large, organic rounding (16-32px).
- **Shadow policy:** Soft, natural deep shadows.
- **Border language:** Subtle, organic borders with natural textures.
- **Patterns/textures:** Leaves, waves, organic shapes.
- **Motion:** Slow, graceful, natural-feeling transitions.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S20"
    style_name: "Nature Organic"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FDFCF7"
      secondary: "#F3F4ED"
    text:
      primary: "#2C3E50"
      secondary: "#5A6A70"
      muted: "#A0A090"
    brand:
      primary: "#4E6B3F"
      secondary: "#D2691E"
      accent: "#8B4513"
    border:
      strong: "#4E6B3F"
      subtle: "rgba(78, 107, 63, 0.2)"
    focus:
      ring: "#4E6B3F"
  radius:
    none: 0
    sm: 12
    md: 20
    lg: 32
    pill: 9999
  border:
    width: { hairline: 1, medium: 2, strong: 3 }
  shadow:
    soft: "0 10px 30px rgba(0,0,0,0.05)"
  layout:
    container: { content: 1100, wide: 1200 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Quicksand", fallback: ["Montserrat", "sans-serif"] }
    scale:
      h1: { size: 56, line: 64, weight: 600, tracking: 0.02 }
      h2: { size: 40, line: 48, weight: 600, tracking: 0.01 }
      body: { size: 18, line: 28, weight: 400, tracking: 0.02 }
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
