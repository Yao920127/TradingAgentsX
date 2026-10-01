# Style: Cyberpunk / TRON (S16)

## Overview
- **ID**: S16
- **Name**: Cyberpunk (TRON Masterpiece Edition)
- **Industries**: High-Tech, Gaming, Neural Research, Visionary SaaS
- **Category**: Digital Frontier / Retro-Futurism

## Design DNA
- **Palette Strategy**: Pure "Void Black" (#000000) depth. Primary "Electric Cyan" (#00E5FF) for energy, secondary "Lightcycle Orange" (#FF9E00) for alerts. White used sparingly for high-intensity focal points.
- **Typography**: `Orbitron` for high-impact display (italicized for speed). `Rajdhani` for technical body text, using high letter-spacing (tracking) for uppercase metadata.
- **Radius Policy**: Perfect 1:1 circular motifs (Identity Disks) or absolute-zero sharp edges. No soft modern rounding.
- **Shadow Policy**: Gaussian-blurred neon bloom. Multiple layers of glows to simulate light emission in a dark atmosphere.
- **Border Language**: Glowing hairline borders, often doubled or nested. Moving light-trails on container edges.
- **Patterns**: 3D perspective grids receding into infinite horizon. Atmospheric fog/mist using noise masks. Vertical "Uplink" beams of light.
- **Motion**: Linear, precise, "light-speed" transitions. Pulsing energy rings, scanning lines, and digital disintegration effects.

## Rules
### Do
- Use `#000000` for absolute background depth
- Incorporate a central "Vertical Light Beam" for epic scale
- Focus on "Lighting as Texture" (Gradients and Glows)
- Use "Identity Disk" UI elements for navigation or status
- Embrace atmospheric depth (Mist/Clouds in the distance)

### Don't
- Don't use flat grey - use semi-transparent cyan over black
- Don't use organic rounded corners (unless they are perfect circles)
- Don't use cluttered or noisy textures (keep it clean but backlit)
- Don't take itself casually - maintain a visionary, cinematic tone

---

## Complete Prompt

# Cyberpunk / TRON "Masterpiece Edition" Prompt (S16)

## Objective
Design a **World-Class, Cinematic Landing Page** that feels like a **Digital Frontier**. This is not just a UI; it is an **Atmospheric Experience** for a high-tech SaaS or visionary product.

## Inputs
- **Style:** S16 — Cyberpunk Masterpiece (TRON Legacy)
- **Mood:** Visionary, Cinematic, Precise, Deep Space

## Style DNA Implementation (S16)

### 1. Atmosphere & Lighting (The Foundation)
- **Container**: Absolute black background (`#000000`).
- **Texture**: Add a subtle noise-masked "Mist" or "Fog" at the bottom and center to create depth.
- **Master Light**: A single, white-to-cyan vertical light beam running through the center of the page, acting as the visual spine.
- **Bloom**: Every interactive element must emit a 15-40px Gaussian glow.

### 2. Typography & Branding
- **H1 Header**: Massive (120px+), using `Orbitron` Black, italicized. Apply a vertical gradient from White to Cyan-Fade.
- **Sub-headers**: Small, uppercase `Rajdhani` with 0.8em letter spacing.
- **Visual Motif**: Use the "Identity Disk" (Ring with a glowing core) as the primary brand asset and loading state.

### 3. Layout Components (The Grid)
- **Hero**: A wide-open "Floor" with a 3D perspective grid receding into a glowing blue horizon.
- **Feature Cards**: "Glassmorphism" panels with glowing cyan hairline borders. Content should appear "projected" onto the glass.
- **Status Indicators**: Use "Lightcycle Orange" (#FF9E00) sparingly for warnings or high-priority status alerts.

### 4. Interactive Motion
- **Hover**: Elements should "ignite" with increased bloom.
- **Scroll**: Use subtle "Perspective Parallax" on the grid floor.
- **Transitions**: High-speed linear slides (150ms) mimicking light trails.

---

```yaml
tokens:
  meta:
    style_id: "S16"
    style_name: "Cyberpunk/TRON Masterpiece"
  color:
    bg:
      primary: "#000000"
      secondary: "#00050A"
    text:
      primary: "#FFFFFF"
      secondary: "#00E5FF"
      muted: "rgba(0, 229, 255, 0.3)"
    brand:
      primary: "#00E5FF"
      secondary: "#FF9E00"
      accent: "#FFFFFF"
    border:
      strong: "#00E5FF"
      glow: "0 0 15px rgba(0, 229, 255, 0.5)"
  radius:
    none: 0
    full: 9999
  shadow:
    neon: "0 0 30px #00E5FF"
    beam: "0 0 100px rgba(0, 225, 255, 0.4)"
  typography:
    font:
      sans: { primary: "Orbitron", body: "Rajdhani" }
      mono: { primary: "JetBrains Mono" }
    scale:
      h1: { size: 140, weight: 900, tracking: 0.05 }
      metadata: { size: 10, weight: 700, tracking: 0.6 }
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
