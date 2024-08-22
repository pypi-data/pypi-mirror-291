# Copyright 2017 fmnisme@gmail.com christian@jonak.org
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# @author: Christian Jonak-Moechel, fmnisme, Tobias von der Krone
# @contact: christian@jonak.org, fmnisme@gmail.com, tobias@vonderkrone.info
# @summary: Python library for the Icinga 2 RESTful API

"""
Icinga 2 API client

The Icinga 2 API allows you to manage configuration objects and resources in a simple,
programmatic way using HTTP requests.
"""

from __future__ import print_function

import logging
from typing import Optional

import pretiac
from pretiac.actions import Actions
from pretiac.configfile import ClientConfigFile
from pretiac.events import Events
from pretiac.exceptions import PretiacException
from pretiac.objects import Objects
from pretiac.status import Status

LOG = logging.getLogger(__name__)


class Client:
    """
    Icinga 2 Client class
    """

    url: str

    username: Optional[str]

    password: Optional[str]

    timeout: Optional[int]

    certificate: Optional[str]

    key: Optional[str]

    ca_certificate: Optional[str]

    objects: Objects

    actions: Actions

    events: Events

    status: Status

    version: str

    def __init__(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: Optional[int] = None,
        certificate: Optional[str] = None,
        key: Optional[str] = None,
        ca_certificate: Optional[str] = None,
        config_file: Optional[str] = None,
    ) -> None:
        """
        initialize object
        """
        config = ClientConfigFile(config_file)
        if config_file:
            config.parse()
        url = url or config.url
        self.username = username or config.username
        self.password = password or config.password
        self.timeout = timeout or config.timeout
        self.certificate = certificate or config.certificate
        self.key = key or config.key
        self.ca_certificate = ca_certificate or config.ca_certificate
        self.objects = Objects(self)
        self.actions = Actions(self)
        self.events = Events(self)
        self.status = Status(self)
        self.version = pretiac.__version__

        if url:
            self.url = url
        else:
            raise PretiacException('No "url" defined.')
        if not self.username and not self.password and not self.certificate:
            raise PretiacException("Neither username/password nor certificate defined.")
