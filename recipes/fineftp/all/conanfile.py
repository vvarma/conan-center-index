from conans import ConanFile, CMake, tools


class FineftpConan(ConanFile):
    name = "fineftp"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    description = "C++ FTP Server Library for Windows, Linux & more"
    topics = ("ftp", "server")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package"
    cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def requirements(self):
        self.requires("asio/1.21.0")

    def _configure_cmake(self):
        if self.cmake is None:
            cmake = CMake(self)
            cmake.configure(source_folder=self._source_subfolder)
            self.cmake = cmake
        return self.cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.components["server"].names["cmake_find_package"] = "server"
        self.cpp_info.components["server"].names["cmake_find_package_multi"] = "server"
        self.cpp_info.components["server"].libs = ["fineftp-server"]
        self.cpp_info.components["server"].requires = ["asio::asio"]
