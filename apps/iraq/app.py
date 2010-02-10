#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

""" this file is here just to prevent route from throwing errors on startup """

import rapidsms

class App(rapidsms.app.App):
    pass
