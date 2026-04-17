# Design System: AI Women's Health Risk (The Serene Sanctuary)

## Typography

This system utilizes a dual-typeface strategy to communicate both modern intelligence and accessible warmth.

- **Headline Font**: Manrope - A modern, geometric sans-serif that feels authoritative yet approachable.
- **Body Font**: Inter - Chosen for its exceptional legibility. Even at small text sizes, the high x-height ensures clarity for users in any environment.
- **Label Font**: Inter

## Color Palette

The palette centers on the balance between the authority of deep teals and the biological warmth of soft corals, all resting upon a comforting, cream-based white foundation.

### Primary Colors
- **Primary**: `#006770`
- **Primary Container**: `#12828C`
- **On Primary**: `#ffffff`
- **On Primary Container**: `#fdffff`

### Secondary Colors
- **Secondary**: `#9a442d`
- **Secondary Container**: `#fc9174`
- **On Secondary**: `#ffffff`
- **On Secondary Container**: `#742814`

### Tertiary Colors
- **Tertiary**: `#376651`
- **Tertiary Container**: `#507f69`
- **On Tertiary**: `#ffffff`
- **On Tertiary Container**: `#fcfffb`

### Backgrounds & Surfaces
- **Background**: `#fdfae7`
- **On Background**: `#1c1c11`
- **Surface**: `#fdfae7`
- **Surface Container Lowest**: `#ffffff`
- **Surface Container Low**: `#f7f4e1`
- **Surface Container**: `#f1eedb`
- **Surface Container High**: `#ece9d6`
- **Surface Variant**: `#e6e3d0`
- **On Surface**: `#1c1c11`
- **On Surface Variant**: `#3e494a`

### Error States
- **Error**: `#ba1a1a`
- **Error Container**: `#ffdad6`
- **On Error**: `#ffffff`
- **On Error Container**: `#93000a`

### Outline & Borders
- **Outline**: `#6e797a`
- **Outline Variant**: `#bdc9ca`

## Design Guidelines

### Colors: Tonal Depth over Structural Lines
- **The "No-Line" Rule**: To achieve a premium, custom feel, **1px solid borders are prohibited** for defining sections or containers. Use background shifts and tonal transitions instead (e.g. `surface-container-low` on `surface`).
- **Surface Hierarchy & Nesting**: Treat the UI as a series of physical layers:
  - Base: `surface` (`#fdfae7`)
  - Secondary Content: `surface-container` (`#f1eedb`)
  - Interactive Cards: `surface-container-lowest` (`#ffffff`) to create a "lifted" feel.
- **The "Glass & Gradient" Rule**: Floating elements (such as AI chat bubbles or nav bars) should use Glassmorphism (semi-transparent `surface-container-lowest` with a `backdrop-blur` of 20px). Signature textures should use a subtle linear gradient from `primary` to `primary_container`.

### Elevation & Depth: Atmospheric Layering
- **Ambient Shadows**: For floating effects, use a shadow with a large blur (30px+) and low opacity (max 6%), tinted with `on-surface`.
- **The "Ghost Border"**: If a border is strictly required for accessibility, use `outline-variant` at 15% opacity.

### Component Details
- **Buttons**:
  - Primary: Gradient `primary` to `primary-container`, `md` corner radius.
  - Secondary: Ghost-style with `on-surface` text and subtle `surface-container-high` background on hover. No borders.
- **Inputs**: Avoid "boxed" inputs. Use `surface-container` background with `md` corner radius. Focus states use a 2px glow of `surface-tint` (`#006971`).
- **Cards & Lists**: Zero dividers. Use vertical whitespace (24px - 32px) or alternating backgrounds instead. AI insight cards use Glassmorphism with a subtle `secondary_container` accent on top.
