import setuptools
import pathlib

try:
    import docutils.core
    from docutils.writers import manpage
except ImportError:
    docutils = None
    manpage = None

from pter import version


with open('README.md', encoding='utf-8') as fd:
    long_description = fd.read()


with open('LICENSE', encoding='utf-8') as fd:
    licensetext = fd.read()


def compile_documentation():
    htmlfiles = []

    if docutils is None:
        return htmlfiles

    dst = pathlib.Path('./pter/docs')
    dst.mkdir(exist_ok=True)
    docpath = pathlib.Path('./doc')
    
    pathlib.Path('./man').mkdir(exist_ok=True)

    if None not in [docutils, manpage]:
        for fn in ['pter.rst', 'qpter.rst', 'pter.config.rst']:
            fn = docpath / fn
            if not fn.is_file():
                continue
            if fn.stem == 'pter':
                man_pter = str(fn)
            if fn.stem == 'qpter':
                man_qpter = str(fn)
            if fn.stem == 'pter.config':
                man_config = str(fn)
            dstfn = str(dst / (fn.stem + '.html'))
            docutils.core.publish_file(source_path=str(fn),
                                       destination_path=dstfn,
                                       writer_name='html')
            htmlfiles.append('docs/' + fn.stem + '.html')

            if fn.stem == 'pter.config':
                docutils.core.publish_file(source_path=str(fn),
                                           destination_path='man/pter.config.5',
                                           writer_name='manpage')
            elif fn.stem in ['pter', 'qpter']:
                docutils.core.publish_file(source_path=str(fn),
                                           destination_path='man/' + fn.stem + '.1',
                                           writer_name='manpage')

    return htmlfiles


def collect_documentation():
    if manpage is None:
        return []
    return [('share/man/man1', ['man/pter.1', 'man/qpter.1']),
            ('share/man/man5', ['man/pter.config.5'])]


def collect_icons():
    icons = []
    dst = pathlib.Path('./pter/icons')

    for fn in dst.iterdir():
        if fn.is_file() and fn.suffix == '.png':
            icons.append('icons/' + fn.name)

    return icons


setuptools.setup(
    name='pter',
    version=version.__version__,
    description="Console UI to manage your todo.txt file(s).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://vonshednob.cc/pter",
    author="R",
    author_email="contact+pter@vonshednob.cc",
    project_urls={'repository': "https://codeberg.org/vonshednob/pter",
                  'changelog': "https://codeberg.org/vonshednob/pter/src/branch/main/CHANGELOG.md",
                  'bugs': "https://codeberg.org/vonshednob/pter/issues",
                  'issues': "https://github.com/vonshednob/pter/issues",
                 },
    entry_points={'console_scripts': ['pter=pter.main:run'],
                  'gui_scripts': ['qpter=pter.main:run']},
    packages=['pter'],
    package_data={'pter': collect_icons() + compile_documentation()},
    data_files=collect_documentation() + [
                ('share/applications', ['extras/pter.desktop', 'extras/qpter.desktop']),
                ('share/doc/pter', ['extras/example.conf'])],
    install_requires=['pytodotxt>=1.1.0', 'cursedspace>=1.3.1'],
    extras_require={'xdg': ['pyxdg'],
                    'qt': ['PyQt5'],
                    'all': ['pyxdg', 'PyQt5']},
    python_requires='>=3.0',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console :: Curses',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3',])
