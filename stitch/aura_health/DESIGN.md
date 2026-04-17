# Design System: The Serene Sanctuary

## 1. Overview & Creative North Star
In the landscape of women's healthcare, digital experiences often feel either overly clinical or patronizingly decorative. This design system seeks a middle path defined by the **"The Serene Sanctuary."** 

Our Creative North Star is an editorial-first approach that treats medical AI not as a cold diagnostic tool, but as a sophisticated, empathetic companion. We break the "generic template" look by utilizing intentional asymmetry, expansive whitespace, and a high-contrast typographic scale. By moving away from rigid grids and hard borders, we create a fluid, breathing environment that lowers user anxiety and fosters deep trust.

---

## 2. Colors: Tonal Depth over Structural Lines
The palette centers on the balance between the authority of deep teals and the biological warmth of soft corals, all resting upon a comforting, cream-based white foundation.

### The "No-Line" Rule
To achieve a premium, custom feel, designers are **prohibited from using 1px solid borders** to define sections or containers. Boundary definition must be achieved through:
*   **Background Shifts:** Place a `surface-container-low` (`#f7f4e1`) component against a `surface` (`#fdfae7`) background.
*   **Tonal Transitions:** Use subtle shifts in the surface hierarchy to denote importance.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of heavy-stock paper. 
*   **Base:** `surface` (`#fdfae7`) is our canvas.
*   **Secondary Content:** `surface-container` (`#f1eedb`) for sidebars or secondary modules.
*   **Interactive Cards:** `surface-container-lowest` (`#ffffff`) to create a "lifted" feel that draws the eye without needing a shadow.

### The "Glass & Gradient" Rule
Floating elements (such as AI chat bubbles or navigation bars) should utilize **Glassmorphism**. Apply a semi-transparent `surface-container-lowest` with a `backdrop-blur` of 20px. 
*   **Signature Textures:** For high-impact areas like hero sections or primary CTAs, use a subtle linear gradient from `primary` (`#006770`) to `primary_container` (`#12828c`). This adds a "soul" to the interface that flat colors cannot provide.

---

## 3. Typography: The Editorial Voice
This system utilizes a dual-typeface strategy to communicate both modern intelligence and accessible warmth.

*   **Display & Headlines (Manrope):** A modern, geometric sans-serif that feels authoritative yet approachable. Use large `display-lg` (3.5rem) settings for AI-driven insights to celebrate user milestones.
*   **Body & Labels (Inter):** Chosen for its exceptional legibility. Even at `body-sm`, the high x-height ensures clarity for users in any environment, from bright urban sunlight to low-light rural settings.

**Typographic Hierarchy as Identity:** 
High-end editorial design relies on dramatic scale. Don't be afraid of the gap between a `display-md` headline and a `body-md` description. This contrast creates a clear information hierarchy that feels curated rather than crowded.

---

## 4. Elevation & Depth: Atmospheric Layering
We move away from the "pasted on" look of traditional UI by using Tonal Layering and Ambient Shadows.

*   **The Layering Principle:** Depth is achieved by "stacking." A `surface-container-highest` card should never sit on a `surface-container-low` base; instead, use the adjacent tiers to create a natural, soft progression.
*   **Ambient Shadows:** If a floating effect is necessary (e.g., for a critical alert), use a shadow with a large blur (30px+) and low opacity (max 6%). The shadow color must be tinted with the `on-surface` (`#1c1c11`) value to mimic natural light.
*   **The "Ghost Border" Fallback:** If a border is required for accessibility, it must be a "Ghost Border": use the `outline-variant` token at **15% opacity**. 100% opaque borders are strictly forbidden as they interrupt the visual flow.

---

## 5. Components: Softness & Intent

### Buttons
*   **Primary:** Uses the signature `primary` to `primary-container` gradient. Corner radius is fixed at `md` (0.75rem).
*   **Secondary:** Ghost-style with `on-surface` text and a subtle `surface-container-high` background on hover. No borders.
*   **Action Chips:** High-legibility labels using `secondary` (`#9a442d`) for interactive states to provide warmth and clear affordance.

### Input Fields
*   **Structure:** Avoid "boxed" inputs. Use a slightly darker `surface-container` background with a `md` (0.75rem) corner radius. 
*   **Focus State:** Instead of a thick border, use a 2px glow of the `surface-tint` (`#006971`) with a soft blur.

### Cards & Lists
*   **The Rule of Zero Dividers:** Traditional horizontal lines are replaced by vertical whitespace (24px - 32px) or alternating background tones between `surface` and `surface-container-low`.
*   **AI Insight Cards:** These should use the Glassmorphic style with a subtle `secondary_container` accent on the top edge to denote AI-generated content.

### Specialty: The "Health Journey" Tracker
Instead of a linear progress bar, use an organic, fluid path that utilizes the `tertiary` (`#376651`) palette. This feels less like a "checklist" and more like a holistic progression.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical layouts for hero sections. Let an image or data visualization bleed off the edge of the screen to create a sense of scale.
*   **Do** prioritize "Breathing Room." If you think there is enough whitespace, add 8px more.
*   **Do** use `secondary` (`#9a442d`) sparingly as a "heartbeat" color—reserved for vital actions, alerts, or emotional highlights.

### Don’t:
*   **Don't** use pure black (`#000000`) or pure white (`#ffffff`) for anything other than specific high-contrast text or the `lowest` container tier.
*   **Don't** use standard 1px dividers. If content feels cluttered, increase the margin-bottom rather than adding a line.
*   **Don't** use sharp corners. Every interactive element must have at least the `DEFAULT` (0.5rem) rounding to maintain the "Soft Minimalism" aesthetic.

---
*Note: This design system is a living document intended to evolve with user feedback while maintaining its core commitment to serene, editorial elegance.*