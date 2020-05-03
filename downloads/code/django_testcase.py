# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.test')

import time

from django.core import signals
from django.test.testcases import LiveServerTestCase, TestCase
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.handlers import StaticFilesHandler


class FunctionalTest(LiveServerTestCase, TestCase):
    static_handler = StaticFilesHandler

    @classmethod
    def setUpClass(cls):
        """
        Django's LiveServerTestCase setupClass but without sqlite :memory check
        and with additional Ghost initialization.
        """
        default_address = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8090-9000')
        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = default_address
        # Prevents transaction rollback errors from the server thread. Removed
        # as from Django 1.8.
        try:
            from django.db import close_connection
            signals.request_finished.disconnect(close_connection)
        except ImportError:
            pass
        super(FunctionalTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Django's LiveServerTestCase tearDownClass, but without sqlite :memory
        check and shuts down the Ghost instance.
        """
        super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='demo',
            password='demo',
            email='demo@localhost'
        )
        super(FunctionalTest, self).setUp()

    def tearDown(self):
        super(FunctionalTest, self).tearDown()

    def sleep(self, secs):
        time.sleep(secs)

