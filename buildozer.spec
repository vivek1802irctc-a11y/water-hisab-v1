[app]

title = Water Hisab

package.name = waterhisab

package.domain = org.vivek

source.dir = .

source.include_exts = py,kv,db,png,jpg,jpeg

version = 1.0

requirements = python3,kivy==2.3.1,kivymd==1.2.0,sqlite3

orientation = portrait

fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]

log_level = 2

warn_on_root = 1