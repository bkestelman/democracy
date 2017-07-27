from django_elasticsearch_dsl import DocType, Index
from .models import Question

# Name of the Elasticsearch index
question = Index('questions')
question.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@question.doc_type
class QuestionDocument(DocType):
    class Meta:
        model = Question

        # The fields to index in Elasticsearch
        fields = [
            'question_text',
        ]

