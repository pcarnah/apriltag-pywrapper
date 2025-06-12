from skbuild import setup

setup(
    name="apriltag-wrapper",
    version="0.1.0",
    description="Lightweight pip-installable wrapper for AprilTag with full tag family support",
    author="Your Name",
    packages=["apriltag"],
    include_package_data=True,
    install_requires=["numpy"],
    python_requires=">=3.7",
    url="https://github.com/yourusername/apriltag-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmake_source_dir="thirdparty/apriltag",
    cmake_args=["-DBUILD_SHARED_LIBS=OFF", "-DBUILD_EXAMPLES=OFF"]
)
