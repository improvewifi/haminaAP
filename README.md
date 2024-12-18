## *** Disclaimer: Use at your own risk ***
It would be best to duplicate the project before using this tool. (Subscription required)
Height is currently omitted because it made the names too long.
Locations for Imperial are rounded to the inch, while the Metric system goes three decimal places.

## This tool adds an X & Y coordinate in either Metric or Imperial units to AP names from a user-determined zero point. <br />
![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/map_with_ap_distances.png) <br />
![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/ap_name_with_distance.png) <br />

Optionally, it can create a CSV file with this information, which has been helpful to installers and other staff to make sure all APs are installed and in the correct locations. While you can download an archive of the code in either a text or json file.

## How to use:
Setting your zero point (Where AP distances will be measured from.)
  1. Create a map note in the location you want to measure from.
  2. In the map note, add the text: zero point (capitalization doesn't matter) <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/map_note.png) <br />
  *Note: If multiple map notes with this text exist, the first to process will be used.

Prepping to copy data:
  1. Turn off all layers except for map notes and APs (Optional but improved performance for large projects)
  2. If you want APs to maintain their exact name and numbering set manually (dynamic numbering increments when pasted back in)
  3. Fit the design to the window
  4. Ctrl+x / Command+x to cut  (if you mess up Ctrl/Command + z works to restore)

In the tool:
  1. Select your measurement system <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/measurement_system.png) <br /> 
  3. Optional: if you want any downloads, check the box(es) wanted <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/delivery.png) <br />
     a. CSV Includes more information, such as azimuth, elevation, etc. I usually hand a copy of this to my low-voltage vendor <br />
     b. The other two options are there for backup and retention services <br />
     *Note: The files only stay on the server for a few hours and then are purged
  4. Paste in the cut/copied data from prepping the data into the text box <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/paste_copied_data.png) <br />
  5. click submit
  6. If downloadable deliverables were requested, select the download link, and a zip file will be downloaded with the requested contents <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/download_link_shown.png) <br />
  *Note: The download link only shows if at least one deliverable is selected
  7. Click the "Copy results button to clipboard" button (the text field below is a way to validate what you are copying, but isn't formatted correctly to copy and paste) <br />
  ![alt text](https://github.com/improvewifi/haminaAP/blob/main/readme_images/copy_results_to_clipboard.png) <br />

Back in Hamina:
  1. refresh the page. This is to ensure that the data isn't shifted down and to the right
  2. Paste in the results copied to the clipboard (Ctrl+v or Command+v)
