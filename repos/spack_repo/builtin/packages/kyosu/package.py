# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Kyosu(CMakePackage):
    """KYOSU - complex numbers, quaternions and octonions over EVE SIMD types, with the
    mathematical functions to go with them."""

    homepage = "https://jfalcou.github.io/kyosu/"
    git = "https://github.com/jfalcou/kyosu.git"

    maintainers("jfalcou")

    license("BSL-1.0")

    version("main", branch="main")

    depends_on("cxx", type="build")
    depends_on("cmake@3.22:", type="build")
    # The build is written with copacabana, which CPM fetches at configure time; the
    # prefix installed here is handed to CPM instead, see cmake_args. EVE and TTS are
    # fetched the same way, and found installed once CPM is told to look for them.
    depends_on("copacabana", type="build")
    depends_on("eve@main")
    depends_on("tts", type="build")

    def cmake_args(self):
        return [
            self.define("CPM_COPACABANA_SOURCE", self.spec["copacabana"].prefix),
            self.define("CPM_LOCAL_PACKAGES_ONLY", True),
            self.define("KYOSU_BUILD_TEST", self.run_tests),
            self.define("KYOSU_BUILD_DOCUMENTATION", False),
            self.define("KYOSU_BUILD_DEMOS", False),
        ]

    def check(self):
        # `all` builds nothing in a header-only library; the unit tests hang off the
        # aggregate target copacabana defines for the project.
        with working_dir(self.build_directory):
            cmake("--build", ".", "--target", "kyosu-test", "--parallel", str(make_jobs))
            ctest("--output-on-failure", "--parallel", str(make_jobs))
