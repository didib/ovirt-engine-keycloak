#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Constants."""


import gettext
import os

from otopi import util

from ovirt_engine_setup import constants as oesetupcons
from ovirt_engine_setup.constants import osetupattrsclass
from ovirt_engine_setup.engine import constants as oenginecons

from . import config

def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-setup')


@util.export
@util.codegen
class Const(object):
    OVIRT_ENGINE_KEYCLOAK_SETUP_PACKAGE_NAME = \
        'ovirt-engine-keycloak'


@util.export
@util.codegen
@osetupattrsclass
class ApacheEnv(object):
    HTTPD_CONF_OVIRT_ENGINE_KEYCLOAK = 'OVESETUP_APACHE/configFileOvirtEngineKeycloak'


@util.export
@util.codegen
class FileLocations(oesetupcons.FileLocations):
    PKG_DATA_DIR = config.PKG_DATA_DIR

    DIR_HTTPD = os.path.join(
        oesetupcons.FileLocations.SYSCONFDIR,
        'httpd',
    )

    HTTPD_CONF_OVIRT_ENGINE_KEYCLOAK = os.path.join(
        DIR_HTTPD,
        'conf.d',
        'z-ovirt-engine-keycloak-proxy.conf'
    )

    HTTPD_CONF_OVIRT_ENGINE_KEYCLOAK_TEMPLATE = os.path.join(
        PKG_DATA_DIR,
        'conf',
        'z-ovirt-engine-keycloak-proxy.conf.in',
    )

    OVIRT_ENGINE_SERVICE_CONFIG_KEYCLOAK = os.path.join(
        oenginecons.FileLocations.OVIRT_ENGINE_SERVICE_CONFIGD,
        '12-setup-keycloak.conf'
    )


