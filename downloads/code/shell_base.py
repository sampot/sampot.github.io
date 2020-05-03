# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import abstractmethod


class ShellBase(object):

    @abstractmethod
    def run(self):
        """ Starts up the shell.
        """
        pass

