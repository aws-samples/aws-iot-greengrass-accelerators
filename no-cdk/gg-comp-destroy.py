# Copyright 2023 Amazon.com, Inc. and its affiliates. All Rights Reserved.

# Licensed under the Amazon Software License (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at

# http://aws.amazon.com/asl/

# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# This script creates a deployment with the component specified in a list
# for the greengrass instance specified in 'resource/manifest.json'


import comp_resource_handler
if __name__ == '__main__':
  
    comp_resource_handler.cleanUpPreviousDeployment()
