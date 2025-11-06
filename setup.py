from skbuild import setup

setup(
    name="apriltag-pywrapper",
    version="3.4.5",
    description="Lightweight pip-installable wrapper for AprilTag with full tag family support",
    author="Patrick Carnahan",
    packages=["apriltag"],
    include_package_data=True,
    install_requires=["numpy"],
    python_requires=">=3.7",
    url="https://github.com/pcarnah/apriltag-pywrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmake_source_dir="thirdparty/apriltag",
    cmake_args=["-DBUILD_SHARED_LIBS=OFF", "-DBUILD_EXAMPLES=OFF"]
)
