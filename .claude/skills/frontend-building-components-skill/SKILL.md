---
name: building-frontend-components-skill
description: This Skill equips Claude to construct frontend web elements including pages, reusable components, layouts, and styling. It provides structured guidance for generating HTML, CSS, and JavaScript code. Use this Skill when users request help with creating, modifying, or troubleshooting frontend UI elements, such as building a webpage layout, styling components, or implementing interactive features without backend integration.
---

# Building Frontend Components

## Overview
This Skill focuses on frontend development using core web technologies: HTML for structure, CSS for styling, and JavaScript for interactivity. Assume users may specify frameworks like React, Vue, or plain vanilla; default to vanilla unless stated.

Key principles:
- Semantic HTML for accessibility.
- Responsive design with media queries.
- Modular components for reusability.
- Progressive enhancement: Start with basics, add JS as needed.

See REFERENCE.md for common patterns, best practices, and resources.

## Workflow
1. **Understand Request**: Parse user query for specifics (e.g., page type, components needed, styling theme, interactivity).
   - Checklist:
     - Target output: Full page, single component, or snippet?
     - Technologies: HTML/CSS/JS only? Framework?
     - Constraints: Mobile-first? Accessibility? Browser compatibility?
     - Visuals: Colors, fonts, layouts (grid/flexbox)?

2. **Plan Structure**:
   - Sketch high-level outline (e.g., header, main, footer).
   - Identify components (e.g., button, card, navbar).
   - Decide layout: Flexbox, Grid, or floats as fallback.

3. **Generate Code**:
   - Start with HTML skeleton (use templates/basic-page.html as base).
   - Add CSS for styling (link to templates/styles.css for examples).
   - Implement JS for behavior (see templates/component-example.js).
   - Validate: Ensure no syntax errors; suggest tools like validators.

4. **Iterate and Refine**:
   - Handle errors: If code breaks, debug step-by-step (e.g., check console logs).
   - Test responsiveness: Describe media queries.
   - Optimize: Minify if requested.

5. **Output Format**:
   - Present code in fenced blocks with language labels.
   - Explain changes or rationale briefly.
   - If full project, suggest file structure.

## Step-by-Step Checklists

### Building a Page
- Define doctype and html tag.
- Add head: Title, meta charset/viewport, link to CSS.
- Body: Sections with semantic tags (article, section, etc.).
- Include JS script tag at end.

### Creating Components
- HTML: Use custom classes/IDs.
- CSS: Scoped selectors to avoid conflicts.
- JS: Event listeners for interactivity.

### Layout and Styling
- Layout: `display: flex;` or `grid-template-columns`.
- Styling: Colors via hex/rgb, fonts via family/stack.
- Responsiveness: `@media (max-width: 768px) { ... }`.

## Output Templates
For a simple component:

```html
<!-- component.html -->
<div class="my-component">
  <!-- Content -->
</div>
CSS/* styles.css */
.my-component {
  /* Styles */
}
JavaScript// script.js
document.querySelector('.my-component').addEventListener('click', () => {
  // Behavior
});
Examples
Input: "Build a responsive navbar with links."
Output:

HTML: Nav element with ul/li/a.
CSS: Flexbox for horizontal layout, media query for hamburger menu.
JS: Toggle menu on mobile.

Input: "Style a card component in blue theme."
Output:

HTML: Div with class "card".
CSS: Background blue, box-shadow, hover effects.