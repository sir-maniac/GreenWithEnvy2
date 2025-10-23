gnome = import('gnome')

app_id = run_command(
    'grep',
    'APP_ID =',
    conf_py,
    check: true
  ).stdout().split(' = ')[1].strip().replace('"', '')

resource_path = '/' + app_id.replace('.','/')

conf_data = configuration_data()
conf_data.set('BIN_FILE', get_option('prefix') / get_option('bindir') / meson.project_name())
conf_data.set('APP_ID', app_id)
conf_data.set('APP_NAME_LONG', 'GreenWithEnvy2')
conf_data.set('APP_NAME', meson.project_name())
conf_data.set('RESOURCE_PATH', resource_path)
conf_data.set('SCHEMA_PATH', resource_path + '/')


desktop_file = configure_file(
  input: 'gwe.desktop.in',
  output: app_id + '.desktop',
  #type: 'desktop',
  configuration: conf_data,
  install: true,
  install_dir: get_option('datadir') / 'applications',
)

gresource_file = configure_file(
  input: 'gwe.gresource.xml.in',
  output: app_id + '.gresource.xml',
  configuration: conf_data,
)

# TODO: Requires GLib 2.52 because of Meson issue
 service_desktop_file = configure_file(
  input: 'gwe.service.desktop.in',
  output: app_id + '.service.desktop',
  configuration: conf_data,
#  install: true,
#  install_dir: get_option('datadir') / meson.project_name()
)

configure_file(
  input: 'gwe.service.in',
  output: app_id + '.service',
  configuration: conf_data,
  install: true,
  install_dir: get_option('datadir') / 'dbus-1/services'
)

gschema_file = configure_file(
  input: 'gwe.gschema.xml.in',
  output: app_id + '.gschema.xml',
  configuration: conf_data,
  install: true,
  install_dir: get_option('datadir') / 'glib-2.0/schemas'
)


message('Looking for dependencies')

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


gwe_resources = gnome.compile_resources(app_id,
  gresource_file,
  extra_args: ['--target',  'data/' + app_id + '.gresource'],
  dependencies: [ gresource_file, service_desktop_file ],
  source_dir: [
    '.',
    meson.current_build_dir() / 'data'
  ],

  gresource_bundle: true,
  install: true,
  install_dir: get_option('datadir') / meson.project_name()
)

install_data(
  'gwe.appdata.xml',
  rename: [app_id + '.appdata.xml'],
  install_dir: get_option('datadir') / 'metainfo'
)

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true
)
