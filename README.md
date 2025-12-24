# Sakura's Rig Interfaces

Sakura's Rig Interfaces is a container addon designed to make development of UI scripts even easier by adding a dynamic loading script along with global utilities which make having duplicate classes a rarer occurance.

---

## Instructions

1. Download the Latest release of Sakura's Rig Interfaces Addon from either [my website](https://sakura-sedaia.com/addon/sakura-rig-interface) or the [Blender Extensions](https://extensions.blender.org/add-ons/sakura-rig-interfaces/) site
2. Open Blender, and navigate to User Preferences > Addons
3. Open the Dropdown Arrow on the Top Right
4. Select "Install From Disk" and install the Sakura Rig Interfaces Addon
5. Check Addon to ensure it is enabled
6. Download the appropriate Rig from [https://sakura-sedaia.com/rigs/sacr](https://sakura-sedaia.com/rig/sakura-character-rig)c
7. Open the Rig and enjoy

## Credits

- JacquesLocke's [Blender Development extension](https://github.com/JacquesLucke/blender_vscode) for Visual Studio Code


## Changelog

- Addon name changed to Sedaia Rig Interfaces, as all global utilities will be moved to their own addon
- Created "Modules" module to handle Module Registry
- Global UI module created to handle any universal operators.

### Preferences

- Renamed file from "addon_prefs" to just "prefs"
- Created a copy of the "File Open" class inside Preferences.
- Added more options

### Sedaia Utilities

- Renamed module "SedaiaOperators" to "sedaia_utils"
- Added lookup table for Class ID Names
- Added Import "extension_path_user" from BPY Utils, and updated associated calls
- Removed Unused definition "update()"
- Class standard renamed to be simply the category and function.
- Replaced all "print" Calls with the proper Report calls
- Made changes within def generate_player_data()
  - Rewrote core router to be more readable and clear.
  - Added Else case for if Online Access is disabled
  - Users can now either Load data, add new entry, or purge and replace existing data when loading previously called Username
  - Cleaned JSON Structure for stored Player Data
    - Removed Username, UUID, and HTTP links
    - "SKIN" dictionary changed to support multiple skin files saved from a single username.

### All Interfaces:

- Added lookup table for Class ID Names

## Rig UI Changes

### SACR R7 UI Version 1 (Final Update):

- Renamed Module to sacrUI_R7_UI1 to SACR_R7_UI1
- Updated all external module calls to the new standard.
- Version 1 of the R7 GUI will no longer recieve updates from this point on, except to ensure continued compatability with the rest of the Addon

### SACR R7 UI Version 2:

- Renamed Module to sacrUI_R7_UI2 to SACR_R7_UI2
- Performed a complete UI Rewrite, incorporating more advanced features and QoL changes.