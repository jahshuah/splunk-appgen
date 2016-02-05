# Splunk App Generator (splunk-appgen)
App scaffolding/generation tool for basic Splunk TAs

## Usage:

```
$ ./splunk_appgen.py -a <appname> [-t <target_directory>]
```

## What it is
This is a little script that generates a basic folder structure for your Splunk app. My main use for this tool is to generate a scaffold for Splunk technology add-ons (TAs) when working with new events. The script will generate the following folder structure:

* appname
  * bin
  * default
    * app.conf
    * eventgen.conf
    * eventtypes.conf
    * indexes.conf
    * inputs.conf
    * props.conf
    * tags.conf
    * transforms.conf
  * local
  * lookups
  * metadata
    * default.meta

The script will ask for information about the app for inclusion in the `appname/default/app.conf` file. If no answers are given to for the prompts, the app will use defaults from `~/appgenrc` or `./appgenrc` (current working directory).

It's really basic. Like, REALLY basic. Requires argparse, ConfigParser, and jinja2 Python modules in order to work. Tested on Python version 2.6 and 2.7.

Use at your own risk (or to your own success!), and may the odds be ever in your favor.

## Coming Soon:

* script designed to package the app into a *.tgz file
  * Might change that to *.spl, but not sure if Splunk is even using that anymore...
