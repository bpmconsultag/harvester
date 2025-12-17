# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-12-17

### Added
- New `harvester_vm_info` module for retrieving VM information via API
- Support for VM annotations in `harvester_vm` module
- Example playbook `create_vm_from_image.yml` demonstrating VM creation with reference images using annotations
- Example playbook `get_vm_info.yml` demonstrating how to retrieve VM information

### Changed
- Enhanced `harvester_vm` module with annotation support for better VM metadata management

## [1.0.1] - 2025-12-17

### Changed
- Renamed role from `harvesterpy` to `harvester` for clarity
- Renamed all role variables from `harvesterpy_*` to `harvester_*` prefix
- Updated repository URLs from harvesterpy to harvester
- Updated all documentation and examples to reflect new naming

### Notes
- The role name is now `harvester` to distinguish it from the `harvesterpy` Python library
- Python library name remains `harvesterpy` - only the Ansible role name changed

## [1.0.0] - 2025-12-17

### Added
- Initial release of harvester Ansible role
- Support for managing Harvester virtual machines
- Support for managing Harvester images
- Support for managing Harvester volumes
- Support for managing Harvester networks
- Integration with HarvesterPy Python library
- Comprehensive documentation and examples
- Test playbooks and CI/CD integration

### Features
- `harvester_vm` module for VM lifecycle management
- `harvester_image` module for image management
- `harvester_volume` module for volume management
- `harvester_network` module for network management
- Configurable API connection settings
- SSL certificate verification options
### Customizable timeouts and namespaces

[1.0.2]: https://github.com/bpmconsultag/harvester/releases/tag/v1.0.2
[1.0.1]: https://github.com/bpmconsultag/harvester/releases/tag/v1.0.1
[1.0.0]: https://github.com/bpmconsultag/harvester/releases/tag/v1.0.0
