# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#

class User:
    def __init__(self, name: str, email: str = None):
        self.name = name
        self.email = email

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
