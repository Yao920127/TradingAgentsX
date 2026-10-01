---
name: style-prompt
description: A comprehensive UI style library of 30 unique designs (S01-S30) for generating themed React + Tailwind CSS components. Features adaptive selection, design DNA extraction, and extensible style generation.
---

# Unique UI Style Library Skill (S01-S30)

A professional "Agents Skill" providing 30 high-fidelity, production-ready UI design styles. This skill empowers AI agents to programmatically discover, extract, and implement sophisticated design aesthetics for React and Tailwind CSS-based web applications.

## Progressive Disclosure for Agents

Follow this three-phase workflow to ensure design consistency and engineering quality:

### Phase 1: Adaptive Selection (Style Discovery)
Identify the target `styleId` (S01-S30) based on the user's industry, desired mood, or aesthetic keywords. If the user's intent is vague, use the following mapping to recommend a style:

| User Need | Recommended Style(s) | Key Aesthetic |
| :--- | :--- | :--- |
| **Clean & Professional** | S01, S09, S26 | Minimalist, Corporate, Enterprise Blue |
| **Luxury & Premium** | S13, S19, S22, S23 | Art Deco, Editorial, Gold, Silver |
| **Futuristic & Tech** | S06, S16, S17, S29 | Bauhaus, Cyberpunk, Synthwave, Bio-Noir |
| **Playful & Creative** | S10, S11, S12, S28 | Memphis, Neo-Brutalism, Doodle, Claymorphism |
| **Natural & Soft** | S05, S20, S21, S30 | Japanese Minimal, Nature, Solarpunk, Aurora |

### Phase 2: DNA Extraction (Deep Reading)
Locate and read the specific reference file in `.agents/skills/style-prompt/references/S[ID]-[Name].md`.
- **Primary Source**: Each file is the absolute "Source of Truth" for that style ID.
- **Content**: Extract the **Design DNA** (Strategy), **Rules** (Dos/Don'ts), and **Full YAML Tokens** (Variables).

### Phase 3: Implementation & Infinite Expansion
- **Precise Implementation**: Use the **Complete Assembled Prompt** at the bottom of the reference file. This prompt is pre-engineered with Next.js/Tailwind best practices and style-specific constraints.
- **Dynamic Expansion**: If the 30 styles do not perfectly match the user's vision, **create a hybrid or new style**. Reference an existing `.md` file (e.g., S01 for minimalist or S16 for dark/tech) as a structural template and override the `tokens` and `DNA` sections to fulfill the custom requirement.

## Reference Library (S01-S30)
Access the full specification files using the links below:

| ID | Style Name | Reference Link |
| :--- | :--- | :--- |
| **S01** | Tech Minimal | [S01-TechMinimal.md](./references/S01-TechMinimal.md) |
| **S02** | Minimalist Monochrome | [S02-MinimalistMonochrome.md](./references/S02-MinimalistMonochrome.md) |
| **S03** | Swiss Design | [S03-Swiss.md](./references/S03-Swiss.md) |
| **S04** | Brutalist | [S04-Brutalist.md](./references/S04-Brutalist.md) |
| **S05** | Japanese Minimal | [S05-JapaneseMinimal.md](./references/S05-JapaneseMinimal.md) |
| **S06** | Bauhaus Modernism | [S06-Bauhaus.md](./references/S06-Bauhaus.md) |
| **S07** | Glassmorphism | [S07-Glassmorphism.md](./references/S07-Glassmorphism.md) |
| **S08** | Dark Mode Elegance | [S08-DarkModeElegance.md](./references/S08-DarkModeElegance.md) |
| **S09** | Corporate Clean | [S09-CorporateClean.md](./references/S09-CorporateClean.md) |
| **S10** | Memphis | [S10-Memphis.md](./references/S10-Memphis.md) |
| **S11** | Neo-Brutalism | [S11-NeoBrutalism.md](./references/S11-NeoBrutalism.md) |
| **S12** | Doodle Sketch | [S12-DoodleSketch.md](./references/S12-DoodleSketch.md) |
| **S13** | Art Deco | [S13-ArtDeco.md](./references/S13-ArtDeco.md) |
| **S14** | Art Nouveau | [S14-ArtNouveau.md](./references/S14-ArtNouveau.md) |
| **S15** | Gothic | [S15-Gothic.md](./references/S15-Gothic.md) |
| **S16** | Cyberpunk / TRON | [S16-Cyberpunk.md](./references/S16-Cyberpunk.md) |
| **S17** | Retro 80s (Synthwave) | [S17-Synthwave.md](./references/S17-Synthwave.md) |
| **S18** | Y2K Aesthetic | [S18-Y2K.md](./references/S18-Y2K.md) |
| **S19** | Luxury Editorial | [S19-LuxuryEditorial.md](./references/S19-LuxuryEditorial.md) |
| **S20** | Nature Organic | [S20-NatureOrganic.md](./references/S20-NatureOrganic.md) |
| **S21** | Solarpunk | [S21-Solarpunk.md](./references/S21-Solarpunk.md) |
| **S22** | Luxury Gold | [S22-LuxuryGold.md](./references/S22-LuxuryGold.md) |
| **S23** | Luxury Silver | [S23-LuxurySilver.md](./references/S23-LuxurySilver.md) |
| **S24** | Minimalist Serif | [S24-MinimalistSerif.md](./references/S24-MinimalistSerif.md) |
| **S25** | Startup Vibrant | [S25-StartupVibrant.md](./references/S25-StartupVibrant.md) |
| **S26** | Enterprise Blue | [S26-EnterpriseBlue.md](./references/S26-EnterpriseBlue.md) |
| **S27** | Fintech Trust | [S27-FintechTrust.md](./references/S27-FintechTrust.md) |
| **S28** | Claymorphism | [S28-Claymorphism.md](./references/S28-Claymorphism.md) |
| **S29** | Cyber-Bio Noir | [S29-CyberBioNoir.md](./references/S29-CyberBioNoir.md) |
| **S30** | Aurora Borealis | [S30-AuroraBorealis.md](./references/S30-AuroraBorealis.md) |

## Engineering Standards
- **CSS Variables**: Use `--brand-primary`, `--bg-primary`, etc., mapped in `tailwind.config.ts`.
- **Accessibility**: Ensure WCAG AA contrast and keyboard navigability.
- **Responsiveness**: Implement mobile-first layouts using the `layout` and `grid` tokens.
- **Consistent State**: Use the `state` tokens (success, error, warning) for interactive elements.