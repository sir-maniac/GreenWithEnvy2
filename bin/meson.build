conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('PKGDATA_DIR', get_option('prefix') / get_option('datadir') / meson.project_name())
conf.set('ICON_PATH', get_option('prefix') / get_option('datadir') / 'icons' )
conf.set('PYTHON', py_installation.full_path())
conf.set('PYTHON_DIR', py_installation.get_install_dir())

configure_file(
  input: 'gwe.in',
  output: meson.project_name(),
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gwe = meson.project_build_root() / 'bin' / meson.project_name()
run_target('run',
  command: [gwe]
)

run_target('debug',
  command: [gwe, '--debug']
)
