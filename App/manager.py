from typing import Any, Iterable, List
from django.db import models
from django.db.models.query import QuerySet


class TopicManager(models.Manager):
    exam_type = "Topic"
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(exam_type=self.exam_type)
    
    def create(self, **kwargs: Any) -> Any:
        kwargs['exam_type'] = self.exam_type
        return super().create(**kwargs)
    
    def bulk_create(self, objs: Iterable, *args, **kwargs) -> List:
        for obj in objs:
            obj.exam_type = self.exam_type
        return super().bulk_create(objs, *args, **kwargs)