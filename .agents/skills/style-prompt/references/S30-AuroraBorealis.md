# Style: Aurora Borealis (S30)

## Overview
- **ID**: S30
- **Name**: Aurora Borealis
- **Industries**: Creative, Lifestyle
- **Category**: Futuristic

## Design DNA
- **Palette Strategy**: Dark background with large animated colorful mesh gradients (green, purple, blue).
- **Typography**: Elegant, modern sans (e.g., Syne). Large tracking.
- **Radius Policy**: Soft, rounded containers (32px or pill).
- **Shadow Policy**: Subtle glass effect shadows. Colored glows from the mesh.
- **Border Language**: Translucent frosted glass borders.
- **Patterns**: Swirling color meshes, grainy animated gradients.
- **Motion**: Slow, continuous background color shifting. Smooth fades.

## Rules
### Do
- Use large gradient meshes (green/purple/blue)
- Keep foreground elements clean and minimal
- Use frosted glass for readability
- Make colors flow together slowly

### Don't
- Don't use harsh or sharp lines
- Don't use solid color blocks predominantly
- Don't use fast or jarring animations
- Don't overcrowd the layout

---

## Complete Prompt

# Aurora Borealis SaaS Landing Page Prompt (S30)

## Objective
Design and specify a **conversion-focused Full Landing Page** for a **SaaS product** using the **S30 Aurora Borealis** style. Output must be **engineering-ready**: tokens, layout specs, components, responsive behavior, and accessibility.

## Inputs
- **Style:** S30 — Aurora Borealis
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

## Style DNA (S30 – Aurora Borealis)

### Style Seeds
- **Palette strategy:** Dark background with large animated colorful mesh gradients (green, purple, blue).
- **Typography:** Elegant, modern sans (e.g., Syne). Large tracking.
- **Radius policy:** Soft, rounded containers (32px or pill).
- **Shadow policy:** Subtle glass effect shadows. Colored glows from the mesh.
- **Border language:** Translucent frosted glass borders.
- **Patterns/textures:** Swirling color meshes, grainy animated gradients.
- **Motion:** Slow, continuous background color shifting. Smooth fades.

Tone: confident, precise, non-hype.

---

```yaml
tokens:
  meta:
    style_id: "S30"
    style_name: "Aurora Borealis"
    industry: "SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#050510"
      mesh: "radial-gradient(at 0% 0%, #4c1d95 0px, transparent 50%), radial-gradient(at 100% 0%, #065f46 0px, transparent 50%)"
    text:
      primary: "#FFFFFF"
      secondary: "#CBD5E1"
    brand:
      primary: "#34D399"
      accent: "#A78BFA"
    border:
      strong: "rgba(255,255,255,0.2)"
      subtle: "rgba(255,255,255,0.05)"
    focus:
      ring: "#34D399"
  radius:
    none: 0
    sm: 8
    md: 16
    lg: 32
    pill: 9999
  border:
    width: { hairline: 1, medium: 1 }
  shadow:
    glass: "0 8px 32px 0 rgba(0,0,0,0.37)"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 400, normal: 800 }
    easing: "cubic-bezier(0.4, 0, 0.2, 1)"
  typography:
    font:
      sans: { primary: "Syne", fallback: ["Inter", "sans-serif"] }
    scale:
      h1: { size: 64, line: 72, weight: 700, tracking: -0.02 }
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
