#!/usr/bin/env python3
"""
Build presentation slides from thetalk.org
Uses org-python to convert org-mode to HTML
"""
import orgparse
from orgpython import to_html
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import re

def slugify(text):
    """Convert text to filename"""
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.lower().replace(' ', '-')
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def autolink_urls(html):
    """Convert plain URLs to <a> tags"""
    url_pattern = r'(?<!href=")(?<!src=")(https?://[^\s<]+)'
    return re.sub(url_pattern, r'<a href="\1">\1</a>', html)

def org_body_to_html(body):
    """Convert org-mode body to clean semantic HTML"""
    if not body:
        return ""

    # Convert org to HTML
    html = to_html(body, toc=False, highlight=False)

    # Autolink URLs
    html = autolink_urls(html)

    return html

def parse_grid_items(body):
    """Parse grid items (format: - Name: Description)"""

    items = []
    for line in body.strip().split('\n'):
        line = line.strip()
        if line.startswith('- ') and ':' in line:
            content = line[2:].strip()
            parts = content.split(':', 1)
            if len(parts) == 2:
                items.append({'name': parts[0].strip(), 'description': parts[1].strip()})

    return items

def parse_images_property(images_prop):
    """Parse IMAGES property: img1.jpg|Caption 1;img2.jpg|Caption|Subcaption"""
    if not images_prop:
        return []

    images = []
    for img_spec in images_prop.split(';'):
        img_spec = img_spec.strip()
        if not img_spec:
            continue

        parts = img_spec.split('|')
        if len(parts) >= 2:
            src = parts[0].strip()
            captions = [p.strip().strip('"') for p in parts[1:]]

            image = {
                'src': src,
                'alt': captions[0] if captions else '',
                'caption_main': captions[0] if captions else None,
                'caption_italic': captions[0].startswith('"') if captions else False,
                'caption_sub': captions[1] if len(captions) > 1 else None,
            }
            images.append(image)

    return images

def convert_timeline_to_html(body):
    """Convert org bullets with years to timeline HTML"""
    if not body:
        return ""

    html_parts = []
    for line in body.strip().split('\n'):
        line = line.strip()
        if line.startswith('- '):
            content = line[2:].strip()
            # Check if line starts with a year
            match = re.match(r'^(\d{4}s?)\s+(.+)$', content)
            if match:
                year, text = match.groups()
                html_parts.append(f'<div class="timeline-item">'
                                  f'<span class="timeline-year">{year}</span>'
                                  f'<p>{text}</p>'
                                  f'</div>')
            else:
                html_parts.append(f'<p>{content}</p>')

    return '\n'.join(html_parts)

def process_node(node, parent_slug='', is_first_child=False):
    """Process a single org node and return slide data"""
    heading = node.heading.strip()

    # Handle title slides
    if '[CLAUDE:' in heading and 'title' in heading.lower():
        if node.body:
            body_lines = [line.strip() for line in node.body.strip().split('\n') if line.strip()]
            if body_lines:
                return [{
                    'title': body_lines[0],
                    'subtitle': body_lines[1] if len(body_lines) > 1 else None,
                    'template': 'title',
                    'filename': slugify(body_lines[0]) + '.html',
                }]
        return []

    clean_heading = re.sub(r'\[CLAUDE:.*?\]', '', heading).strip()
    section_slug = slugify(clean_heading)
    has_body = bool(node.body and node.body.strip())

    # Get template and images from properties
    template = node.properties.get('TEMPLATE', '').lower() if node.properties else ''
    images_prop = node.properties.get('IMAGES', '') if node.properties else ''
    images = parse_images_property(images_prop)

    # Determine filename
    if parent_slug and is_first_child and not has_body:
        filename = f"{parent_slug}.html"
    elif parent_slug:
        filename = f"{parent_slug}-{section_slug}.html"
    else:
        filename = f"{section_slug}.html"

    # Common slide data
    slide_data = {
        'title': clean_heading if node.level == 1 else parent_slug.replace('-', ' ').title(),
        'subtitle': clean_heading if node.level == 2 else None,
        'images': images,
        'filename': filename,
    }

    # Process based on template type
    if template == 'title':
        # Title template with code or content
        slide_data['html_content'] = org_body_to_html(node.body)
        slide_data['template'] = 'title'
        slide_data['images'] = []  # No images for title slides

    elif template == 'evolution':
        # Evolution template with timeline
        slide_data['html_content'] = convert_timeline_to_html(node.body)
        slide_data['template'] = 'evolution'

    elif template == 'grid':
        # Grid template for batteries-style layouts
        slide_data['items'] = parse_grid_items(node.body)
        slide_data['template'] = 'grid'

    elif has_body:
        # Default template for most slides
        slide_data['html_content'] = org_body_to_html(node.body)
        slide_data['template'] = 'default'

    else:
        return []

    return [slide_data]

def parse_org_file(org_path):
    """Parse org file and extract slides"""
    root = orgparse.load(org_path)
    slides = []

    for node in root[1:]:
        if node.level == 1:
            # Process level 1 node
            slides.extend(process_node(node))

            # Process subsections (level 2)
            if node.children:
                parent_slug = slugify(re.sub(r'\[CLAUDE:.*?\]', '', node.heading.strip()).strip())
                is_first = True
                for child in node.children:
                    if child.level == 2:
                        slides.extend(process_node(child, parent_slug, is_first))
                        is_first = False

    return slides

def build_slides(slides, output_dir):
    """Generate HTML files"""
    output_path = Path(output_dir)

    env = Environment(loader=FileSystemLoader('templates'))
    filenames = [slide['filename'] for slide in slides]

    for i, slide in enumerate(slides):
        template = env.get_template(f"{slide['template']}.html")

        slide['prev'] = filenames[i - 1] if i > 0 else None
        slide['next'] = filenames[i + 1] if i < len(filenames) - 1 else None
        slide['all_slides'] = filenames

        html = template.render(**slide)
        (output_path / slide['filename']).write_text(html)

    # Index
    index_template = env.get_template('index.html')
    index_html = index_template.render(
        slides=[(s.get('title', s.get('subtitle', 'Slide')), s['filename']) for s in slides],
        first_slide=filenames[0] if filenames else 'index.html')
    (output_path / 'index.html').write_text(index_html)

    print(f"✓ Built {len(slides)} slides")

if __name__ == '__main__':
    slides = parse_org_file('thetalk.org')
    build_slides(slides, 'build')
