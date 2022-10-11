# Define function directory
ARG FUNCTION_DIR="/function"

FROM continuumio/miniconda3 AS miniconda3

# Install aws-lambda-cpp build dependencies
# Install GCC (Alpine uses musl but we compile and link dependencies with GCC)
RUN apt-get install libstdc++ -y

# Stage 2 - build function and dependencies
FROM miniconda3 AS build-image
# Install aws-lambda-cpp build dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    libtool \
    autoconf \
    automake \
    make \
    cmake \
    libcurl4

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/* ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

# Multi-stage build: grab a fresh copy of the base image
FROM python:buster

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
