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

"""
Consolidated configuration file for Ansible module utilities.
"""

# ----------------------------
# Parallel Tasks Defaults
# ----------------------------
DEFAULT_NTHREADS = 4
DEFAULT_TIMEOUT = 60
LOG_DIR_DEFAULT = "/tmp/thread_logs"
DEFAULT_LOG_FILE = "/tmp/task_results_table.log"
DEFAULT_SLOG_FILE = "/tmp/stask_results_table.log"
CSV_FILE_PATH_DEFAULT = "/tmp/status_results_table.csv"
DEFAULT_REPO_STORE_PATH = "/tmp/offline_repo"
USER_JSON_FILE_DEFAULT = ""
DEFAULT_STATUS_FILENAME = "status.csv"

STATUS_CSV_HEADER = 'name,type,status\n'
SOFTWARE_CSV_HEADER = "name,status"

# ----------------------------
# Software tasklist Defaults
# ----------------------------
LOCAL_REPO_CONFIG_PATH_DEFAULT = ""
SOFTWARE_CSV_FILENAME = "software.csv"
FRESH_INSTALLATION_STATUS = True

# ----------------------------
# Software Utilities Defaults
# ----------------------------
PACKAGE_TYPES = ['rpm', 'deb', 'tarball', 'image', 'manifest', 'git',
                 'pip_module', 'deb', 'shell', 'ansible_galaxy_collection', 'iso']
CSV_COLUMNS = {"column1": "name", "column2": "status"}
SOFTWARE_CONFIG_SUBDIR = "config"
RPM_LABEL_TEMPLATE = "RPMs for {key}"
OMNIA_REPO_KEY = "omnia_repo_url_rhel"
RHEL_OS_URL = "rhel_os_url"
SOFTWARES_KEY = "softwares"
