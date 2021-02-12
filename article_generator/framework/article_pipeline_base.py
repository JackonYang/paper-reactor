from jinja2 import Environment, FileSystemLoader
import re


continuous_spaces = [
    re.compile(r'\s+', re.DOTALL),
]


class ArticlePipelineBase:
    config_dir = None
    project_data_dir = None
    template_dir = None

    def __init__(self, config_dir, project_data_dir, template_dir, **kwargs):
        self.config_dir = config_dir
        self.project_data_dir = project_data_dir
        self.template_dir = template_dir

    def run(self):
        for task in self.iter_tasks():
            self.render_task_article(task)

    def render(self, template, filename=None, **kwargs):
        # output_dir = settings.output_dir
        # if not os.path.exists(output_dir):
        #     os.mkdir(output_dir)

        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template(template)

        # out_filename = os.path.join(output_dir, filename)

        content = template.render(**kwargs)

        # if filename:
        #     with codecs.open(out_filename, 'w', 'utf8') as f:
        #         f.write(content)
        #     print('success! saved in %s' % os.path.abspath(out_filename))

        return self.remove_spaces(content)

    def remove_spaces(self, text):
        for ptn in continuous_spaces:
            text = ptn.sub(' ', text)

        return text

    # API to be implemented
    # iter_tasks
