# Frontend Refresh Design

## Goal

Upgrade the Flask UI from a plain prototype into a polished assistive-tech product interface and remove debug-image output from the user-facing result page.

## Scope

- Keep the app flow unchanged.
- Redesign the upload page and result page with stronger layout, typography, spacing, and visual hierarchy.
- Remove debug artifact images from the rendered result page.
- Keep only recognized text, translated Yoruba text, speech controls, and recognition metadata visible to the user.

## Visual Direction

- Product-style interface rather than academic demo styling.
- Bright layered panels on top of a gradient background.
- High contrast with large controls and readable text.
- Responsive layout that collapses cleanly on mobile.

## Result Page Content

- Recognized English text
- Yoruba text used for speech
- Audio player
- Recognition metadata such as cell count, confidence, and speech mode
- No debug image gallery

## Implementation Notes

- Use a shared stylesheet for both pages.
- Add lightweight structural classes in the templates rather than JavaScript.
- Preserve accessibility with visible focus states and clear button contrast.
