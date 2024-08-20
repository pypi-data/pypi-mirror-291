# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""Helpers and utilities to identify platforms.

Everything here can be aggressively cached and frozen, as it's only compute
platform-dependent values.

.. note::

    Default icons are inspired from Starship project:
    - https://starship.rs/config/#os
    - https://github.com/davidkna/starship/blob/e9faf17/.github/config-schema.json#L1221-L1269
"""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Iterable, Iterator

if sys.version_info >= (3, 9):
    from functools import cache
else:
    from functools import lru_cache

    def cache(user_function):
        """Simple lightweight unbounded cache. Sometimes called "memoize".

        .. important::

            This is a straight `copy of the functools.cache implementation
            <https://github.com/python/cpython/blob/55a26de/Lib/functools.py#L647-L653>`_,
            which is only `available in the standard library starting with Python v3.9
            <https://docs.python.org/3/library/functools.html?highlight=caching#functools.cache>`.
        """
        return lru_cache(maxsize=None)(user_function)


import distro
from boltons.iterutils import remap

from . import detection


def recursive_update(
    a: dict[str, Any], b: dict[str, Any], strict: bool = False
) -> dict[str, Any]:
    """Like standard ``dict.update()``, but recursive so sub-dict gets updated.

    Ignore elements present in ``b`` but not in ``a``. Unless ``strict`` is set to
    `True`, in which case a `ValueError` exception will be raised.
    """
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = recursive_update(a[k], v, strict=strict)
        # Ignore elements unregistered in the template structure.
        elif k in a:
            a[k] = b[k]
        elif strict:
            msg = f"Parameter {k!r} found in second dict but not in first."
            raise ValueError(msg)
    return a


def remove_blanks(
    tree: dict,
    remove_none: bool = True,
    remove_dicts: bool = True,
    remove_str: bool = True,
) -> dict:
    """Returns a copy of a dict without items whose values blanks.

    Are considered blanks:
    - `None` values
    - empty strings
    - empty `dict`

    The removal of each of these class can be skipped by setting ``remove_*``
    parameters.

    Dictionarries are inspected recursively and their own blank values are removed.
    """

    def visit(path, key, value) -> bool:
        """Ignore some class of blank values depending on configuration."""
        if remove_none and value is None:
            return False
        if remove_dicts and isinstance(value, dict) and not len(value):
            return False
        if remove_str and isinstance(value, str) and not len(value):
            return False
        return True

    return remap(tree, visit=visit)


@dataclass(frozen=True)
class Platform:
    """A platform can identify multiple distributions or OSes with the same
    characteristics.

    It has a unique ID, a human-readable name, and boolean to flag current platform.
    """

    id: str
    """Unique ID of the platform."""

    name: str
    """User-friendly name of the platform."""

    icon: str = field(repr=False, default="❓")
    """Icon of the platform."""

    current: bool = field(init=False)
    """`True` if current environment runs on this platform."""

    def __post_init__(self):
        """Set the ``current`` attribute to identifying the current platform."""
        object.__setattr__(self, "current", detection.__dict__[f"is_{self.id}"]())
        object.__setattr__(self, "__doc__", f"Identify {self.name}.")

    def info(self) -> dict[str, str | bool | None | dict[str, str | None]]:
        """Returns all platform attributes we can gather."""
        info = {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "current": self.current,
            # Extra fields from distro.info().
            "distro_id": None,
            "version": None,
            "version_parts": {"major": None, "minor": None, "build_number": None},
            "like": None,
            "codename": None,
        }
        # Get extra info from distro.
        if self.current:
            distro_info = distro.info()
            # Rename distro ID to avoid conflict with our own ID.
            distro_info["distro_id"] = distro_info.pop("id")
            info = recursive_update(info, remove_blanks(distro_info))
        return info


AIX = Platform("aix", "IBM AIX", "➿")
ALTLINUX = Platform("altlinux", "ALT Linux")
AMZN = Platform("amzn", "Amazon Linux", "🙂")
ANDROID = Platform("android", "Android", "🤖")
ARCH = Platform("arch", "Arch Linux", "🎗️")
BUILDROOT = Platform("buildroot", "Buildroot")
CENTOS = Platform("centos", "CentOS", "💠")
CLOUDLINUX = Platform("cloudlinux", "CloudLinux OS")
CYGWIN = Platform("cygwin", "Cygwin", "Ͼ")
DEBIAN = Platform("debian", "Debian", "🌀")
EXHERBO = Platform("exherbo", "Exherbo Linux")
FEDORA = Platform("fedora", "Fedora", "🎩")
FREEBSD = Platform("freebsd", "FreeBSD", "😈")
GENTOO = Platform("gentoo", "Gentoo Linux", "🗜️")
GUIX = Platform("guix", "Guix System")
HURD = Platform("hurd", "GNU/Hurd", "🐃")
IBM_POWERKVM = Platform("ibm_powerkvm", "IBM PowerKVM")
KVMIBM = Platform("kvmibm", "KVM for IBM z Systems")
LINUXMINT = Platform("linuxmint", "Linux Mint", "🌿")
MACOS = Platform("macos", "macOS", "🍎")
MAGEIA = Platform("mageia", "Mageia")
MANDRIVA = Platform("mandriva", "Mandriva Linux")
MIDNIGHTBSD = Platform("midnightbsd", "MidnightBSD", "🌘")
NETBSD = Platform("netbsd", "NetBSD", "🚩")
OPENBSD = Platform("openbsd", "OpenBSD", "🐡")
OPENSUSE = Platform("opensuse", "openSUSE", "🦎")
ORACLE = Platform("oracle", "Oracle Linux", "🦴")
PARALLELS = Platform("parallels", "Parallels")
PIDORA = Platform("pidora", "Pidora")
RASPBIAN = Platform("raspbian", "Raspbian", "🍓")
RHEL = Platform("rhel", "RedHat Enterprise Linux", "🎩")
ROCKY = Platform("rocky", "Rocky Linux", "💠")
SCIENTIFIC = Platform("scientific", "Scientific Linux")
SLACKWARE = Platform("slackware", "Slackware")
SLES = Platform("sles", "SUSE Linux Enterprise Server", "🦎")
SOLARIS = Platform("solaris", "Solaris", "🌞")
SUNOS = Platform("sunos", "SunOS", "☀️")
UBUNTU = Platform("ubuntu", "Ubuntu", "🎯")
UNKNOWN_LINUX = Platform("unknown_linux", "Unknown Linux", "🐧")
WINDOWS = Platform("windows", "Windows", "🪟")
WSL1 = Platform("wsl1", "Windows Subsystem for Linux v1", "⊞")
WSL2 = Platform("wsl2", "Windows Subsystem for Linux v2", "⊞")
XENSERVER = Platform("xenserver", "XenServer")


@dataclass(frozen=True)
class Group:
    """A ``Group`` identify a collection of ``Platform``.

    Used to group platforms of the same family.
    """

    id: str
    """Unique ID of the group."""

    name: str
    """User-friendly description of a group."""

    icon: str = field(repr=False, default="❓")
    """Icon of the group."""

    platforms: tuple[Platform, ...] = field(repr=False, default_factory=tuple)
    """Sorted list of platforms that belong to this group."""

    platform_ids: frozenset[str] = field(default_factory=frozenset)
    """Set of platform IDs that belong to this group.

    Used to test platform overlaps between groups.
    """

    def __post_init__(self):
        """Keep the platforms sorted by IDs."""
        object.__setattr__(
            self,
            "platforms",
            tuple(sorted(self.platforms, key=lambda p: p.id)),
        )
        object.__setattr__(
            self,
            "platform_ids",
            frozenset({p.id for p in self.platforms}),
        )
        # Double-check there is no duplicate platforms.
        assert len(self.platforms) == len(self.platform_ids)

    def __iter__(self) -> Iterator[Platform]:
        """Iterate over the platforms of the group."""
        yield from self.platforms

    def __len__(self) -> int:
        """Return the number of platforms in the group."""
        return len(self.platforms)

    @staticmethod
    def _extract_platform_ids(other: Group | Iterable[Platform]) -> frozenset[str]:
        """Extract the platform IDs from ``other``."""
        if isinstance(other, Group):
            return other.platform_ids
        return frozenset(p.id for p in other)

    def isdisjoint(self, other: Group | Iterable[Platform]) -> bool:
        """Return `True` if the group has no platforms in common with ``other``."""
        return self.platform_ids.isdisjoint(self._extract_platform_ids(other))

    def fullyintersects(self, other: Group | Iterable[Platform]) -> bool:
        """Return `True` if the group has all platforms in common with ``other``.

        We cannot just compare ``Groups`` with the ``==`` equality operator as the
        latter takes all attributes into account, as per ``dataclass`` default behavior.
        """
        return self.platform_ids == self._extract_platform_ids(other)

    def issubset(self, other: Group | Iterable[Platform]) -> bool:
        return self.platform_ids.issubset(self._extract_platform_ids(other))

    def issuperset(self, other: Group | Iterable[Platform]) -> bool:
        return self.platform_ids.issuperset(self._extract_platform_ids(other))


ALL_PLATFORMS: Group = Group(
    "all_platforms",
    "Any platforms",
    "🖥️",
    (
        AIX,
        ALTLINUX,
        AMZN,
        ANDROID,
        ARCH,
        BUILDROOT,
        CENTOS,
        CLOUDLINUX,
        CYGWIN,
        DEBIAN,
        EXHERBO,
        FEDORA,
        FREEBSD,
        GENTOO,
        GUIX,
        HURD,
        IBM_POWERKVM,
        KVMIBM,
        LINUXMINT,
        MACOS,
        MAGEIA,
        MANDRIVA,
        MIDNIGHTBSD,
        NETBSD,
        OPENBSD,
        OPENSUSE,
        ORACLE,
        PARALLELS,
        PIDORA,
        RASPBIAN,
        RHEL,
        ROCKY,
        SCIENTIFIC,
        SLACKWARE,
        SLES,
        SOLARIS,
        SUNOS,
        UBUNTU,
        UNKNOWN_LINUX,
        WINDOWS,
        WSL1,
        WSL2,
        XENSERVER,
    ),
)
"""All recognized platforms."""


ALL_WINDOWS = Group("all_windows", "Any Windows", "🪟", (WINDOWS,))
"""All Windows operating systems."""


UNIX = Group(
    "unix",
    "Any Unix",
    "⨷",
    tuple(p for p in ALL_PLATFORMS.platforms if p not in ALL_WINDOWS),
)
"""All Unix-like operating systems and compatibility layers."""


UNIX_WITHOUT_MACOS = Group(
    "unix_without_macos",
    "Any Unix but macOS",
    "⨂",
    tuple(p for p in UNIX if p is not MACOS),
)
"""All Unix platforms, without macOS.

