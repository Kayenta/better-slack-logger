import setuptools

with open("README.md", mode="r", encoding="utf8") as fd:
    long_description = fd.read()

setuptools.setup(
    name="better-slack-logger",
    version="0.11.0",
    author="Chaitanya Chinni & Jay Turner",
    description="Slack Logger is a custom message logger to Slack for Python 3",
    maintainer="Jay Turner",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TurnrDev/better-slack-logger",
    packages=setuptools.find_packages(),
    install_requires=["slackclient == 2.9.3", "pyyaml == 5.4.1"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.5",
    keywords=[
        "monitoring",
        "slack",
        "messaging",
        "logging",
        "health-check",
        "notification-service",
        "notification",
        "slack-api",
    ],
)
