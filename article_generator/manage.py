import os
import importlib


APP_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '.'))

PROJECT_ROOT = os.path.dirname(APP_ROOT)
PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, 'paper-data')

rules_dir = os.path.join(
    APP_ROOT, 'pipeline-rules'
)


def run_all():
    for rule_meta in load_rules():
        run_rule(rule_meta)


def load_rules():
    for t in os.listdir(rules_dir):
        yield {
            'name': t,
            'config_dir': os.path.join(rules_dir, t),
            'project_data_dir': PROJECT_DATA_DIR,
            'template_dir': os.path.join(APP_ROOT, 'templates'),
        }


def run_rule(rule_meta):
    rule_name = rule_meta['name']
    module_name = 'framework.%s' % rule_name
    module = importlib.import_module(module_name)
    classObj = getattr(module, rule_name)
    ret = classObj(**rule_meta).run()

    print(ret)


if __name__ == '__main__':
    run_all()
