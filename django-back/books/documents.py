from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book

@registry.register_document
class BookDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    
    class Index:
        name = 'books'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'analyzer': {
                    'korean': {
                        'type': 'custom',
                        'tokenizer': 'nori_tokenizer',
                        'filter': ['nori_readingform', 'lowercase']
                    }
                }
            }
        }

    class Django:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'isbn',
            'publisher',
            'pub_date',
            'author',
            'author_info',
            'customer_review_rank',
            'subTitle'
        ]
        related_models = [Book.category.field.model]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Book.category.field.model):
            return related_instance.books.all()
