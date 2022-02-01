from conans import ConanFile, tools


class SimpleiniConan(ConanFile):
    name = "simpleini"
    version = "4.17"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Cross-platform C++ library providing a simple API to read and write INI-style configuration files"
    topics = ("ini")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def package(self):
        self.copy("*.h", dst="include", src=self._source_subfolder)

