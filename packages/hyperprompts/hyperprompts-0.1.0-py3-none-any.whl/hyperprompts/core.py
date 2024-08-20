import inspect
from textwrap import dedent
from typing import List, Callable, Tuple, Any
import re

def extract_placeholders(text: str) -> List[str]:
    return re.findall(r'\{(\w+)\}', text)

class Prompt:
    def __init__(self, func: Callable):
        self.func = func
        self.signature = inspect.signature(func)

    def __call__(self, **inputs) -> Tuple[str, List[str]]:
        # Get the source code of the function
        source = inspect.getsource(self.func)
        
        # Extract the function body
        function_body = self.extract_function_body(source)
        
        # Create a new namespace and add input parameters
        namespace = inputs.copy()
        
        # Execute the function body in this namespace
        exec(function_body, namespace)
        
        # Filter out function parameters and built-in variables
        filtered_locals = {k: v for k, v in namespace.items() 
                           if k not in inputs and not k.startswith('__')}
        
        placeholders = []
        template_parts = []
        for text in filtered_locals.values():
            if isinstance(text, str):
                placeholders.extend(extract_placeholders(text))
                template_parts.append(dedent(text))
        
        template = "\n".join(template_parts)
        return template, list(set(placeholders))

    @staticmethod
    def extract_function_body(source: str) -> str:
        lines = source.split('\n')
        # Find the line where the function body starts
        body_start = next(i for i, line in enumerate(lines) if line.strip().endswith(':'))
        # Extract the function body, including nested functions if any
        body_lines = lines[body_start + 1:]
        min_indent = min(len(line) - len(line.lstrip()) for line in body_lines if line.strip())
        return '\n'.join(line[min_indent:] for line in body_lines)

# Decorator to automatically wrap the function
def hyperprompt(func):
    return Prompt(func)