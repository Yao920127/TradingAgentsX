# Style: Dark Mode Elegance (S08)

## Overview
- **ID**: S08
- **Name**: Dark Mode Elegance
- **Industries**: Tech, Lifestyle
- **Category**: Minimalist

## Design DNA
- **Palette Strategy**: Dark mode with cyan/purple accents. High contrast for readability. Subtle gradients for depth.
- **Typography**: Clean monospace for tech feel. Mixed with sans-serif for readability. Consistent spacing.
- **Radius Policy**: Minimal (4-8px). Tech aesthetic with slight softening.
- **Shadow Policy**: Glow effects and subtle elevation. Colored shadows for tech feel.
- **Border Language**: Thin borders with tech feel. Cyan/purple accents.
- **Patterns**: Subtle tech grids, micro-patterns.
- **Motion**: Fast, responsive animations (150-200ms). Tech feel.

## Rules
### Do
- Use high contrast for readability
- Add subtle cyan/purple accents
- Create depth with shadows
- Ensure accessibility in dark mode

### Don't
- Don't use low contrast text
- Don't ignore accessibility
- Don't overdo the effects
- Don't use flat blacks exclusively

---

## Complete Prompt

# Dark Mode Elegance SaaS Landing Page Prompt (S08)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S08 Dark Mode Elegance** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S08 — Dark Mode Elegance
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

## Style DNA (S08 – Dark Mode Elegance)

### Style Seeds
- **Palette strategy:** Dark mode with cyan/purple accents. High contrast for readability. Subtle gradients for depth.
- **Typography:** Clean monospace for tech feel. Mixed with sans-serif for readability. Consistent spacing.
- **Radius policy:** Minimal (4-8px). Tech aesthetic with slight softening.
- **Shadow policy:** Glow effects and subtle elevation. Colored shadows for tech feel.
- **Border language:** Thin borders with tech feel. Cyan/purple accents.
- **Patterns/textures:** Subtle tech grids, micro-patterns.
- **Motion:** Fast, responsive animations (150-200ms). Tech feel.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S08"
    style_name: "Dark Mode Elegance"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#000000"
      secondary: "#141414"
      gradient: "linear-gradient(135deg, #000000 0%, #1A1A1A 100%)"
    text:
      primary: "#FFFFFF"
      secondary: "#CCCCCC"
      muted: "#888888"
    brand:
      primary: "#00D9FF"
      secondary: "#7C3AED"
      accent: "#10B981"
    border:
      strong: "#333333"
      subtle: "#1A1A1A"
    state: { success: "#10B981", warning: "#F59E0B", error: "#EF4444" }
    focus: { ring: "#00D9FF" }
  radius:
    none: 0
    sm: 4
    md: 8
    lg: 12
  border:
    width: { hairline: 1, medium: 2, strong: 3 }
  shadow:
    glow: "0 0 20px rgba(0, 217, 255, 0.5)"
    elevation: "0 4px 16px rgba(0,0,0,0.3)"
    colored: "0 4px 16px rgba(0, 217, 255, 0.2)"
  layout:
    container: { content: 1100, wide: 1260 }
    grid: { desktop: 12, tablet: 8, mobile: 4 }
    gutter: { mobile: 14, desktop: 20 }
  motion:
    duration: { fast: 150, normal: 200, slow: 300 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Inter", fallback: ["SF Pro Display", "system-ui", "-apple-system"] }
      mono: { primary: "JetBrains Mono", fallback: ["SF Mono", "ui-monospace"] }
    scale:
      h1: { size: 56, line: 64, weight: 700, tracking: -0.02 }
      h2: { size: 40, line: 48, weight: 700, tracking: -0.01 }
      h3: { size: 28, line: 36, weight: 700, tracking: -0.005 }
      body: { size: 16, line: 24, weight: 400, tracking: 0 }
      small: { size: 14, line: 20, weight: 400, tracking: 0 }
    measure: { hero_max: "48ch", body_max: "72ch" }
  spacing:
    base: 8
    section_py: { mobile: [80, 96], desktop: [128, 144] }
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
