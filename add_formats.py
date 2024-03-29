#!/usr/bin/env python
import os, re, json, shutil

with open('scenario.json', 'r') as f:
    scenario = json.load(f)
formats = scenario["creatives"]
# remove unneeded sizes
subfolders = [ f.path for f in os.scandir() if f.is_dir() ]
for folder in subfolders:
    folder_is_format = os.path.exists(os.path.join(folder,'settings.json'))
    if (folder_is_format):
        size_found = False
        for format in formats:
            search = re.search(format+"$", folder)
            if (search):
                size_found = True
        if(size_found):
            print("keeping folder", folder, '✔️')
        else:
            print("removing folder", folder, '❌')
            shutil.rmtree(folder)

#choose existing format for base
for format in formats:
    format_exists = os.path.exists(format)
    if format_exists:
        base = format
        break
        
# add new sizes
for format in formats:
    format_exists = os.path.exists(format)
    if not format_exists:
        print("adding folder ./" + format, "➕ based on", base)
        shutil.copytree(base, format)
        with open(os.path.join(format,'settings.json'), 'r') as f:
            format_settings = json.load(f)
        sizes = re.search("(\d+)x(\d+)",format)
        if "BANNER_WIDTH" in format_settings["MACROS"]:
            format_settings["MACROS"]["BANNER_WIDTH"]=sizes.group(1)
            format_settings["MACROS"]["BANNER_HEIGHT"]=sizes.group(2)
        if "banner" in format_settings["MACROS"]:
            if "WIDTH" in format_settings["MACROS"]["banner"]:
                format_settings["MACROS"]["banner"]["WIDTH"]=sizes.group(1)
                format_settings["MACROS"]["banner"]["HEIGHT"]=sizes.group(2)
        if "BANNER" in format_settings["MACROS"]:
            if "WIDTH" in format_settings["MACROS"]["BANNER"]:
                format_settings["MACROS"]["BANNER"]["WIDTH"]=sizes.group(1)
                format_settings["MACROS"]["BANNER"]["HEIGHT"]=sizes.group(2)
        format_settings["WGW_API_PARAMS"]["size"]["width"]=sizes.group(1)
        format_settings["WGW_API_PARAMS"]["size"]["height"]=sizes.group(2)        
        with open(os.path.join(format,'settings.json'), 'w') as f:    
            json.dump(format_settings, f, indent = 4)
