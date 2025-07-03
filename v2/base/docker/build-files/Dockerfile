# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Replace the args to lock to a specific version
ARG GREENGRASS_RELEASE_VERSION=2.14.3
ARG GREENGRASS_ZIP_FILE=greengrass-${GREENGRASS_RELEASE_VERSION}.zip
ARG GREENGRASS_RELEASE_URI=https://d2s8p88vqu9w66.cloudfront.net/releases/${GREENGRASS_ZIP_FILE}

# Author
LABEL maintainer="AWS IoT Greengrass"
# Greengrass Version
LABEL greengrass-version=${GREENGRASS_RELEASE_VERSION}
# Base OS
LABEL base-os="Amazon Linux 2023 (AWS ECR Public)"
# Python Version
LABEL python-version="3.11"
# Java Version  
LABEL java-version="17"

# Set up Greengrass v2 execution parameters
# TINI_KILL_PROCESS_GROUP allows forwarding SIGTERM to all PIDs in the PID group so Greengrass can exit gracefully
ENV TINI_KILL_PROCESS_GROUP=1 \
    GGC_ROOT_PATH=/greengrass/v2 \
    PROVISION=false \
    AWS_REGION=us-east-1 \
    THING_NAME=default_thing_name \
    THING_GROUP_NAME=default_thing_group_name \
    TES_ROLE_NAME=default_tes_role_name \
    TES_ROLE_ALIAS_NAME=default_tes_role_alias_name \
    COMPONENT_DEFAULT_USER=default_component_user \
    DEPLOY_DEV_TOOLS=false \
    INIT_CONFIG=default_init_config \
    TRUSTED_PLUGIN=default_trusted_plugin_path \
    THING_POLICY_NAME=default_thing_policy_name
RUN env

# Entrypoint script to install and run Greengrass
COPY "greengrass-entrypoint.sh" /

# Install Greengrass v2 dependencies
RUN dnf update -y && \
    dnf install -y --setopt=install_weak_deps=False \
    python3 \
    python3-pip \
    java-17-amazon-corretto-headless \
    tar \
    unzip \
    wget \
    sudo \
    procps-ng \
    which && \
    wget $GREENGRASS_RELEASE_URI && \
    dnf clean all && \
    chmod +x /greengrass-entrypoint.sh && \
    mkdir -p /opt/greengrassv2 $GGC_ROOT_PATH && \
    unzip $GREENGRASS_ZIP_FILE -d /opt/greengrassv2 && \
    rm $GREENGRASS_ZIP_FILE

# modify /etc/sudoers
COPY "modify-sudoers.sh" /
RUN chmod +x /modify-sudoers.sh
RUN ./modify-sudoers.sh

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD pgrep -f "Greengrass.jar" > /dev/null || exit 1

ENTRYPOINT ["/greengrass-entrypoint.sh"]