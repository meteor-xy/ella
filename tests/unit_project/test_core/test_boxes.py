# -*- coding: utf-8 -*-
from djangosanetesting import UnitTestCase, DatabaseTestCase

from django.contrib.sites.models import Site

from ella.core.models import Category, Publishable
from ella.core.templatetags.core import _parse_box, BoxNode
from ella.core.box import Box

from unit_project.test_core import create_basic_categories, create_and_place_a_publishable

class TestBoxTagParser(UnitTestCase):
    def test_parse_box_with_pk(self):
        node = _parse_box([], ['box', 'box_type', 'for', 'core.category', 'with', 'pk', '1'])
        self.assert_true(isinstance(node, BoxNode))
        self.assert_equals('box_type', node.box_type)
        self.assert_equals(Category, node.model)
        self.assert_equals(('pk', '1'), node.lookup)

    def test_parse_box_for_varname(self):
        node = _parse_box([], ['box', 'other_box_type', 'for', 'var_name'])
        self.assert_true(isinstance(node, BoxNode))
        self.assert_equals('other_box_type', node.box_type)
        self.assert_equals('var_name', node.var_name)

    def test_parse_box_with_slug(self):
        node = _parse_box([], ['box', 'box_type', 'for', 'sites.site', 'with', 'slug', '"home"'])
        self.assert_true(isinstance(node, BoxNode))
        self.assert_equals('box_type', node.box_type)
        self.assert_equals(Site, node.model)
        self.assert_equals(('slug', '"home"'), node.lookup)

class TestPublishableBox(DatabaseTestCase):
    def setUp(self):
        super(TestPublishableBox, self).setUp()
        create_basic_categories(self)
        create_and_place_a_publishable(self)

    def test_box_template_path(self):
        publishable = Publishable.objects.get(pk=1)
        article = publishable.target

        box_publishable = publishable.Box('box_type', [])
        box_article = Box(article, 'box_type', [])

        template_list = [
            'box/category/nested-category/content_type/articles.article/first-article/box_type.html',
            'box/category/nested-category/content_type/articles.article/box_type.html',
            'box/category/nested-category/content_type/articles.article/box.html',
            'box/content_type/articles.article/first-article/box_type.html',
            'box/content_type/articles.article/box_type.html',
            'box/content_type/articles.article/box.html',
            'box/box_type.html',
            'box/box.html',
        ]

        self.assert_equals(template_list, box_publishable._get_template_list())
        self.assert_equals(template_list, box_article._get_template_list())


