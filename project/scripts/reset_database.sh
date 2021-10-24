#!/bin/bash

# TODO: Fix up relative pathing so you don't accidentally
# delete unintended files/directories

# Remove migrations folder
rm -rf ../migrations

# Remove aerich.ini file
rm ../aerich.ini
