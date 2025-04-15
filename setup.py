from setuptools import setup, find_packages

with open("README.md", "r") as file:
	long_description = file.read()

link = 'https://github.com/xXxCLOTIxXx/kyodo/archive/refs/heads/main.zip'
ver = '0.8.26'

setup(
	name = "kyodo",
	version = ver,
	url = "https://github.com/xXxCLOTIxXx/kyodo",
	download_url = link,
	license = "MIT",
	author = "Xsarz",
	author_email = "xsarzy@gmail.com",
	description = "Library for creating kyodo bots and scripts.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"kyodo.py",
		"kyodo",
		"kyodo-py",
		"kyodo-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"xsarz",
		"official",
		"async",
	],
	install_requires = [
		"logging",
		"colorama",
		"aiohttp",
		"pyjwt",
		"aiofiles"
	],
	packages = find_packages()
)