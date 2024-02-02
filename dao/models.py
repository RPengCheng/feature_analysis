# coding=utf-8
from tortoise import Model,fields
class Todo(Model):
    """数据库中的表todo"""
    id = fields.IntField(pk=True)
    contest = fields.CharField(max_length=500)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)