# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.9.5"
ARG DISTRO_VERSION="3.14"

FROM continuumio/miniconda3 AS miniconda3
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



# Include global args in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
# Copy handler function
COPY app/* ${FUNCTION_DIR}
# Optional – Install the function's dependencies
WORKDIR ${FUNCTION_DIR}
#RUN python -m pip install --upgrade pip


# Install Lambda Runtime Interface Client for Python
RUN python -m pip install awslambdaric --target ${FUNCTION_DIR}



# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
FROM miniconda3
RUN apt-get update && apt-get upgrade -y
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs

# Install Python Libraries for Model
COPY app/setup.sh /home/app/
COPY app/county-zip-huduser.csv /home/app/
RUN chmod 755 /home/app/setup.sh
RUN /home/app/setup.sh



# AWS stuff?
COPY app/entry.sh /
RUN chmod 755 /entry.sh
#RUN python /home/app/main.py
ENTRYPOINT [ "/entry.sh" ]
CMD [ "main.handler" ]