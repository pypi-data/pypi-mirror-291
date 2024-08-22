from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='wavsetpos',
    version='1.1',
    description='A library for setting pos of a wav file with pygame.mixer.music',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='',
    author='Raymond Grottodden',
    author_email='raymondgrotto651@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['pygame', 'wav', 'music', 'mixer'],
    packages=find_packages(),
    install_requires=['pydub==0.25.1']
)