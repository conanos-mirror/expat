#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conanos.build import config_scheme
import shutil, os

class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.5"
    description = "Fast XML parser in C"
    url = "https://github.com/bincrafters/conan-expat"
    license = "MIT"
    exports = ['LICENSE.md']
    exports_sources = ['CMakeLists.txt', 'FindEXPAT.cmake']
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def source(self):
        base_url = "https://github.com/libexpat/libexpat/archive"
        zip_name = "R_%s.zip" % self.version.replace(".", "_") 
        tools.get("%s/%s" % (base_url, zip_name))

    def build(self):
        cmake = CMake(self, parallel=True)

        cmake.definitions['BUILD_doc'] = False
        cmake.definitions['BUILD_examples'] = False
        cmake.definitions['BUILD_tests'] = False
        cmake.definitions['BUILD_tools'] = False
        cmake.definitions['CMAKE_DEBUG_POSTFIX'] = 'd'
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.definitions['BUILD_shared'] = self.options.shared

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindEXPAT.cmake", ".", ".")
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            shutil.copy2(os.path.join("lib", "expatd.lib"), 
                         os.path.join(self.package_folder, "lib", "expat.lib"))

    def package_info(self):
        self.cpp_info.libs = ["expatd" if self.settings.build_type == "Debug" else "expat"]
        if not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

    def configure(self):
        del self.settings.compiler.libcxx
        
        config_scheme(self)
