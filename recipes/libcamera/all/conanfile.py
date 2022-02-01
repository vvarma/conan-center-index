import os.path

from conans import ConanFile, Meson, tools


class LibcameraConan(ConanFile):
    name = "libcamera"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    generators = "pkg_config"
    build_requires = "meson/0.60.2"
    requires = "boost/1.77.0"
    _meson = None

    def system_requirements(self):
        import pip
        if hasattr(pip, "main"):
            pip.main(["install", "jinja2", "ply"])
        else:
            from pip._internal import main
            main(['install', "jinja2", "ply"])

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        self.run(f"git clone --depth=1 https://github.com/vvarma/libcamera.git {self._source_subfolder}")

    def __configure_meson(self):
        if self._meson is None:
            args = ["-Dv4l2=True", "-Ddocumentation=disabled", "-Dqcam=disabled"]
            _meson = Meson(self)
            _meson.configure(
                args=args,
                source_dir=self._source_subfolder,
                build_dir=self._build_subfolder,
            )
            self._meson = _meson
        return self._meson

    def build(self):
        meson = self.__configure_meson()
        meson.build()

    def package(self):
        meson = self.__configure_meson()
        meson.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.components["core"].names["camera_find_package"] = "core"
        self.cpp_info.components["core"].names["camera_find_package_multi"] = "core"
        self.cpp_info.components["core"].libs = ["camera", "camera-base"]
        self.cpp_info.components["core"].requires = ["boost::boost"]
        self.cpp_info.components["core"].includedirs = [os.path.join("include", "libcamera")]
