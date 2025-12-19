#!/bin/bash
# Build and publish the harvester collection to Ansible Galaxy

set -e

# Build the collection
ansible-galaxy collection build --force

# Publish to Galaxy
ansible-galaxy collection publish ./bpmconsultag-harvester-*.tar.gz --token "$ANSIBLE_GALAXY_TOKEN"