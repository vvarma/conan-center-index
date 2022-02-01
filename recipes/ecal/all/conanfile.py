import os.path
import shutil

from conans import ConanFile, CMake, tools


class EcalConan(ConanFile):
    name = "ecal"
    license = "Apache v2"
    url = "https://github.com/conan-io/conan-center-index"
    description = "The enhanced Communication Abstraction Layer"
    topics = ("dds")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_gui": [True, False],
        "with_hdf5": [True, False],
        "with_debug": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_gui": True,
        "with_hdf5": True,
        "with_debug": False,
    }
    generators = "cmake", "cmake_find_package"
    exports_sources = "CMakeLists.txt",
    cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        if self.options.with_hdf5:
            self.requires("hdf5/1.10.6")
        self.requires("protobuf/3.17.1", private=True)
        self.requires("libcurl/7.78.0", private=True)
        if self.options.with_gui:
            self.requires("qt/5.15.2", private=True)
            self.requires("openssl/1.1.1l", override=True)
        self.requires("spdlog/1.9.2", private=True)
        self.requires("tclap/1.2.4", private=True)
        self.requires("asio/1.21.0", private=True)
        self.requires("gtest/1.11.0", private=True)
        self.requires("tinyxml2/8.0.0", private=True)
        self.requires("simpleini/4.17", private=True)
        self.requires("termcolor/2.0.0", private=True)
        self.requires("fineftp/1.2.0", private=True)
        self.requires("steinwurf/6.0.0", private=True)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self.cmake is None:
            cmake = CMake(self)
            cmake.definitions["ECAL_THIRDPARTY_BUILD_SPDLOG"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_PROTOBUF"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_TINYXML2"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_FINEFTP"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_ZLIB"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_LIBSSH2"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_CURL"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_GTEST"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_HDF5"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_TERMCOLOR"] = "OFF"
            cmake.definitions["ECAL_THIRDPARTY_BUILD_RECYCLE"] = "OFF"
            cmake.definitions["CPACK_PACK_WITH_INNOSETUP"] = "OFF"
            cmake.definitions["BUILD_SAMPLES"] = "OFF"
            if not self.options.with_gui:
                cmake.definitions["HAS_QT5"] = "OFF"
            if not self.options.with_hdf5:
                cmake.definitions["HAS_HDF5"] = "OFF"
            cmake.configure()
            self.cmake = cmake
        return self.cmake

    def build(self):
        shutil.copy(os.path.join(self.source_folder, self._source_subfolder, "LICENSE.txt"), self.build_folder)
        shutil.copy(os.path.join(self.source_folder, self._source_subfolder, "README.md"), self.build_folder)
        # self.copy("LICENSE.txt", dst=self._build_subfolder, src=self._source_subfolder)
        # self.copy("README.md", dst=self._build_subfolder, src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "etc"))

    def package_info(self):
        self.cpp_info.components["core"].names["cmake_find_package"] = "core"
        self.cpp_info.components["core"].names["cmake_find_package_multi"] = "core"
        self.cpp_info.components["core"].libs = ["ecal_core"]

        self.cpp_info.components["core_c"].names["cmake_find_package"] = "core_c"
        self.cpp_info.components["core_c"].names["cmake_find_package_multi"] = "core_c"
        self.cpp_info.components["core_c"].libs = ["ecal_core_c"]
        self.cpp_info.components["core_c"].requires = ["core"]

        self.cpp_info.components["utils"].names["cmake_find_package"] = "utils"
        self.cpp_info.components["utils"].names["cmake_find_package_multi"] = "utils"
        self.cpp_info.components["utils"].libs = ["ecal_utils"]

        if self.options.with_hdf5:
            self.cpp_info.components["hdf5"].names["cmake_find_package"] = "hdf5"
            self.cpp_info.components["hdf5"].names["cmake_find_package_multi"] = "hdf5"
            self.cpp_info.components["hdf5"].libs = ["ecal_hdf5"]
            self.cpp_info.components["hdf5"].requires = ["utils", "hdf5::hdf5"]
