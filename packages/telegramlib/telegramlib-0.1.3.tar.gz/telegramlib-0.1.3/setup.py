from setuptools import setup, find_packages
import platform

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

install_requires = parse_requirements('requirements.txt')
install_requires += [package + "; sys_platform == 'darwin'" for package in parse_requirements('requirements-macos.txt') if package not in install_requires]

setup(
    name="telegramlib",
    version="0.1.3",
    description="Easiest Python package to create Telegram bots.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniele Lanciotti",
    author_email="daniele9001@gmail.com",
    url="https://github.com/ilLancio/telegramlib",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["telegram", "bot", "api", "easy"],
    license="MIT",
    project_urls={
        "Source": "https://github.com/ilLancio/telegramlib",
        "Tracker": "https://github.com/ilLancio/telegramlib/issues",
        "Documentation": "https://illancio.github.io/telegramlib/",
        "Changelog": "https://github.com/ilLancio/telegramlib/blob/master/CHANGELOG.md",
        "Homepage": "https://illancio.github.io"
    }
)
