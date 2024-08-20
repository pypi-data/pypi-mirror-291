<div align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/dark_background_logo.svg">
  <img alt="hyperprompt" src="assets/light_background_logo.svg" width=700">
</picture></div>


**`hyperprompt`** is a lightweight Python package designed for creating dynamic and customizable text templates using Pythonic logic. 

With hyperprompt, you define meta-prompts using pure Python, compile them with configuration inputs to produce templates with placeholders, and then compile these templates with actual data to generate the final output.

## Installation

Install hyperprompt using pip:

```bash
pip install hyperprompt
```

## Features

* 🚀 **Pythonic and Intuitive**: Define meta-prompts using standard Python functions and control structures.
* 🛠️ **Conditional Logic**: Leverage Python's control flow to create dynamic and context-aware templates.

## Usage Example
### Defining the Meta-Prompt
```python
from hyperprompt import hyperprompt

# Step One: Define the meta-prompt
@hyperprompt
def greeting_template(user_role: str, language: str):
    match language:
        case "English":
            greeting = "Hello, {name}!"
        case "Spanish":
            greeting = "¡Hola, {name}!"    
    
    role_info = "You have {tasks} tasks pending" if user_role == "admin" else None
    footer = "Have a great day!"
```
### Compiling
```python
template, placeholders = greeting_template(user_role="admin", language="English")
print(placeholders) # ['name', 'tasks']

final_prompt = template.format(name="Alice", tasks="5")
print(final_prompt) # Hello, Alice! You have 5 tasks pending. Have a great day!

template, placeholders = greeting_template(user_role="user", language="Spanish")
print(placeholders) # ['name']

final_prompt = template.format(name="Carlos") 
print(final_prompt) # Hello, Carlos! Have a great day!
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.