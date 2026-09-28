FROM ubuntu:24.04 AS tools

LABEL org.opencontainers.image.source=https://github.com/Stone-Soup-Tech/docker-images-android

ARG command_line_tools
ARG command_line_tools_sha1

ENV ANDROID_HOME=/opt/android-sdk-linux \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en

ENV ANDROID_SDK_ROOT=$ANDROID_HOME \
    PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

RUN test -n "$command_line_tools" \
    && test -n "$command_line_tools_sha1" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bc \
        build-essential \
        curl \
        git \
        lcov \
        libsqlite3-dev \
        libstdc++6 \
        locales \
        openjdk-21-jdk \
        openssh-client \
        sqlite3 \
        sudo \
        unzip \
        wget \
        xxd \
        zip \
    && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8

WORKDIR /opt

RUN wget -q "https://dl.google.com/android/repository/commandlinetools-linux-${command_line_tools}_latest.zip" -O android-sdk-tools.zip \
    && echo "${command_line_tools_sha1}  android-sdk-tools.zip" | sha1sum --check - \
    && mkdir -p "$ANDROID_HOME/cmdline-tools" \
    && unzip -q android-sdk-tools.zip -d "$ANDROID_HOME/cmdline-tools" \
    && mv "$ANDROID_HOME/cmdline-tools/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest" \
    && rm android-sdk-tools.zip \
    && chown -R root:root "$ANDROID_HOME"

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && mkdir -p /root/.android \
    && touch /root/.android/repositories.cfg

RUN curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install_root.sh -o /tmp/install-android-cli.sh \
    && bash /tmp/install-android-cli.sh \
    && rm /tmp/install-android-cli.sh

RUN yes | android --sdk="$ANDROID_HOME" sdk install platform-tools

RUN git config --global user.email "support@sst-ci.org" \
    && git config --global user.name "SST CI"

FROM tools AS sdk

ARG android_platform
ARG android_build_tools

ENV ANDROID_PLATFORM_VERSION=$android_platform \
    ANDROID_BUILD_TOOLS_VERSION=$android_build_tools

RUN test -n "$ANDROID_PLATFORM_VERSION" \
    && test -n "$ANDROID_BUILD_TOOLS_VERSION" \
    && yes | android --sdk="$ANDROID_HOME" sdk install \
        "platforms/android-$ANDROID_PLATFORM_VERSION" \
        "build-tools/$ANDROID_BUILD_TOOLS_VERSION"

FROM sdk AS ndk

ARG android_ndk
ENV ANDROID_NDK_VERSION=$android_ndk

RUN test -n "$ANDROID_NDK_VERSION" \
    && yes | android --sdk="$ANDROID_HOME" sdk install "ndk/$ANDROID_NDK_VERSION"
