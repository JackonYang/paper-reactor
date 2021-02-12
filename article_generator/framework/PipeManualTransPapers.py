import os

from .article_pipeline_base import ArticlePipelineBase


class PipeManualTransPapers(ArticlePipelineBase):

    def iter_tasks(self):
        input_data_dir = os.path.join(
            self.config_dir, 'manual-trans-files'
        )
        for fname in os.listdir(input_data_dir):
            yield fname

    def load_task_papers(self):
        pass
