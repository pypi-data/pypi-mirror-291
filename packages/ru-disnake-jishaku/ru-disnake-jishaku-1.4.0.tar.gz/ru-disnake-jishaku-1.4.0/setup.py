import pathlib
import re

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

# Получение версии из файла meta.py
VERSION = "1.0.0"
try:
    with open(ROOT / 'jishaku' / 'meta.py', 'r', encoding='utf-8') as f:
        content = f.read()
        VERSION_MATCH = re.search(r'VersionInfo\(major=(\d+), minor=(\d+), micro=(\d+)', content)

        if VERSION_MATCH:
            VERSION = '.'.join(VERSION_MATCH.groups())
        else:
            raise RuntimeError('Version is not set or could not be located')

except FileNotFoundError:
    raise RuntimeError('The meta.py file was not found')
except Exception as e:
    raise RuntimeError(f'An error occurred while reading the version: {e}')

# Получение дополнительных зависимостей из requirements
EXTRA_REQUIRES = {}

for feature in (ROOT / 'requirements').glob('*.txt'):
    try:
        with open(feature, 'r', encoding='utf-8') as f:
            EXTRA_REQUIRES[feature.with_suffix('').name] = [line.strip() for line in f if line.strip()]
    except Exception as e:
        raise RuntimeError(f'An error occurred while reading {feature}: {e}')

# Основные зависимости
REQUIREMENTS = EXTRA_REQUIRES.pop('_', [])

if not VERSION:
    raise RuntimeError('Version is not set')

# Чтение файла README.md
try:
    with open(ROOT / 'README.md', 'r', encoding='utf-8') as f:
        README = f.read()
except FileNotFoundError:
    raise RuntimeError('README.md file not found')

# Настройка пакета
setup(
    name='ru-disnake-jishaku',
    author='darkness800',
    url='https://github.com/darkness800/disnake-jishaku-ru',
    license='MIT',
    description='A disnake extension including useful tools for bot development and debugging.',
    long_description=README,
    long_description_content_type='text/markdown',
    project_urls={
        'Code': 'https://github.com/darkness800/disnake-jishaku-ru',
        'Issue tracker': 'https://github.com/darkness800/disnake-jishaku-ru/issues'
    },
    version='1.4.0',
    packages=['jishaku', 'jishaku.features', 'jishaku.repl', 'jishaku.shim'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires='>=3.8.0',
    extras_require=EXTRA_REQUIRES,
    keywords='jishaku disnake disnake-jishaku-ru discord cog repl extension ru-fork',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ]
)

