"""
Pyrsistence

Create simple persistent configuration classes

Basic usage:
    >>> from . import BaseConfig, Field
    >>> class MyConfig(BaseConfig):
    ...    filename = "my_config"
    ...    username: str = Field("user")
    ...    dob: datetime = Field("user")
    ...    email: str = Field("user")
"""

# Copyright (C) 2024, Jacob Sánchez Pérez

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA

import logging
import configparser
from typing import Any

from platformdirs import user_config_dir


class BaseConfigMetaclass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[type[Any], ...],
        attrs: dict[str, Any]
    ) -> type:
        if 'filename' not in attrs:
            # we cannot use a default because of different apps
            raise TypeError('Config must define a filename')
        ...

    #def __init__(self):
    #    ...

class BaseConfig(metaclass=BaseConfigMetaclass):
    filename = "my_config"
