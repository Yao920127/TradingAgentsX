# Style: Memphis (S10)

## Overview
- **ID**: S10
- **Name**: Memphis
- **Industries**: Creative, Lifestyle, Modern SaaS, Fashion
- **Category**: Artistic / Post-Modern

## Design DNA
- **Palette Strategy**: High-saturation primary colors (Pink, Yellow, Cyan, Lime) paired with stark white and thick black. "Color Blocking" technique.
- **Typography**: Bold, playful sans-serifs (Fredoka, Montserrat) with heavy weights. Irregular alignments.
- **Radius Policy**: Mixed geometry. Perfect circles next to sharp squares and triangles.
- **Shadow Policy**: "Hard Offset" shadows. Solid black shadows displaced by 4-8px without any blur.
- **Border Language**: Extremely thick black borders (3px - 6px) on almost every container and element.
- **Patterns**: "Confetti" patterns: random floating dots, zigzags, wavy lines, and geometric shapes.
- **Motion**: Bouncy, playful transitions (300ms - 500ms). Exaggerated "Pop" effects.

## Rules
### Do
- Use thick black outlines on everything
- Embrace "Tactile" depth with hard offset shadows
- Mix seemingly clashing primary colors
- Add randomized floating shapes (dots, zigzags) as background elements
- Use bold, tilted, or non-traditional text placements

### Don't
- Don't use soft gradients or realistic shadows
- Don't follow a strict, quiet grid (needs some "ordered chaos")
- Don't use thin, delicate lines
- Don't keep everything aligned to the center; use asymmetry

---

## Complete Prompt

# Memphis SaaS Landing Page Prompt (S10)

## Objective
Design and specify a **High-Energy, Post-Modern Full Landing Page** for a **Creative SaaS product** using the **S10 Memphis** style. Output must be a **Visual Explosion** of geometry and color.

## Inputs
- **Style:** S10 — Memphis
- **Industry:** Creative Tech
- **Use:** Full Landing Page

## Style DNA Implementation (S10)

### 1. Visual Geometry & Colors
- **Background**: Start with a pure white base but liberally use "Confetti" patterns (floating black dots, pink triangles, cyan squiggles).
- **Core Elements**: Every card or section must have a **4px solid black border** and a **8px hard black offset shadow**.
- **Palette**: Use `#FF61D2` (Pink), `#FFE100` (Yellow), `#00F0FF` (Cyan), and `#C1FF00` (Lime).

### 2. Typography & Headers
- **Headers**: Use `Montserrat` Black or a similar heavy font. Tilt some sub-headers by -2 to 3 degrees. 
- **Hierarchy**: Use "Colored Blocks" as backgrounds for text to make it pop.

### 3. Components
- **Hero**: Use overlapping geometric shapes (large circles and triangles) behind the main product image. 
- **Features**: Instead of a clean grid, use slightly offset cards with varying border colors.
- **Buttons**: Thick borders, vibrant colors, "Pop-up" motion on hover (moving the button away from its shadow).

---

```yaml
tokens:
  meta:
    style_id: "S10"
    style_name: "Memphis"
    industry: "Creative SaaS"
    use_case: "Full Landing Page"
  color:
    bg:
      primary: "#FFFFFF"
      secondary: "#FFB0E0"
    text:
      primary: "#000000"
      secondary: "#222222"
      muted: "#555555"
    brand:
      primary: "#FF61D2"
      secondary: "#FFE100"
      accent: "#00F0FF"
    border:
      strong: "#000000"
      accent: "#C1FF00"
    focus:
      ring: "#000000"
  radius:
    none: 0
    full: 9999
  border:
    width: { hairline: 2, medium: 4, strong: 6 }
  shadow:
    hard: "8px 8px 0 #000000"
    hard_sm: "4px 4px 0 #000000"
  layout:
    container: { content: 1120, wide: 1280 }
  motion:
    duration: { fast: 150, normal: 300, bouncy: 500 }
    easing: "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
  typography:
    font:
      sans: { primary: "Montserrat", fallback: ["Fredoka One", "sans-serif"] }
    scale:
      h1: { size: 84, weight: 900, tracking: -0.05 }
      body: { size: 18, weight: 700, tracking: 0 }
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
