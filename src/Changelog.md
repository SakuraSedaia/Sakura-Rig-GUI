## Sakura's Rig Interfaces V3

Dev Version: V3
Targeted Blender: 5.0
Minimum Blender: 4.2

---
V3 Summary

V3 see's another architecture change, making it much easier to add more Rig Interfaces to the UI with an Autoload script and dynamic loading for other modules.

On top of the Architecture changes, the Skin Downloader and an updated UI Script for SACR R7 which utilizes some of the new backend hooks and properties from R7.4 for more fine control.

---

## Changelog
- Addon name changed to Sedaia Rig Interfaces, as all global utilities will be moved to their own addon
- Working Directory renamed to "src"
- Archive Directory renamed to "archives
- Created "Modules" module to handle Module Registry
- Global UI module created to handle any universal operators.
- Build Script to automate the process of packaging

### Preferences

- Renamed file from "addon_prefs" to just "prefs"
- Created a copy of the "File Open" class inside Preferences.
- Added more options

### Sedaia Utilities

- Renamed module "SedaiaOperators" to "sedaia_utils"
- Added Import "extension_path_user" from BPY Utils, and updated associated calls
- Removed Unused definition "update()"
- Removed Unused "File Delete" class
- Class standard renamed to be simply the category and function.
- Replaced all "print" Calls with the proper Report calls
- Made changes within def generate_player_data()
  - Rewrote core router to be more readable and clear.
  - Added Else case for if Online Access is disabled
  - Users can now either Load data, add new entry, or purge and replace existing data when loading previously called Username
  - Restructured Player JSON
    - Removed HTTP links
    - "SKIN" dictionary changed to support multiple skin files saved from a single username.

### All Modules:

- Added lookup table for Class ID Names

## Rig UI Changes

### General UI Changes

- Applied new more reliable method for Material Object Detection
  - New method iterates through an Enumerator and just checks for the presence of a matching Keyword

### SACR R7 UI Version 1 (Final Update):

- Renamed Module to sacrUI_R7_UI1 to SACR_R7_UI1
- Updated all external module calls to the new standard.
- Version 1 of the R7 GUI will no longer recieve updates from this point on, except to ensure continued compatability with the rest of the Addon

### SACR R7 UI Version 2:

- Renamed Module to sacrUI_R7_UI2 to SACR_R7_UI2
- Performed a complete UI Rewrite, incorporating more advanced features and QoL changes.
- Added Restrict Select option
- Added option to reset rig scale