This is useful to avoid macOS-specific workarounds on Unix platforms.
"""


BSD = Group(
    "bsd", "Any BSD", "🅱️", (FREEBSD, MACOS, MIDNIGHTBSD, NETBSD, OPENBSD, SUNOS)
)
"""All BSD platforms.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `386BSD` (`FreeBSD`, `NetBSD`, `OpenBSD`, `DragonFly BSD`)
    - `NeXTSTEP`
    - `Darwin` (`macOS`, `iOS`, `audioOS`, `iPadOS`, `tvOS`, `watchOS`, `bridgeOS`)
    - `SunOS`
    - `Ultrix`
"""


BSD_WITHOUT_MACOS = Group(
    "bsd_without_macos",
    "Any BSD but macOS",
    "🅱️",
    tuple(p for p in BSD if p is not MACOS),
)
"""All BSD platforms, without macOS.

This is useful to avoid macOS-specific workarounds on BSD platforms.
"""


ALL_LINUX = Group(
    "all_linux",
    "Any Linux",
    "🐧",
    (
        ALTLINUX,
        AMZN,
        ANDROID,
        ARCH,
        BUILDROOT,
        CENTOS,
        CLOUDLINUX,
        DEBIAN,
        EXHERBO,
        FEDORA,
        GENTOO,
        GUIX,
        IBM_POWERKVM,
        KVMIBM,
        LINUXMINT,
        MAGEIA,
        MANDRIVA,
        OPENSUSE,
        ORACLE,
        PARALLELS,
        PIDORA,
        RASPBIAN,
        RHEL,
        ROCKY,
        SCIENTIFIC,
        SLACKWARE,
        SLES,
        UBUNTU,
        UNKNOWN_LINUX,
        XENSERVER,
    ),
)
"""All Unix platforms based on a Linux kernel.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Android`
    - `ChromeOS`
    - any other distribution
"""


LINUX_LAYERS = Group(
    "linux_layers", "Any Linux compatibility layers", "≚", (WSL1, WSL2)
)
"""Interfaces that allows Linux binaries to run on a different host system.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Windows Subsystem for Linux`
"""


SYSTEM_V = Group(
    "system_v", "Any Unix derived from AT&T System Five", "Ⅴ", (AIX, SOLARIS)
)
"""All Unix platforms derived from AT&T System Five.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `A/UX`
    - `AIX`
    - `HP-UX`
    - `IRIX`
    - `OpenServer`
    - `Solaris`
    - `OpenSolaris`
    - `Illumos`
    - `Tru64`
    - `UNIX`
    - `UnixWare`
