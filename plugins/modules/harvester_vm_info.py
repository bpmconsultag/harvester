#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, bpmconsultag
# MIT License

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: harvester_vm_info
short_description: Get information about virtual machines in SUSE Harvester HCI
version_added: "1.0.0"
description:
    - Retrieve detailed information about virtual machines and their instances in SUSE Harvester HCI.
    - This module uses the harvesterpy Python library.
    - Can retrieve both VM (VirtualMachine) and VMI (VirtualMachineInstance) information.
options:
    host:
        description:
            - Harvester host URL (e.g., 'https://harvester.example.com')
        required: true
        type: str
    token:
        description:
            - API token for authentication
        required: false
        type: str
    username:
        description:
            - Username for basic authentication
        required: false
        type: str
    password:
        description:
            - Password for basic authentication
        required: false
        type: str
    verify_ssl:
        description:
            - Whether to verify SSL certificates
        required: false
        type: bool
        default: true
    timeout:
        description:
            - Request timeout in seconds
        required: false
        type: int
        default: 30
    name:
        description:
            - Name of the virtual machine
        required: true
        type: str
    namespace:
        description:
            - Namespace of the virtual machine
        required: false
        type: str
        default: "default"
    gather_instance:
        description:
            - Whether to also gather VirtualMachineInstance information
            - VMI contains runtime information like IP addresses, status, etc.
        required: false
        type: bool
        default: true
requirements:
    - harvesterpy >= 0.1.5
author:
    - bpmconsultag
'''

EXAMPLES = r'''
# Get VM information including instance data
- name: Get VM info with IP address
  harvester_vm_info:
    host: "https://harvester.example.com"
    token: "your-api-token"
    name: "my-vm"
    namespace: "default"
  register: vm_info

- name: Display VM IP address
  debug:
    msg: "VM IP: {{ vm_info.instance.status.interfaces[0].ipAddress }}"
  when: vm_info.instance.status.interfaces is defined

# Get only VM information without instance data
- name: Get VM info only
  harvester_vm_info:
    host: "https://harvester.example.com"
    token: "your-api-token"
    name: "my-vm"
    namespace: "default"
    gather_instance: false
  register: vm_info
'''

RETURN = r'''
vm:
    description: Virtual Machine object
    returned: always
    type: dict
    sample: {
        "metadata": {
            "name": "my-vm",
            "namespace": "default"
        },
        "spec": {
            "running": true
        },
        "status": {
            "ready": true,
            "printableStatus": "Running"
        }
    }
instance:
    description: Virtual Machine Instance object with runtime information
    returned: when gather_instance is true and instance exists
    type: dict
    sample: {
        "metadata": {
            "name": "my-vm",
            "namespace": "default"
        },
        "status": {
            "phase": "Running",
            "interfaces": [
                {
                    "ipAddress": "192.168.1.100",
                    "mac": "52:54:00:12:34:56",
                    "name": "default"
                }
            ]
        }
    }
exists:
    description: Whether the VM exists
    returned: always
    type: bool
instance_exists:
    description: Whether the VM instance exists
    returned: when gather_instance is true
    type: bool
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from harvesterpy import HarvesterClient
    from harvesterpy.exceptions import (
        HarvesterException,
        HarvesterAPIError,
        HarvesterAuthenticationError,
        HarvesterNotFoundError,
    )
    HAS_HARVESTERPY = True
except ImportError:
    HAS_HARVESTERPY = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str', required=True),
            token=dict(type='str', required=False, no_log=True),
            username=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            verify_ssl=dict(type='bool', required=False, default=True),
            timeout=dict(type='int', required=False, default=30),
            name=dict(type='str', required=True),
            namespace=dict(type='str', required=False, default='default'),
            gather_instance=dict(type='bool', required=False, default=True),
        ),
        required_one_of=[
            ['token', 'username']
        ],
        required_together=[
            ['username', 'password']
        ],
        supports_check_mode=True,
    )

    if not HAS_HARVESTERPY:
        module.fail_json(msg="harvesterpy Python library is required. Install with: pip install harvesterpy")

    # Extract module parameters
    host = module.params['host']
    token = module.params.get('token')
    username = module.params.get('username')
    password = module.params.get('password')
    verify_ssl = module.params['verify_ssl']
    timeout = module.params['timeout']
    name = module.params['name']
    namespace = module.params['namespace']
    gather_instance = module.params['gather_instance']

    result = {
        'changed': False,
        'vm': {},
        'instance': {},
        'exists': False,
        'instance_exists': False,
    }

    try:
        # Initialize Harvester client
        client = HarvesterClient(
            host=host,
            token=token,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            timeout=timeout
        )

        # Get VM information
        try:
            vm = client.virtual_machines.get(name, namespace=namespace)
            result['vm'] = vm
            result['exists'] = True
        except HarvesterNotFoundError:
            result['exists'] = False
            module.exit_json(**result)

        # Get VMI information if requested
        if gather_instance:
            try:
                # Query VirtualMachineInstance endpoint directly
                vmi_path = f"/apis/kubevirt.io/v1/namespaces/{namespace}/virtualmachineinstances/{name}"
                vmi = client.get(vmi_path)
                result['instance'] = vmi
                result['instance_exists'] = True
            except HarvesterNotFoundError:
                result['instance_exists'] = False
            except Exception as e:
                # VMI might not exist if VM is stopped
                result['instance_exists'] = False

        module.exit_json(**result)

    except HarvesterAuthenticationError as e:
        module.fail_json(msg=f"Authentication failed: {str(e)}")
    except HarvesterAPIError as e:
        module.fail_json(msg=f"API error: {str(e)}")
    except HarvesterException as e:
        module.fail_json(msg=f"Harvester error: {str(e)}")
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    main()
