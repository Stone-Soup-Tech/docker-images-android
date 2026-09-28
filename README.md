# Docker images with Android SDK

[![Build Android images](https://github.com/Stone-Soup-Tech/docker-images-android/actions/workflows/build.yml/badge.svg)](https://github.com/Stone-Soup-Tech/docker-images-android/actions/workflows/build.yml)

You can either [use it in CI](https://cirrus-ci.org/examples/#android) or run
locally via Docker:

```console
docker run --rm -it \
  --volume "$PWD:/build" \
  --workdir /build \
  ghcr.io/stone-soup-tech/android-sdk:latest \
  ./gradlew :app:assembleDebug
```

The example above mounts current working directory and runs a Gradle build.

## Image tags

- `latest` and `<api>` contain the latest stable Android SDK platform and build tools.
- `latest-ndk` and `<api>-ndk` additionally contain the latest stable Android NDK.
- The standalone `tools` image is currently disabled; the SDK and NDK images still
  use the internal tools build stage.

For reproducible builds, use an API tag such as `36` or `36-ndk`. The moving
tags are updated after an automated version-update pull request is merged.

## GitHub Container Registry

https://github.com/Stone-Soup-Tech/docker-images-android/pkgs/container/android-sdk
