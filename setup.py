from setuptools import setup, find_packages

setup(
	author="Matt Triano",
	description="A package of little pieces.",
	name="pezzetti",
	version="0.1.0",
	packages=find_packages(include=["pezzetti", "pezzetti.*"]),
)