"""


UNIX_LAYERS = Group(
    "unix_layers",
    "Any Unix compatibility layers",
    "≛",
    (CYGWIN,),
)
"""Interfaces that allows Unix binaries to run on a different host system.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Cygwin`
    - `Darling`
    - `Eunice`
    - `GNV`
    - `Interix`
    - `MachTen`
    - `Microsoft POSIX subsystem`
    - `MKS Toolkit`
    - `PASE`
    - `P.I.P.S.`
    - `PWS/VSE-AF`
    - `UNIX System Services`
    - `UserLAnd Technologies`
    - `Windows Services for UNIX`
"""


OTHER_UNIX = Group(
    "other_unix",
    "Any other Unix",
    "⊎",
    tuple(
        p
        for p in UNIX
        if p
        not in (
            BSD.platforms
            + ALL_LINUX.platforms
            + LINUX_LAYERS.platforms
            + SYSTEM_V.platforms
            + UNIX_LAYERS.platforms
        )
    ),
)
"""All other Unix platforms.

.. note::
    Are considered of this family (`according Wikipedia
    <https://en.wikipedia.org/wiki/Template:Unix>`_):

    - `Coherent`
    - `GNU/Hurd`
    - `HarmonyOS`
    - `LiteOS`
    - `LynxOS`
    - `Minix`
    - `MOS`
    - `OSF/1`
    - `QNX`
    - `BlackBerry 10`
    - `Research Unix`
    - `SerenityOS`
