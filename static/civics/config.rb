# To prevent problems of encoding when compiling:
Encoding.default_external = "utf-8"

# Additional plugins:
require 'compass/import-once/activate'
require 'sass-globbing'

# Set abstractions as an import path to every partial
add_import_path "sass/base/abstractions"

# Set syntax to sass:
preferred_syntax = :sass

#
# Paths and assets
#
http_path       = "/"
css_dir         = "css"
sass_dir        = "sass"
images_dir      = "img"
fonts_dir       = "fonts"
javascripts_dir = "js"
relative_assets = true

#
# Output style
#
output_style  = (environment == :production) ? :compressed : :expanded
line_comments = (environment == :production) ? false : true

# To prevent warnings about deprecated stuff
disable_warnings = true
