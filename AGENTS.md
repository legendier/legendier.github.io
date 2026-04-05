# Agent Guidelines for This Repository

This is a static resume website with HTML, CSS, and vanilla JavaScript. There is no build system, test framework, or linter configured.

## Project Structure

```
/                   # Root directory
├── index.html      # Main HTML file
├── css/
│   └── style.css   # All styles
├── js/
│   └── main.js     # All JavaScript (particle effects, animations)
├── images/
│   └── avatar.svg  # Profile image
└── AGENTS.md      # This file
```

## Build / Run Commands

This is a static site with no build process. Open `index.html` directly in a browser to view.

- **View locally**: Open `index.html` in any browser
- **Serve with live reload**: Use a simple server like `npx serve .` or VS Code Live Server extension
- **No tests**: This project has no test suite
- **No linting**: No ESLint or Prettier configured

## Code Style Guidelines

### General Principles

- Keep files simple and readable
- Use semantic HTML elements
- Avoid over-abstraction; this is a single-page site
- Comment complex logic briefly where helpful

### HTML (index.html)

- Use semantic tags (`<aside>`, `<main>`, `<section>`, `<footer>`)
- Include proper meta tags: charset, viewport, description
- External resources (fonts, icons) from CDN
- Use accessible attributes: `alt` text for images
- Keep inline styles minimal; prefer CSS classes

### CSS (css/style.css)

- Use CSS variables for colors if adding new ones
- Follow existing naming: lowercase with hyphens (`.glass-card`, `.fade-up`)
- Use Flexbox and CSS Grid for layout
- Include fallback fonts if needed
- Keep responsive breakpoints aligned with existing ones (`@media (max-width: 880px)`)
- Use `rem` for spacing and sizing
- Group related styles together

### JavaScript (js/main.js)

- Wrap code in IIFE: `(function() { ... })();` to avoid global pollution
- Use `const` / `let`; avoid `var`
- Use semantic variable names (`particles`, `animationId`, `mouseX`)
- Add null checks for DOM elements before use
- Use `addEventListener` instead of inline handlers
- Keep functions focused and reasonably sized
- Handle edge cases (e.g., check if canvas context exists)
- Use modern ES6+ syntax

### Naming Conventions

- CSS classes: kebab-case (`.scroll-indicator`, `.progress-fill`)
- JavaScript: camelCase (`resizeCanvas`, `initParticles`)
- Constants: UPPER_SNAKE_CASE (`PARTICLE_COUNT`, `CONNECT_DIST`)
- IDs: kebab-case (matches CSS pattern)

### Error Handling

- Check if DOM elements exist before manipulating (`if (glow)`, `if (!ctx) return`)
- Use try-catch for any async operations
- Log meaningful messages to console for debugging

### Performance Considerations

- Use `requestAnimationFrame` for animations
- Pause canvas animations when tab is hidden (already implemented with visibility API)
- Limit particle count and connection distance to reasonable values

## Adding New Features

When modifying this resume:

1. **HTML**: Add new sections following the glass-card pattern
2. **CSS**: Add styles in appropriate section, maintain color consistency (`#0ff` for cyan accent)
3. **JS**: Add new logic in a new section with clear comments

## Common Tasks

- **Add new skill**: Add HTML element in skills section + CSS for progress bar
- **Add new project**: Add card in projects grid
- **Update contact info**: Edit text in index.html sidebar
- **Change color scheme**: Update CSS variables and color values (mainly cyan `#0ff`)

## Important Notes

- This is a personal resume site - maintain the professional yet creative aesthetic
- The particle canvas effect is a signature visual element - preserve it
- Mobile responsive design is already implemented - test any changes on mobile breakpoint

## Code Patterns from This Project

### JavaScript - Canvas Particle System

The particle system in `js/main.js` demonstrates several patterns:

- **Constants at top**: `const PARTICLE_COUNT = 85`, `const CONNECT_DIST = 150`
- **Init function pattern**: Separate `initParticles()` from `drawParticles()`
- **Animation loop**: Use `requestAnimationFrame` and store `animationId` for cancellation
- **Resize handling**: Debounce or directly call resize with `window.addEventListener('resize', ...)`
- **Mouse tracking**: Track with `mousemove`, clear on `mouseleave` using null values

```javascript
// Proper pattern for canvas initialization
const canvas = document.getElementById('particle-canvas');
const ctx = canvas.getContext('2d');
if (!ctx) return; // Early exit if canvas not available
```

### CSS - Glass Card Pattern

The signature glass-morphism effect uses:

```css
.glass-card {
    background: rgba(12, 20, 28, 0.75);
    backdrop-filter: blur(12px);
    border-radius: 2rem;
    border: 1px solid rgba(0, 255, 255, 0.25);
    box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
```

When adding new cards, maintain this pattern with cyan (`#0ff`) accent color.

### HTML - Section Template

New sections should follow:

```html
<div class="glass-card section-card fade-up">
    <div class="section-title">
        <i class="fas fa-icon"></i>
        <span>Section Name</span>
    </div>
    <!-- Content here -->
</div>
```

## Common Pitfalls to Avoid

1. **Canvas not visible**: Ensure z-index is lower than content (`z-index: 0` with `pointer-events: none`)
2. **Memory leaks**: Always `cancelAnimationFrame` when leaving page, use visibility API
3. **Mobile performance**: Disable heavy canvas effects below 880px breakpoint
4. **Inline styles**: Avoid in HTML; use CSS classes instead (existing inline styles in HTML are legacy)
5. **Hardcoded colors**: Use `#0ff` for cyan accent; don't introduce random new colors

## Version Control

- This is a simple static site - no CI/CD pipeline
- No automated tests to run
- Before deploying, manually verify in browser and check mobile responsiveness