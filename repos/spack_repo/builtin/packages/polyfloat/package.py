# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Polyfloat(CMakePackage):
    """POLYFLOAT - flexible multiprecision floating point types built on EVE SIMD types."""

    homepage = "https://jfalcou.github.io/polyfloat/"
    git = "https://github.com/jfalcou/polyfloat.git"

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
    # The tests compare against MPFR through MPFR C++, which they fetch as a header.
    depends_on("gmp", type="test")
    depends_on("mpfr", type="test")

    def cmake_args(self):
        return [
            self.define("CPM_COPACABANA_SOURCE", self.spec["copacabana"].prefix),
            self.define("CPM_LOCAL_PACKAGES_ONLY", True),
            self.define("POLYFLOAT_BUILD_TEST", self.run_tests),
            self.define("POLYFLOAT_BUILD_DOCUMENTATION", False),
        ]

    def check(self):
        # `all` builds nothing in a header-only library; the unit tests hang off the
        # aggregate target copacabana defines for the project.
        with working_dir(self.build_directory):
            cmake("--build", ".", "--target", "polyfloat-test", "--parallel", str(make_jobs))
            ctest("--output-on-failure", "--parallel", str(make_jobs))
