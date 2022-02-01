from conans import ConanFile, CMake, tools


class RecycleConan(ConanFile):
    name = "steinwurf"
    license = "BSD-3"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Simple resource pool for recycling resources in C++"
    topics = ("pool")
    exports_sources = "CMakeLists.txt",
    generators = "cmake"
    cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self.cmake is None:
            cmake = CMake(self)
            cmake.configure()
            self.cmake = cmake
        return self.cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.components["recycle"].names["cmake_find_package"] = "recycle"
        self.cpp_info.components["recycle"].names["cmake_find_package_multi"] = "recycle"
