# Navigation Microservice

## Overview
The navigation menu has been architected as a reusable microservice that can be consumed by any page in the application. This follows the same pattern as the contact microservices using the linked list structure.

## Architecture

### Endpoints

#### HTML Component
```
GET /nav
```
Returns the navigation menu as an HTML component with embedded JavaScript for mobile menu functionality.

**Response Type:** `text/html`

**Example:**
```html
<nav class="navbar">
    <div class="container">
        <div class="nav-brand">
            <a href="/">SAVANTLAB</a>
        </div>
        <button class="nav-toggle" aria-label="Toggle navigation">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <div class="nav-links">
            <a href="/#research">Research</a>
            <a href="/#projects">Projects</a>
            <a href="/counterterrorism">Counterterrorism</a>
            <a href="/reading">Reading</a>
            <a href="/journal">Journal</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </div>
    </div>
</nav>
<script>
    // Mobile menu toggle JavaScript
</script>
```

#### JSON Data
```
GET /api/navigation
```
Returns navigation links data as JSON.

**Response Type:** `application/json`

**Example Response:**
```json
{
  "links": [
    {"label": "Research", "url": "/#research"},
    {"label": "Projects", "url": "/#projects"},
    {"label": "Counterterrorism", "url": "/counterterrorism"},
    {"label": "Reading", "url": "/reading"},
    {"label": "Journal", "url": "/journal"},
    {"label": "About", "url": "/about"},
    {"label": "Contact", "url": "/contact"}
  ]
}
```

## Usage

### In Templates
Every page template loads the navigation microservice using this pattern:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation Microservice -->
    <div id="nav-container"></div>

    <!-- Page content -->
    
    <script>
        // Load navigation microservice
        fetch('/nav')
            .then(response => response.text())
            .then(html => {
                document.getElementById('nav-container').innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading navigation:', error);
            });
    </script>
</body>
</html>
```

### Key Points
1. **Placeholder container**: `<div id="nav-container"></div>` is where the navigation loads
2. **Fetch on load**: JavaScript fetches the HTML from `/nav` endpoint
3. **Inject HTML**: Response is injected into the container
4. **Self-contained**: The nav component includes its own mobile menu JavaScript

## Features

### Mobile Responsive
- **Desktop**: Horizontal menu with full links
- **Mobile**: Hamburger menu (≤768px screens)
- **Smooth animations**: Menu slides in from right on mobile
- **Auto-close**: Menu closes when a link is clicked

### Styling
The navigation uses CSS classes from `style.css`:
- `.navbar` - Main navigation container
- `.nav-brand` - Logo/brand link
- `.nav-toggle` - Hamburger button (hidden on desktop)
- `.nav-links` - Navigation links container

## Benefits

### 1. Single Source of Truth
- Navigation menu is defined in one place: `templates/nav_menu.html`
- Changes to menu items automatically propagate to all pages
- No duplication of HTML code

### 2. Microservice Pattern
- Navigation can be consumed by any page or external application
- Clear API contract (`/nav` and `/api/navigation`)
- Follows the same architecture as contact microservices

### 3. Maintainability
- Update navigation in one file
- All pages automatically receive updates
- Easier to test and debug

### 4. Performance
- Browser caches the component
- Reduces page size (no repeated nav HTML)
- Parallel loading with page content

## Implementation Files

### Templates
- `templates/nav_menu.html` - Navigation component template
- All page templates - Load nav from microservice

### Backend
- `app.py:nav_component()` - Serves HTML component at `/nav`
- `app.py:api_navigation()` - Serves JSON data at `/api/navigation`

### Styles
- `static/css/style.css` - Navigation and mobile menu styles

## Future Enhancements

### Possible Extensions
1. **Active state**: Highlight current page in navigation
2. **Dynamic loading**: Load nav links from database
3. **User-specific**: Show different menus for different users
4. **A/B testing**: Serve different navigation variants
5. **Analytics**: Track navigation usage patterns

## Comparison to Contact Microservices

| Feature | Contact Microservices | Navigation Microservice |
|---------|----------------------|-------------------------|
| Data Structure | Linked List | Array/List |
| API Endpoints | `/api/contact/*` | `/nav`, `/api/navigation` |
| HTML Component | Individual templates | Single template |
| Navigation | Previous/Next nodes | N/A |
| State Management | Node traversal | Stateless |

Both follow microservice principles:
- **Encapsulation**: Self-contained functionality
- **API-driven**: Clear endpoint contracts
- **Reusable**: Can be consumed by multiple clients
- **Maintainable**: Single source of truth

## Testing

### Manual Testing
1. Visit any page (e.g., `/about`, `/contact`, `/`)
2. Verify navigation menu loads
3. Test mobile responsiveness (resize browser or use DevTools)
4. Test hamburger menu on mobile
5. Verify all links work

### API Testing
```bash
# Test HTML endpoint
curl http://localhost:5001/nav

# Test JSON endpoint
curl http://localhost:5001/api/navigation
```

## Deployment Notes

When deploying:
1. Ensure `templates/nav_menu.html` is included
2. Verify `/nav` endpoint is accessible
3. Test mobile menu on actual mobile devices
4. Check CORS settings if serving from different domain
5. Monitor performance of navigation loading

---

**Architecture Pattern**: Microservices  
**Status**: Production Ready  
**Last Updated**: December 2025
