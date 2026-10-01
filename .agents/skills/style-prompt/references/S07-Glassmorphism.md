# Style: Glassmorphism (S07)

## Overview
- **ID**: S07
- **Name**: Glassmorphism
- **Industries**: Tech, Creative
- **Category**: Futuristic

## Design DNA
- **Palette Strategy**: Translucent colors. Gradient backgrounds. Frosted effects.
- **Typography**: Modern sans-serif. Clean and readable.
- **Radius Policy**: Large radius (16-24px). Soft, pill shapes.
- **Shadow Policy**: Soft, diffused shadows. Layered depth.
- **Border Language**: Subtle, light borders. Frosted edges.
- **Patterns**: Organic shapes in background with high blur.
- **Motion**: Smooth animations. Parallax effects.

## Rules
### Do
- Use frosted glass effects
- Add subtle transparency
- Create depth with layers
- Use soft shadows

### Don't
- Don't use opaque backgrounds
- Don't forget the blur effect
- Don't use harsh edges
- Don't overdo the transparency

---

## Complete Prompt

# Glassmorphism SaaS Landing Page Prompt (S07)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S07 Glassmorphism** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S07 — Glassmorphism
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

## Style DNA (S07 – Glassmorphism)

### Style Seeds
- **Palette strategy:** Translucent colors. Gradient backgrounds. Frosted effects.
- **Typography:** Modern sans-serif. Clean and readable.
- **Radius policy:** Large radius (16-24px). Soft, pill shapes.
- **Shadow policy:** Soft, diffused shadows. Layered depth.
- **Border language:** Subtle, light borders. Frosted edges.
- **Patterns/textures:** Organic shapes in background with high blur.
- **Motion:** Smooth animations. Parallax effects.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S07"
    style_name: "Glassmorphism"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "rgba(255,255,255,0.7)"
      secondary: "rgba(255,255,255,0.5)"
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    text:
      primary: "#1A1A2E"
      secondary: "#4A4A4A"
      muted: "#8A8AA0"
    brand:
      primary: "#667eea"
      accent: "#764ba2"
    border:
      strong: "rgba(255,255,255,0.3)"
      subtle: "rgba(255,255,255,0.1)"
    state: { success: "#667eea", warning: "#764ba2", error: "#1A1A2E" }
    focus: { ring: "#667eea" }
  radius:
    none: 0
    sm: 12
    md: 20
    lg: 28
    pill: 9999
  border:
    width: { hairline: 1, medium: 2, strong: 3 }
  shadow:
    glass: "0 8px 32px rgba(0,0,0,0.1)"
    soft: "0 4px 16px rgba(0,0,0,0.08)"
  blur:
    glass: "blur(10px)"
    strong: "blur(20px)"
  layout:
    container: { content: 1120, wide: 1280 }
    grid: { desktop: 12, tablet: 8, mobile: 4 }
    gutter: { mobile: 16, desktop: 24 }
  motion:
    duration: { fast: 200, normal: 400 }
    easing: ease-out
  typography:
    font:
      sans: { primary: "SF Pro Display", fallback: ["Inter", "system-ui", "sans-serif"] }
      mono: { primary: "JetBrains Mono", fallback: ["ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 600, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 600, tracking: -0.01 }
      h3: { size: 28, line: 36, weight: 600, tracking: -0.005 }
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
