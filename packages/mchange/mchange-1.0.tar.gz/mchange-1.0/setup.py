import setuptools
with open(r'C:\Users\sex\Documents\mchange\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='mchange',
	version='1.0',
	author='mc_c0rp',
	author_email='mc.c0rp@icloud.com',
	description='Fast and Free currency converter that uses Xe.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/mc-c0rp/mchange',
	packages=['mchange'],
	install_requires=["bs4", "requests"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)