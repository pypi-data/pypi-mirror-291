import html2text
import html5_parser
from lxml import etree
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


def html_to_markdown_with_depth(html_content, max_depth):
    # Parse HTML using html5-parser
    document = html5_parser.parse(html_content)

    # Helper function to traverse the tree and convert to a string with limited depth
    def traverse_tree(node, current_depth):
        if current_depth > max_depth or not hasattr(node, 'tag'):
            return ""
        
        result = etree.tostring(node, encoding='unicode', method='html')
        
        # Recursively process child nodes
        for child in node:
            result += traverse_tree(child, current_depth + 1)
        
        return result

    # Start traversal from the root of the document
    limited_html = traverse_tree(document, 0)

    # Convert the limited HTML to Markdown
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False  # Keep links in the markdown
    markdown_text = text_maker.handle(limited_html)

    return markdown_text

def display_markdown_hierarchically(markdown_text, max_depth):
    console = Console()
    depth = 1

    def create_panel(text, current_depth):
        nonlocal depth
        if current_depth > max_depth:
            return None
        return Panel(Markdown(text,
            justify="left", code_theme="github-light" ),border_style="bold"
            , highlight=True, title=Text(
                style="bold underline blue ", text="Title", justify="left",
            ), title_align="center",
            subtitle="depth: " + str(current_depth), subtitle_align="center",
            style="on cyan1",
            padding=(0,1,1,1)
        )

    lines = markdown_text.splitlines()
    current_text = ""
    panels = []

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith("#"):
            if current_text:
                panels.append(create_panel(current_text, depth))
                current_text = ""
            depth = stripped_line.count("#")
        current_text += line + "\n"
    
    if current_text:
        panels.append(create_panel(current_text, depth))

    for panel in panels:
        if panel:
            console.print(panel)

if __name__ == "__main__":
    # Sample HTML content
    html_content = """
    <html>
        <head><title>Sample Page</title></head>
        <body>
            <h1>Heading 1</h1>
            <p>This is a <strong>sample</strong> paragraph with <a href="https://example.com">a link</a>.</p>
            <div>
                <h2>Subheading</h2>
                <ul>
                    <li>First item</li>
                    <li>Second item</li>
                </ul>
            </div>
            <footer>
                <p>Footer content</p>
            </footer>
        </body>
    </html>
    """

    max_depth = 3
    markdown_output = html_to_markdown_with_depth(html_content, max_depth)

    print("Markdown Output:")
    print(markdown_output)

    display_markdown_hierarchically(markdown_output, max_depth)