# Claude Code in Practice - Presentation

Programmatic slide generation from org-mode source.

## Quick Start

```bash
# Build slides
make build

# Serve presentation
make serve

# Clean build directory
make clean
```

## How it Works

1. **Source**: `thetalk.org` - Org-mode file with presentation content
2. **Parser**: `build.py` - Parses org-mode and generates HTML using Jinja2
3. **Templates**: `templates/*.html` - Jinja2 templates for different slide types
4. **Output**: `build/*.html` - Generated presentation slides
5. **Server**: `server.py` - FastAPI server to serve static files

## Org-Mode Structure

### Title Slides

```org
* [CLAUDE: Title type slide]
Main Title
Subtitle
```

### Bullet Point Slides

```org
* Slide Title
- Bullet point 1
- Bullet point 2
- Bullet point 3
```

### Subsections

```org
* Main Section
** Subsection Title
- Subsection bullet 1
- Subsection bullet 2
```

## Template Types

- `title.html` - Centered title slides
- `bullets.html` - Standard bullet point slides
- `index.html` - Auto-redirect to first slide

## Navigation

- Prev/Next buttons automatically generated
- Index always redirects to first slide
- Clean URLs based on slide titles

## Development

```bash
# Install dependencies
uv add orgparse fastapi jinja2 uvicorn

# Run build
python build.py

# Start server
uv run uvicorn server:app --reload --port 8000
```

Server runs at: http://localhost:8000