"""


NON_OVERLAPPING_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_WINDOWS,
        BSD,
        ALL_LINUX,
        LINUX_LAYERS,
        SYSTEM_V,
        UNIX_LAYERS,
        OTHER_UNIX,
    ),
)
"""Non-overlapping groups."""


EXTRA_GROUPS: frozenset[Group] = frozenset(
    (
        ALL_PLATFORMS,
        UNIX,
        UNIX_WITHOUT_MACOS,
        BSD_WITHOUT_MACOS,
    ),
)
"""Overlapping groups, defined for convenience."""


ALL_GROUPS: frozenset[Group] = frozenset(NON_OVERLAPPING_GROUPS | EXTRA_GROUPS)
"""All groups."""


ALL_OS_LABELS: frozenset[str] = frozenset(p.name for p in ALL_PLATFORMS.platforms)
"""Sets of all recognized labels."""


def reduce(items: Iterable[Group | Platform]) -> set[Group | Platform]:
    """Reduce a collection of ``Group`` and ``Platform`` to a minimal set.

    Returns a deduplicated set of ``Group`` and ``Platform`` that covers the same exact
    platforms as the original input, but group as much platforms as possible, to reduce
    the number of items.

    .. hint::
        Maybe this could be solved with some `Euler diagram
        <https://en.wikipedia.org/wiki/Euler_diagram>`_ algorithms, like those
        implemented in `eule <https://github.com/trouchet/eule>`_.

        This is being discussed upstream at `trouchet/eule#120
        <https://github.com/trouchet/eule/issues/120>`_.
    """
    # Collect all platforms.
    platforms: set[Platform] = set()
    for item in items:
        if isinstance(item, Group):
            platforms.update(item.platforms)
        else:
            platforms.add(item)

    # List any group matching the platforms.
    valid_groups: set[Group] = set()
    for group in ALL_GROUPS:
        if group.issubset(platforms):
            valid_groups.add(group)

    # Test all combination of groups to find the smallest set of groups + platforms.
    min_items: int = 0
    results: list[set[Group | Platform]] = []
    # Serialize group sets for deterministic lookups. Sort them by platform count.
    groups = tuple(sorted(valid_groups, key=len, reverse=True))
    for subset_size in range(1, len(groups) + 1):
        # If we already have a solution that involves less items than the current
        # subset of groups we're going to evaluates, there is no point in continuing.
        if min_items and subset_size > min_items:
            break

        for group_subset in combinations(groups, subset_size):
            # If any group overlaps another, there is no point in exploring this subset.
            if not all(g[0].isdisjoint(g[1]) for g in combinations(group_subset, 2)):
                continue

            # Remove all platforms covered by the groups.
            ungrouped_platforms = platforms.copy()
            for group in group_subset:
                ungrouped_platforms.difference_update(group.platforms)

            # Merge the groups and the remaining platforms.
            reduction = ungrouped_platforms.union(group_subset)
            reduction_size = len(reduction)

            # Reset the results if we have a new solution that is better than the
            # previous ones.
            if not results or reduction_size < min_items:
                results = [reduction]
                min_items = reduction_size
            # If the solution is as good as the previous one, add it to the results.
            elif reduction_size == min_items:
                results.append(reduction)

    if len(results) > 1:
        msg = f"Multiple solutions found: {results}"
        raise RuntimeError(msg)

    # If no reduced solution was found, return the original platforms.
    if not results:
        return platforms  # type: ignore[return-value]

    return results.pop()


@cache
def current_os() -> Platform:
    """Return the current platform."""
    matching = []
    for p in ALL_PLATFORMS.platforms:
        if p.current:
            matching.append(p)

    if len(matching) > 1:
        msg = f"Multiple platforms match current OS: {matching}"
        raise RuntimeError(msg)

    if not matching:
        msg = (
            f"Unrecognized {sys.platform} / "
            f"{platform.platform(aliased=True, terse=True)} platform."
        )
        raise SystemError(msg)

    assert len(matching) == 1
    return matching.pop()


CURRENT_OS_ID: str = current_os().id
CURRENT_OS_LABEL: str = current_os().name
"""Constants about the current platform."""
