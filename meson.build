project('gwe2',
  version: run_command(
    'grep',
    'APP_VERSION',
    files('gwe/conf.py'),
    check: true
  ).stdout().split(' = ')[1].strip().strip('"'),
  meson_version: '>= 0.63.0'
)
# project version is defined in gwe/conf.py

conf_py = files('gwe/conf.py')

# Importing modules
# i18n = import('i18n')
python = import('python')
py_installation = python.find_installation('python3')
if not py_installation.found()
    error('No valid python3 installation found')
else
    message('Found python3 installation')
endif

summary({
  'Python Binary': py_installation.full_path(),
  'Python Install Path': py_installation.get_install_dir()
})

find_result = run_command(
  'find', 'gwe', '-iname', '*.py',
  check: true)
sources = find_result.stdout().strip().split('\n')

# Dependencies
dependency('gobject-introspection-1.0', version: '>= 1.56.0')

py_installation.install_sources(sources, preserve_path: true)

# dependencies that are needed for 'run' and 'debug' targets
local_run_deps = []

subdir('data')
subdir('bin')

meson.add_install_script('scripts/meson_post_install.py')