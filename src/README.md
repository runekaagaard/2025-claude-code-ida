# Claude Code in Practice - Presentation

A clean, focused presentation with beautiful grey tones and orange accents. Each slide shows one concept with SSI for DRY structure.

## Design Philosophy

**One slide = One concept**
- Clean, centered layouts
- Beautiful grey color palette with orange highlights
- Generous whitespace
- Large, readable text
- Optional subtitle (h2) for content type

## Running the Presentation

```bash
cd src
python3 serve.py
```

Open `http://localhost:8000` in your browser.

## Structure

```
src/
├── _header.html              # SSI: Common header
├── _footer.html              # SSI: Common footer
├── serve.py                  # Python HTTP server with SSI support
├── index.html                # Slide navigation/overview
│
├── slide-00-title.html       # Title slide
├── slide-01-documentation.html
│
├── slide-02a-exploration.html          # Talk points
├── slide-02b-exploration-prompt.html   # Claude prompt
├── slide-02c-exploration-tooling.html  # Bash/Elisp code
│
├── slide-03a-planning.html             # Talk points
├── slide-03b-planning-prompt.html      # Claude prompt
├── slide-03c-planning-response.html    # Follow-up Q&A
│
├── slide-04a-build-root.html           # Talk points
├── slide-04b-build-root-prompt.html    # Claude prompt
├── slide-04c-build-root-feel.html      # Feel section
│
├── slide-05a-build-leaves.html         # Talk points
├── slide-05b-build-leaves-prompt.html  # Claude prompt
├── slide-05c-build-leaves-feel.html    # Feel section
│
├── slide-06a-cleanup.html              # Talk points
├── slide-06b-cleanup-prompt.html       # Claude prompt
├── slide-06c-cleanup-feel.html         # Feel section
│
├── slide-07a-ship-it.html              # Talk points
├── slide-07b-ship-it-prompt.html       # Claude prompt
├── slide-07c-ship-it-tooling.html      # clg() function
└── slide-07d-ship-it-feel.html         # Feel section
```

## Color Palette

- **Background**: `gray-950` with subtle grid pattern
- **Surface**: `gray-900` with `gray-800` borders
- **Text**: `gray-100` (primary), `gray-300` (body), `gray-500` (subtle)
- **Accent**: `claude-orange` (#D97757) for highlights, bullets, active states
- **Success**: `green-500` for checkmarks

## Typography

- **Headings**: Inter, bold, 5xl (title) / 2xl (subtitle)
- **Body**: Inter, xl-2xl for readability
- **Code**: JetBrains Mono, various sizes

## Navigation

- **Next/Prev buttons** in bottom-right corner
- **Index button** to return to overview
- Sequential flow through all slides

## SSI Usage

Each slide includes header and footer:

```html
<!--#include virtual="_header.html" -->

<!-- Slide content -->

<!--#include virtual="_footer.html" -->
```

The Python server processes these includes automatically.

## Slide Anatomy

### Title Slide
- Large gradient orange title
- Subtitle
- Clean, centered

### Content Slides
- **h1**: Main topic (e.g., "Exploration and Research")
- **h2** (optional): Content type (e.g., "Claude Prompt", "Feel", "Tooling")
- **Content**: Bullets, code blocks, or checkmarks
- **Navigation**: Bottom-right buttons

### Index Page
- Grouped by topic
- Shows slide numbering (00, 01, 02a, 02b, etc.)
- Orange highlights on hover

## Adding New Slides

1. Copy an existing slide as template
2. Update the h1 title
3. Add optional h2 subtitle
4. Add your content
5. Update prev/next navigation links
6. Add to index.html

## Typography Scale

- Title (h1): `text-5xl` (48px)
- Subtitle (h2): `text-2xl` (24px)
- Body bullets: `text-xl` (20px)
- Code: `text-base` to `text-lg` (16-18px)
