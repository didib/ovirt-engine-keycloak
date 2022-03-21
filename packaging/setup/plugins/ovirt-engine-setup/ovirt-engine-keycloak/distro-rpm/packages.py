#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""
Package upgrade plugin.
"""

import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.keycloak import constants as okkcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-keycloak')


@util.export
class Plugin(plugin.PluginBase):
    """
    Package upgrade plugin.
    """

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            osetupcons.Stages.DISTRO_RPM_PACKAGE_UPDATE_CHECK,
        ),
        condition=lambda self: (
            self.environment[oenginecons.CoreEnv.ENABLE] and
            self.environment[oenginecons.EngineDBEnv.NEW_DATABASE] and
            not self.environment[osetupcons.CoreEnv.DEVELOPER_MODE]
        )
    )
    def _customization(self):
        setup_packages = okkcons.Const.OVIRT_ENGINE_KEYCLOAK_SETUP_PACKAGE_NAME

        # Add our setup package to the list of setup packages.
        # This is used to make sure all setup packages are fully up-to-date
        # before running engine-setup.
        self.environment[
            osetupcons.RPMDistroEnv.PACKAGES_SETUP
        ].append(
            setup_packages
        )

        if self.environment[oenginecons.CoreEnv.ENABLE]:
            # TODO: Replace condition above with a keycloak-specific one
            package = okkcons.Const.OVIRT_ENGINE_KEYCLOAK_PACKAGE_NAME

            # Add ourselves to the list of packages to be upgraded by
            # engine-setup.
            self.environment[
                osetupcons.RPMDistroEnv.PACKAGES_UPGRADE_LIST
            ].append(
                {
                    'packages': [packages],
                },
            )

            # Add ourselves to the list of packages to be versionlocked
            # after the upgrade, to prevent users from manually upgrading them,
            # thus risking incompatibility between older engine and newer
            # keycloak.
            self.environment[
                osetupcons.RPMDistroEnv.VERSION_LOCK_APPLY
            ].append(package)

            # Add both packages to the list of packages to be filtered out of
            # versionlock right before upgrading.
            # Adding the setup package is not really needed. This file was
            # copied from dwh, see also the discussion/refinement in:
            # https://gerrit.ovirt.org/c/ovirt-dwh/+/79705/
            # But is harmless.
            self.environment[
                osetupcons.RPMDistroEnv.VERSION_LOCK_FILTER
            ].extend([
                package,
                setup_packages,
            ])


# vim: expandtab tabstop=4 shiftwidth=4
