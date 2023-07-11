#!/bin/bash

# Remove the docs directory
rm -rf docs

# Automatically generate the directory again using pdoc
pdoc --force --html --output-dir docs activitypubdantic

# Move the files to the docs folder
mv docs/activitypubdantic/* docs

# Remove the old directory
rm -rf docs/activitypubdantic