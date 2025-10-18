gnome = import('gnome')

app_id = run_command(
    'grep',
    'APP_ID =',
    conf_py,
    check: true
  ).stdout().split(' = ')[1].strip().replace('"', '')

desktop_conf = configuration_data()
desktop_conf.set('bindir', get_option('prefix') / get_option('bindir'))

desktop_file = configure_file(
  input: app_id + '.desktop.in',
  output: app_id + '.desktop',
  #type: 'desktop',
  install: true,
  install_dir: get_option('datadir') / 'applications',
  configuration: desktop_conf
)

message('Looking for dependencies')


# TODO: Requires GLib 2.52 because of Meson issue
#desktop_service = configure_file(
#  input: app_id + '.service.desktop.in',
#  output: app_id + '.service.desktop',
#  configuration: desktop_conf,
#  install: true,
#  install_dir: get_option('datadir') / meson.project_name(),
#)

# i18n.merge_file(
#   input: desktop_file,
#   output: app_id + '.desktop',
#   type: 'desktop',
#   po_dir: '../po',
#   install: true,
#   install_dir: get_option('datadir') / 'applications'
# )
#
# i18n.merge_file(
#   input: app_id + '.appdata.xml.in',
#   output: app_id + '.appdata.xml',
#   po_dir: '../po',
#   install: true,
#   install_dir: get_option('datadir') / 'appdata'
# )

dbus_conf = configuration_data()
dbus_conf.set('bindir', get_option('prefix') / get_option('bindir'))

configure_file(
  input: app_id + '.service.in',
  output: app_id + '.service',
  configuration: dbus_conf,
  install: true,
  install_dir: get_option('datadir') / 'dbus-1/services'
)

install_data(app_id + '.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0/schemas'
)

if false
  gtk_encode_symbolic = find_program('gtk-encode-symbolic-svg')
  sizes = ['32x32', '64x64']
  icon_targets = []
  foreach size: sizes
    icon_targets += custom_target('symbolic-icon-' + size,
      input: 'icons/' + app_id + '-symbolic.svg',
      output: 'icons/' + app_id + '-symbolic.png',
      command: [gtk_encode_symbolic, '--output=' + meson.current_build_dir(), '@INPUT@', size]
    )
  endforeach
endif

icondir = get_option('datadir') / 'icons'
install_subdir('icons/hicolor', install_dir: icondir)

install_data('icons/' + app_id + '-symbolic.svg',
  install_dir: icondir / 'hicolor/symbolic/apps'
)

contributors = '\n'.join([
  'Ryan Bloomfield (sir-maniac)',
  'Roberto Leinardi (leinardi) &lt;roberto@leinardi.com&gt;',
  'Gabriele Musco (gabmus) &lt;emaildigabry@gmail.com&gt;'
])

LIBEXEC_DIR = get_option('prefix') / get_option('libexecdir')
EXTENSION_DIR = get_option('prefix') / get_option('libdir') / meson.project_name()
bindir = get_option('prefix') / get_option('bindir')

glade_conf = configuration_data()
glade_conf.set('PACKAGE_URL', 'https://github.com/sir-maniac/GreenWithEnvy2/issues')
glade_conf.set('DATA_DIR', get_option('prefix') / get_option('datadir') / meson.project_name())
glade_conf.set('EXTENSION_DIR', EXTENSION_DIR)
glade_conf.set('LOCALE_DIR', get_option('prefix') / get_option('datadir') / 'locale')
glade_conf.set('PYTHON_DIR', py_installation.get_install_dir())
#glade_conf.set('PYTHON_EXEC_DIR', get_option('prefix') / python.sysconfig_path('stdlib'))
glade_conf.set('PYTHON', py_installation.full_path())
glade_conf.set('APPID', app_id)
glade_conf.set('libexecdir', LIBEXEC_DIR)
# this is for development version # glade_conf.set('VERSION', ''.join([run_command(['git', 'describe', '--long', '--tags']).stdout(), get_option('profile')]))
glade_conf.set('VERSION', meson.project_version())
glade_conf.set('CONTRIBUTORS', contributors)

gwe_resources = gnome.compile_resources(app_id,
  app_id + '.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: get_option('datadir') / meson.project_name()
)

gwe_settings = gnome.compile_schemas()

install_data(
  app_id + '.appdata.xml',
  install_dir: get_option('datadir') / 'metainfo'
)
