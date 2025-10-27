gnome = import('gnome')

app_id = run_command(
    'grep',
    'APP_ID =',
    conf_py,
    check: true
  ).stdout().split(' = ')[1].strip().replace('"', '')

resource_path = '/' + app_id.replace('.','/')

conf_data = configuration_data()
conf_data.set('APP_ID', app_id)
conf_data.set('APP_NAME_LONG', 'GreenWithEnvy2')
conf_data.set('APP_NAME', meson.project_name())
conf_data.set('RESOURCE_PATH', resource_path)
conf_data.set('SCHEMA_PATH', resource_path + '/')

# Exec entry in .desktop file
if setuptools
  conf_data.set('EXEC', meson.project_name())
else
  conf_data.set('EXEC', get_option('prefix') / get_option('bindir') / meson.project_name())
endif

desktop_file = configure_file(
  input: 'gwe.desktop.in',
  output: app_id + '.desktop',
  #type: 'desktop',
  configuration: conf_data,
  install: true,
  install_dir: resource_data_dir / 'applications',
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
#  install_dir: resource_data_dir / meson.project_name()
)

configure_file(
  input: 'gwe.service.in',
  output: app_id + '.service',
  configuration: conf_data,
  install: true,
  install_dir: resource_data_dir / 'dbus-1/services'
)

gschema_file = configure_file(
  input: 'gwe.gschema.xml.in',
  output: app_id + '.gschema.xml',
  configuration: conf_data,
  install: true,
  install_dir: resource_data_dir / 'glib-2.0/schemas'
)


message('Looking for dependencies')

# i18n.merge_file(
#   input: desktop_file,
#   output: app_id + '.desktop',
#   type: 'desktop',
#   po_dir: '../po',
#   install: true,
#   install_dir: resource_data_dir / 'applications'
# )
#
# i18n.merge_file(
#   input: app_id + '.appdata.xml.in',
#   output: app_id + '.appdata.xml',
#   po_dir: '../po',
#   install: true,
#   install_dir: resource_data_dir / 'appdata'
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


sizes = ['16x16', '24x24', '32x32', '48x48', '256x256']
cp = find_program('cp')
mkdir = find_program('mkdir')
copy_icon_cmd = []

foreach size: sizes
  foreach size_dir: [ size, size + '@2x' ]

    source = files('icons/hicolor' / size_dir / 'apps/gwe.png')

    dest_dir = 'icons/hicolor' / size_dir / 'apps'
    dest_name =  app_id + '.png'

    install_data(
      source,
      rename: dest_name,
      install_dir: resource_data_dir / dest_dir
    )

    # Documentation says assumption shouldn't be made about working directory
    #  so use absolute destination path
    copy_dest_dir = meson.current_build_dir() / dest_dir

    if copy_icon_cmd.length() > 0
      copy_icon_cmd += ['&&']
    endif
    copy_icon_cmd += [
        mkdir, '-p', copy_dest_dir, '&&',
        cp, source, copy_dest_dir / dest_name
    ]

  endforeach
endforeach

local_run_deps += custom_target('copy_icons',
  build_by_default: true,
  output: 'phony_copy_icons',
  command: copy_icon_cmd
)

install_data('icons/gwe-symbolic.svg',
  rename: app_id + '-symbolic.svg',
  install_dir: resource_data_dir / 'icons/hicolor/symbolic/apps'
)

contributors = '\n'.join([
  'Ryan Bloomfield (sir-maniac)',
  'Roberto Leinardi (leinardi) &lt;roberto@leinardi.com&gt;',
  'Gabriele Musco (gabmus) &lt;emaildigabry@gmail.com&gt;'
])

if setuptools
  gresources_install_dir = resource_data_dir
else
  gresources_install_dir = get_option('datadir') / meson.project_name()
endif

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
  install_dir: gresources_install_dir
)
local_run_deps += gwe_resources

install_data(
  'gwe.appdata.xml',
  rename: [app_id + '.appdata.xml'],
  install_dir: gresources_install_dir / 'metainfo'
)

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true
)
