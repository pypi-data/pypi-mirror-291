import inspect
import os
import re
from typing import Any, Callable, Dict, List, Tuple, Union


def parse_google_docstring(docstring: str) -> Dict[str, Any]:
    """Parse a Google-style docstring into its components."""
    sections = {
        'description': '',
        'args': {},
        'returns': '',
        'examples': []
    }
    current_section = 'description'
    
    lines = docstring.split('\n')
    for line in lines:
        line = line.strip()
        if line.lower().startswith('args:'):
            current_section = 'args'
        elif line.lower().startswith('returns:'):
            current_section = 'returns'
        elif line.lower().startswith('examples:'):
            current_section = 'examples'
        elif ':' in line and current_section == 'args':
            param, desc = line.split(':', 1)
            sections['args'][param.strip()] = desc.strip()
        elif current_section == 'examples' and line.startswith('>>>'):
            sections['examples'].append(line)
        else:
            sections[current_section] += line + '\n'
    
    # Clean up sections
    for key in sections:
        if isinstance(sections[key], str):
            sections[key] = sections[key].strip()
    
    return sections

def get_relative_path(obj: type | Callable | object) -> str:
    """Get the relative path of the file containing the object."""
    try:
        module = inspect.getmodule(obj)
        if module is None:
            return "Unknown location"
        
        return os.path.relpath(inspect.getfile(module))
    except ValueError:
        return "Unknown location"

def generate_feature_list(description: str) -> str:
    """Generate a markdown list of features from the description."""
    features = re.findall(r'- (.*)', description)
    if not features:
        return ""
    
    markdown = "<p><strong>Key features</strong></p>\n\n<ul>\n"
    for feature in features:
        markdown += f"<li>{feature}</li>\n"
    markdown += "</ul>\n"
    return markdown

def generate_examples(examples: List[str]) -> str:
    """Generate a markdown code block with examples."""
    if not examples:
        return ""
    
    markdown = "<p><strong>Usage example</strong></p>\n\n<pre><code>\n"
    for example in examples:
        markdown += f"{example}\n"
    markdown += "</code></pre>\n"
    return markdown

def generate_method_list(methods: List[Tuple[str, Dict[str, Any]]]) -> str:
    """Generate a markdown list of methods with their descriptions."""
    if not methods:
        return ""
    
    markdown = "<p><strong>Methods</strong></p>\n\n<ul>\n"
    for method_name, method_doc in methods:
        args = ', '.join(method_doc['args'].keys())
        first_sentence = method_doc['description'].split('.')[0]
        markdown += f"<li>`{method_name}({args})`: {first_sentence}</li>\n"
    markdown += "</ul>\n"
    return markdown

def generate_docs(obj: type | Callable | object) -> str:
    """Generate markdown documentation for a given object (class, function, or module).
    
    Args:
    obj: The object to document
    
    Returns:
    str: Markdown formatted documentation
    """
    if inspect.isclass(obj):
        return generate_class_docs(obj)
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        return generate_function_docs(obj)
    if inspect.ismodule(obj):
        return generate_module_docs(obj)
    return f"Unsupported object type: {type(obj)}"

def generate_class_docs(cls: type) -> str:
    """Generate markdown documentation for a class."""
    class_name = cls.__name__
    class_doc = cls.__doc__ or "No class description available."
    parsed_class_doc = parse_google_docstring(class_doc)
    
    file_path = get_relative_path(cls)
    
    methods = []
    for name, member in inspect.getmembers(cls):
        if inspect.isfunction(member) or inspect.ismethod(member) and not name.startswith('_'):
                method_doc = inspect.getdoc(member) or "No description available."
                parsed_method_doc = parse_google_docstring(method_doc)
                methods.append((name, parsed_method_doc))
    
    return f"""
## {class_name}

<details id="{class_name.lower()}">
<summary>{class_name}</summary>

<p>Defined in: <code>{file_path}</code></p>

<p>{parsed_class_doc['description']}</p>

{generate_feature_list(parsed_class_doc['description'])}

{generate_examples(parsed_class_doc['examples'])}

{generate_method_list(methods)}

<p>The `{class_name}` class provides functionality for {parsed_class_doc['description'].split('.')[0].lower()}.</p>

</details>
"""

def generate_function_docs(func: Callable) -> str:
    """Generate markdown documentation for a function or method."""
    func_name = func.__name__
    func_doc = func.__doc__ or "No function description available."
    parsed_func_doc = parse_google_docstring(func_doc)
    
    file_path = get_relative_path(func)
    
    ', '.join(parsed_func_doc['args'].keys())
    
    markdown = f"""
## {func_name}

<details id="{func_name.lower()}">
<summary>{func_name}</summary>

<p>Defined in: <code>{file_path}</code></p>

<p>{parsed_func_doc['description']}</p>

<p><strong>Args:</strong></p>
<ul>
"""

    for arg, desc in parsed_func_doc['args'].items():
        markdown += f"<li>`{arg}`: {desc}</li>\n"

    markdown += f"""
</ul>

<p><strong>Returns:</strong></p>
<p>{parsed_func_doc['returns']}</p>

{generate_examples(parsed_func_doc['examples'])}

</details>
"""

    return markdown

def generate_module_docs(module: object) -> str:
    """Generate markdown documentation for a module."""
    module_name = module.__name__
    module_doc = module.__doc__ or "No module description available."
    parsed_module_doc = parse_google_docstring(module_doc)
    
    file_path = get_relative_path(module)
    
    markdown = f"""
# Module: {module_name}

<p>Defined in: <code>{file_path}</code></p>

<p>{parsed_module_doc['description']}</p>

{generate_feature_list(parsed_module_doc['description'])}

{generate_examples(parsed_module_doc['examples'])}

## Contents

"""

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            if not name.startswith('_'):  # Exclude private members
                markdown += f"- [{name}](#{name.lower()})\n"
    
    markdown += "\n"

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            if not name.startswith('_'):  # Exclude private members
                markdown += generate_docs(obj) + "\n"

    return markdown
