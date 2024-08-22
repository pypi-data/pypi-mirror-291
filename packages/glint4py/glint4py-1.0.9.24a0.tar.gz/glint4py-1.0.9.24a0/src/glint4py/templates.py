"""
Module for rendering templates in the Glint web framework.

This module defines the TemplateRenderer class, which is responsible
for rendering templates with a given context. Templates are read from
the file system and formatted using the provided context data.
"""

import os
from typing import Dict

class TemplateRenderer:
    """Renders templates with a given context.

    The TemplateRenderer class is used to load templates from the file
    system and render them with the provided context. The context is
    used to replace placeholders in the template with actual values.
    """

    def __init__(self, template_dir: str = "templates"):
        """Initializes the TemplateRenderer with the directory for templates.

        Args:
            template_dir (str, optional): The directory where template files
                                           are located. Defaults to "templates".
        """
        self.template_dir = template_dir
        self.template_cache = {}

    def _load_template(self, template_name: str) -> str:
        """Loads a template from the file system and caches it.

        Args:
            template_name (str): The name of the template file to load.

        Returns:
            str: The template content.

        Raises:
            FileNotFoundError: If the template file does not exist.
        """
        if template_name in self.template_cache:
            return self.template_cache[template_name]

        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.isfile(template_path):
            raise FileNotFoundError(
                f"Template file '{template_name}' not found in '{self.template_dir}'"
            )

        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            self.template_cache[template_name] = template_content
            return template_content
        except (OSError, IOError) as e:
            raise RuntimeError(f"Error reading template file '{template_name}'") from e

    def render(self, template_name: str, context: Dict[str, str]) -> str:
        """Renders a template with the given context.

        Args:
            template_name (str): The name of the template file to render.
            context (Dict[str, str]): A dictionary containing the context data to
                                      be used in the template. Keys in the dictionary
                                      are replaced with corresponding values in the
                                      template.

        Returns:
            str: The rendered template as a string with placeholders
                 replaced by values from the context.

        Raises:
            KeyError: If a placeholder in the template is not provided
                      in the context.
        """
        try:
            template = self._load_template(template_name)
            return template.format(**context)
        except KeyError as e:
            raise KeyError(f"Missing context key: {e}") from e
        except (ValueError, RuntimeError) as e:
            raise RuntimeError(f"Error rendering template '{template_name}': {e}") from e

    def add_template(self, template_name: str, template_content: str):
        """Adds a template directly to the cache.

        Args:
            template_name (str): The name of the template.
            template_content (str): The content of the template.
        """
        self.template_cache[template_name] = template_content

    def clear_cache(self):
        """Clears the template cache."""
        self.template_cache.clear()

    def list_templates(self) -> list:
        """Lists all template names currently in the cache.

        Returns:
            list: A list of template names.
        """
        return list(self.template_cache.keys())

    def set_template_dir(self, template_dir: str):
        """Sets a new directory for loading templates.

        Args:
            template_dir (str): The new directory for template files.
        """
        self.template_dir = template_dir
