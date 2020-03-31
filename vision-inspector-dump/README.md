# Dump IBM Visual Inspector Data from PowerAI Vision or Visual Insights

## Usage
```
python visual_inspector_dump.py --user admin 
                                --passwd passw0rd
                                --url https://vision-poc1.aus.stglabs.ibm.com/powerai-vision
                                --output outer.csv
```
See the [notebook example](../master/DataDumpExample.ipynb) as well for usage via API.

## Supported flags
```
usage: visual_inspector_dump.py [-h] [--dsid DSID] --url URL --output OUTPUT
                                --user USER --passwd PASSWD [--showall]
                                [--debug]

Tool to extract IBM Visual Inspector data from IBM Visual Insights

optional arguments:
  -h, --help       show this help message and exit
  --dsid DSID      (Optional) UUID of a target dataset
  --url URL        Vision URL eg https://ip/powerai-vision WITHOUT trailing
                   slash or /api
  --output OUTPUT  Output file name eg output.csv
  --user USER      Username
  --passwd PASSWD  Password
  --showall        (Optional) Show all image data. By default, this tool
                   filters training data.
  --debug          Set Debug logging level
  ```
