# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=import-error

#!/usr/bin/python

""" This module is used to fetch telemetry host inventory"""

import csv
import configparser
from ansible.module_utils.basic import AnsibleModule

def get_hosts_from_group(file_path, group_name, module):
    """
    This function retrieves a list of hosts for a specified group from an Ansible inventory file.
    Parameters:
        file_path (str): The path to the Ansible inventory file.
        group_name (str): The name of the group for which to retrieve hosts.
    Returns:
        list: A list of hosts under the specified group.
    """
    if not file_path:
        return []
    config = configparser.ConfigParser(allow_no_value=True, delimiters=' ', comment_prefixes='#')
    config.optionxform = str  # preserve case
    config.read(file_path)

    if group_name not in config:
        module.warn(f"Group '{group_name}' not found in cluster_layout.")
        return []

    # Return list of hosts under the group
    return list(config[group_name].keys())

def fetch_valid_parent_tags(file_path, service_node_metadata, module):
    """
    This function fetches the parent tags from a given CSV file.

    Parameters:
        file_path (str): The path to the CSV file containing parent tags.

    Returns:
        set: A set of parent tags found in the CSV file.
    """
    parent_tags = set()
    invalid_tags = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent = row.get('PARENT', '').strip()
            if parent:
                if parent not in service_node_metadata:
                    module.warn(f"Parent tag '{parent}' not found in service node metadata.")
                    invalid_tags.add(parent)
                    continue
                parent_tags.add(parent)
    return parent_tags, invalid_tags

def fetch_active_passive_servicetags(parent_tags, service_node_metadata):
    """
    Fetches the active and passive service tags based
    on the provided parent tags and service node metadata.

    Parameters:
        parent_tags (list): A list of parent tags used to identify service nodes.
        service_node_metadata (dict): A dictionary containing metadata about service nodes.

    Returns:
        tuple: A tuple containing two sets. The first set contains active service tags.
               The second set contains passive service tags.
    """
    svc_node_info = {}
    for service_tag, data in service_node_metadata.items():
        node_info = {}
        if service_tag in parent_tags:
            active_service_tag = data.get('active_service_tag', service_tag)
            node_info['active_service_tag'] =  active_service_tag
            sn_active_ip = data.get('virtual_ip_address', data['admin_ip'])
            node_info['active_ip'] = sn_active_ip
            node_info['admin_ip'] = data['admin_ip']
            svc_node_info[active_service_tag] = node_info
            if data.get('active', False):
                passive_service_tags = data.get('passive_nodes', [])
                for passive_tag in passive_service_tags:
                    if passive_tag not in svc_node_info:
                        svc_node_info[passive_tag] = {
                            'active_service_tag': active_service_tag,
                            'active_ip': service_node_metadata[passive_tag]['virtual_ip_address'],
                            'admin_ip': service_node_metadata[passive_tag]['admin_ip']
                        }

    return svc_node_info

def main():
    """Main module function."""
    module_args = {
        'bmc_group_data_path': {'type': "str", 'required': True},
        'service_node_metadata': {'type': "dict", 'required': True},
        'inventory_file_path': {'type': "str", 'required': False},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    bmc_group_data_path = module.params["bmc_group_data_path"]
    service_node_metadata = module.params["service_node_metadata"]
    inventory_file_path = module.params.get("inventory_file_path", "")
    try:
        parent_tags, invalid_tags = fetch_valid_parent_tags(bmc_group_data_path,
                                                            service_node_metadata, module)
        if invalid_tags:
            module.exit_json(
                changed=False,
                msg=f"Invalid parent tags found: {', '.join(invalid_tags)}.",
                invalid_parent_tags=list(invalid_tags)
            )
        # sn_admin_ip, sn_active_ip = fetch_admin_ip(parent_tags, service_node_metadata)
        svc_node_info = fetch_active_passive_servicetags(parent_tags, service_node_metadata)
        oim_ha_nodes = get_hosts_from_group(inventory_file_path, 'oim_ha_node', module)
        module.exit_json(changed=False, sn_node_info=svc_node_info,
                         oim_ha_hosts=oim_ha_nodes)
    except ValueError as e:
        module.fail_json(msg=f"Failed to to get Service Node Group data. {e}")

if __name__ == "__main__":
    main()
