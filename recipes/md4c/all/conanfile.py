import os.path

from conans import ConanFile, CMake, tools


class Md4cConan(ConanFile):
    name = "md4c"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    description = "C Markdown parser. Fast. SAX-like interface. Compliant to CommonMark specification."
    topics = ("markdown", "parser")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self.cmake == None:
            cmake = CMake(self)
            cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
            self.cmake = cmake
        return self.cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ["md4c"]
