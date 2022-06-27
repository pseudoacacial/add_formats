import os, re, json, shutil

with open('scenario.json', 'r') as f:
    scenario = json.load(f)

formats = scenario["creatives"]
for format in formats:
    format_exists = os.path.exists(format)
    if not format_exists:
        # os.mkdir(format)
        shutil.copytree(formats[0], format)
        with open(format+'\settings.json', 'r') as f:
            format_settings = json.load(f)
        sizes = re.search("(\d+)x(\d+)",format)
        format_settings["MACROS"]["BANNER_WIDTH"]=sizes.group(1)
        format_settings["MACROS"]["BANNER_HEIGHT"]=sizes.group(2)
        format_settings["WGW_API_PARAMS"]["size"]["width"]=sizes.group(1)
        format_settings["WGW_API_PARAMS"]["size"]["height"]=sizes.group(2)
        
        with open(format+'\settings.json', 'w') as f:    
            json.dump(format_settings, f, indent = 4)