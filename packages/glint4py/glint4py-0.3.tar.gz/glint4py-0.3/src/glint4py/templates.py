import os

class TemplateRenderer:
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir

    def render(self, template_name, context):
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, 'r') as file:
            template = file.read()
        return template.format(**context)
