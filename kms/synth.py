# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

client_library_version = "0.1.0"

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
version = "v1"

# ----------------------------------------------------------------------------
# Generate kms GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "kms",
    version,
    config_path="artman_cloudkms.yaml",
    artman_output_name="kms-v1",
    include_protos=True,
)

s.move(library, excludes=["README.rst", "setup.py", "nox*.py", "docs/**/*"])

# Temporary fixup for 'grpc-google-iam-vi 0.12.4' (before generation).
s.replace(
    "google/cloud/kms_v1/gapic/transports/key_management_service_grpc_transport.py",
    "from google.iam.v1 import iam_policy_pb2",
    "from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
