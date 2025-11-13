#!/usr/bin/env python3
"""
Build presentation slides from thetalk.org
"""
import orgparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import re


def slugify(text):
    """Convert text to URL-friendly slug"""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def extract_bullets(body):
    """Extract bullet points from org-mode body"""
    if not body:
        return []
    bullets = []
    for line in body.strip().split('\n'):
        line = line.strip()
        if line.startswith('-'):
            bullets.append(line[1:].strip())
    return bullets


def extract_code_blocks(body):
    """Extract code blocks from org-mode body"""
    if not body:
        return []

    code_blocks = []
    pattern = r'#\+begin_src\s+(\w+)\n(.*?)#\+end_src'
    matches = re.findall(pattern, body, re.DOTALL)

    for lang, code in matches:
        code_blocks.append({
            'language': lang,
            'code': code.strip()
        })

    return code_blocks


def parse_org_file(org_path):
    """Parse org file and extract slide data"""
    root = orgparse.load(org_path)
    slides = []

    for node in root[1:]:  # Skip first node (file itself)
        if node.level == 1:  # Top-level headings
            # Check for special CLAUDE markers
            is_title_slide = '[CLAUDE:' in node.heading and 'Title type slide' in node.heading

            if is_title_slide:
                # Title slide - extract from body
                if node.body:
                    body_lines = [line.strip() for line in node.body.strip().split('\n') if line.strip()]
                    if body_lines:
                        # Check if it's a code-centered slide (like "npm install")
                        if 'npm' in body_lines[0] or 'install' in body_lines[0]:
                            slide = {
                                'title': None,
                                'subtitle': None,
                                'code': '\n'.join(body_lines),
                                'template': 'code_centered',
                                'slug': slugify(body_lines[0]),
                            }
                        else:
                            slide = {
                                'title': body_lines[0],
                                'subtitle': body_lines[1] if len(body_lines) > 1 else None,
                                'content': body_lines[2:] if len(body_lines) > 2 else [],
                                'template': 'title',
                                'slug': slugify(body_lines[0]),
                            }
                        slides.append(slide)
            else:
                # Regular section - check if it has subsections
                if node.children:
                    # Has subsections - create intro slide first if there's body content
                    intro_bullets = extract_bullets(node.body)
                    if intro_bullets:
                        slide = {
                            'title': node.heading,
                            'subtitle': None,
                            'content': intro_bullets,
                            'template': 'bullets',
                            'slug': slugify(node.heading),
                        }
                        slides.append(slide)

                    # Then create slide for each child
                    for child in node.children:
                        if child.level == 2:
                            # Check if child has code blocks
                            code_blocks = extract_code_blocks(child.body)
                            if code_blocks:
                                slide = {
                                    'title': node.heading,
                                    'subtitle': child.heading,
                                    'code_blocks': code_blocks,
                                    'template': 'code',
                                    'slug': slugify(f"{node.heading}-{child.heading}"),
                                }
                            else:
                                slide = {
                                    'title': node.heading,
                                    'subtitle': child.heading,
                                    'content': extract_bullets(child.body),
                                    'template': 'bullets',
                                    'slug': slugify(f"{node.heading}-{child.heading}"),
                                }
                            slides.append(slide)
                else:
                    # No subsections - create single slide
                    slide = {
                        'title': node.heading,
                        'subtitle': None,
                        'content': extract_bullets(node.body),
                        'template': 'bullets',
                        'slug': slugify(node.heading),
                    }
                    slides.append(slide)

    return slides


def build_slides(slides, output_dir):
    """Generate HTML files from slides"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader('templates'))

    # Generate filenames
    filenames = []
    for i, slide in enumerate(slides):
        filename = f"{slide['slug']}.html"
        # Handle duplicate slugs
        if filename in filenames:
            filename = f"{slide['slug']}-{i}.html"
        filenames.append(filename)

    # Generate each slide
    for i, (slide, filename) in enumerate(zip(slides, filenames)):
        template = env.get_template(f"{slide['template']}.html")

        # Add navigation and context
        slide['prev'] = filenames[i-1] if i > 0 else None
        slide['next'] = filenames[i+1] if i < len(filenames) - 1 else None
        slide['current_index'] = i
        slide['total_slides'] = len(slides)
        slide['all_slides'] = filenames

        # Render
        html = template.render(**slide)
        (output_path / filename).write_text(html)

    # Generate index
    index_template = env.get_template('index.html')
    index_html = index_template.render(
        slides=[(s['title'], f) for s, f in zip(slides, filenames)],
        first_slide=filenames[0] if filenames else 'index.html'
    )
    (output_path / 'index.html').write_text(index_html)

    # Copy styles
    import shutil
    if Path('src/styles.css').exists():
        shutil.copy('src/styles.css', output_path / 'styles.css')

    print(f"✓ Built {len(slides)} slides to {output_dir}/")
    return filenames


if __name__ == '__main__':
    slides = parse_org_file('thetalk.org')
    build_slides(slides, 'build')
