## Sakura's Rig Interfaces V3

Current Version: 3.1.0
Targeted Blender: 5.0
Minimum Blender: 4.2

---

V3.1.0 is a small corrective release fixing some minor navigation issues I experienced with the UI in practical use as well as fixing some minor issues I personally noticed.

These issues and changes were brought about after a render that I worked on following the release of R7.4.0, in which I found the UI to be a bit cluttered and difficult to navigate, specifically around the face section. The changes made in this release are intended to make the UI more user friendly and easier to navigate. As well as adding in some missing Material options for the Irises and Sclera.

On the backend, a lot of dirty laundry was cleaned up, mainly regarding unused variables, useless characters, and bad naming semantics.

---

## General Extension Changes

- Replaced "module_info" with "bl_info" in all modules which still had it
  - This change is because bl_info already handles all the info I wanted module_info to handle, and having bl_info and module_info was just wasted space.
- Simplified the "Region" blocks, removing the Separator "Line."
- Moved all SACR UI's to "sedaia_ui"

### Sedaia Utils

- Removed "rig_download" entry from Ops ID list, as it is unused.
- Removed redundant Region calls and blocks.
- Removed useless "error.URLError" from retrieveJSON()
- Removed a lot of redundant parenthasis 
- Renamed multiple functions to use pascal_case instead of snakeCase
- Removed unused "FILE_delete" class
- Added `bl_options = {"REGISTER", "INTERNAL"}` to all Skin Operators
- Added new Backup function for the Skin downloader.

### Global UI -> Skin Utility UI

- Renamed module from "global_ui" to "SKIN_utility_ui"
- Moved module into "sedaia_ui" from Root
- Removed Panel Template
- Removed redundant Region Calls
- Removed region block separators
- Added "SEDAIA_SKIN_PT" to configure all current and future panels
- Made all Variables in the "Configs" array local class variables for "ui_skinUtility"
- Renamed Class from SEDAIA_MAIN_PT to SEDAIA_SKIN_PT
- Renamed the Tab from "Sedaia Skin Utility" to "Download Skins"


## Rig UI Changes

### SACR R7 UI Version 1.3.2

- Fixed a couple lingering semantic issues.

### SACR R7 UI Version 2.0.1:

- Added a new "SACR7_UI2_panel" class to store the Category and Space Information in a single location, making further development and maintenance easier.
- Removed the Configuration Atlas due to the new SACR7_UI2_panel class, where 
- Added "Opacity" to Iris and Sclera Emissive properties.
- Moved Iris and Sclera panels under the new Eyes Panel.
- Moved Eyebrow Controller visibility options to the Eyebrow Panel.
- Moved Eye Controller visibility options to the Eye Panel.
- Moved Mouth Controller visibility options to the Mouth Panel.
- Rebuilt the Eyebrow, Eyes, and Mouth visibility options backend to be cleaner and more readable
- Updated the Checkboxes in the Iris and Sclera sections to use a new method of defining UI spacing, fixing the inconsistent sizing issue with using a percentage split.
- Removed `if __init__ = "main"` statement as this module cannot be installed on it's own, and the statement's inclusion was redundant.
- Removed License Disclosure from the top of the Module.
- Restrict Select no longer available on the Lite Version of SACR R7.4.1
- Color ramp for Pupils now under a sub panel