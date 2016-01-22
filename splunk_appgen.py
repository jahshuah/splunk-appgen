#!/usr/bin/env python

"""
Description:
An app generator/scaffolding tool for Splunk applications

"""
__author__ = "Joshua Hart"
__version__ = 1.0
__status__ = "beta"

import os
import sys
import argparse
import ConfigParser
import jinja2
from jinja2 import *

# Read in defaults from appgen.conf and set default
# values for the app.conf stuff
appgenrc = {}

# Require config file appgenrc to pull default 
if os.path.isfile(os.path.join(os.path.expanduser('~'), 'appgenrc')):
    appgenrc['path'] = os.path.join(os.path.expanduser('~'), 'appgenrc')
elif os.path.isfile(os.path.join(os.getcwd(), 'appgenrc')):
    appgenrc['path'] = os.path.join(os.getcwd(), 'appgenrc')

if appgenrc['path']:
    try:
        cfg = ConfigParser.RawConfigParser()
        cfg.read(appgenrc['path'])
        
        author = cfg.get('defaults', 'default_author')
        company = cfg.get('defaults', 'default_company')
        version = cfg.get('defaults', 'default_version')
        description = cfg.get('defaults', 'default_description')
        title = cfg.get('defaults', 'default_title')
    except:
        print "\nCannot read .appgenrc! Check to ensure the file exists and is readable.\n"
        sys.exit(1)

# Load templates
template_env = Environment(loader=FileSystemLoader('./_templates/'))

# Build the scaffold of the app (e.g. $appname/default/app.conf, $appname/default/props.conf, etc.)
def build_scaffold(root, app):
    scaffold = {
        "bin": None,
        "local": None,
        "default" : {
            "app.conf": None,
            "eventgen.conf": None,
            "eventtypes.conf": None,
            "indexes.conf": None,
            "inputs.conf": None,
            "props.conf": None,
            "tags.conf": None,
            "transforms.conf": None
        },
        "metadata" : {
            "default.meta": None
        },
        "lookups": None
    }

    # This is totally a cop-out, but it's the best I could come up with at the time.
    dirs_list = []
    for key, value in scaffold.iteritems():
        dirs_list.append(key)

    # Build the scaffold :)
    for i in dirs_list:
        if not os.path.exists(os.path.join(root, app, i)):
            os.makedirs(os.path.join(root, app, i))
        if scaffold[i] is not None:
            for key, value in scaffold[i].iteritems():
                open(os.path.join(root, app, i, key), 'a').close()

def write_appconf_file(root, app):
    print "Let's gather some information about your app...\n"
    app_info = {}
    app_info['author'] = raw_input("Author (default is '" + author + "'): ") or author
    app_info['company'] = raw_input("Company (default is '" + company + "'): ") or company
    app_info['version'] = raw_input("App version number (default is '" + version + "'): ") or version
    app_info['description'] = raw_input("Description of app (default is '" + description + "'): ") or description
    app_info['title'] = raw_input("Friendly name for all (default is '" + title + "'): ") or title
    app_info['app_name'] = raw_input("App ID (no spaces, default is '" + app + "'): ") or app

    with open(os.path.join(root, app, "default", "app.conf"), 'w') as appconf_file:
        appconf_file.write(template_env.get_template('app.j2').render(app_info))

def generate_default_meta(root, app):
    with open(os.path.join(root, app, "metadata", "default.meta"), 'w') as defaultmeta_file:
        defaultmeta_file.write(template_env.get_template('default.meta.j2').render())

def main():
    # Pass the app name to the script via command line arguments
    parser = argparse.ArgumentParser(description='Scaffolding tool for Splunk applications (mostly TAs)')
    parser.add_argument(
        '-a',
        '--app-name',
        nargs=1,
        default="dcndc_app_scaffolded_app",
        required=True,
        help="Name of the app, without spaces. Serves as the app/project folder name.",
        metavar='APP_NAME'
    )
    parser.add_argument(
        '-t',
        '--target-dir',
        nargs=1,
        default=".",
        required=False,
        help='Starting directory for new app. Default is current directory.',
        metavar='TARGET_DIRECTORY'
    )
    args = parser.parse_args()
    app_name = args.app_name[0]
    root_dir = args.target_dir[0]
    print "Creating your app structure at %s\n" % (os.path.join(root_dir, app_name))

    # Create the app and its scaffolding
    build_scaffold(root_dir, app_name)
    write_appconf_file(root_dir, app_name)
    generate_default_meta(root_dir, app_name)

if __name__ == '__main__':
    main()
