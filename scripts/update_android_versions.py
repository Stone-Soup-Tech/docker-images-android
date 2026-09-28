#!/usr/bin/env python3
"""Update versions.yml from Google's stable Android SDK repository metadata."""

import argparse
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_REPOSITORY = "https://dl.google.com/android/repository/repository2-3.xml"


def child(element, name):
    if element is None:
        return None
    return next((item for item in element if item.tag.rsplit("}", 1)[-1] == name), None)


def stable(package):
    channel = child(package, "channelRef")
    revision = child(package, "revision")
    return (
        package.get("obsolete") != "true"
        and (channel is None or channel.get("ref") == "channel-0")
        and revision is not None
        and child(revision, "preview") is None
    )


def version_key(value):
    return tuple(int(part) for part in value.split("."))


def latest(packages, pattern):
    matches = []
    for package in packages:
        match = pattern.fullmatch(package.get("path", ""))
        if match and stable(package):
            matches.append((version_key(match.group(1)), match.group(1), package))
    if not matches:
        raise RuntimeError(f"No stable package matched {pattern.pattern}")
    return max(matches, key=lambda item: item[0])[1:]


def text(element, name):
    item = child(element, name)
    return item.text.strip() if item is not None and item.text else ""


def command_line_tools(packages):
    package = next(
        (
            package
            for package in packages
            if package.get("path") == "cmdline-tools;latest" and stable(package)
        ),
        None,
    )
    if package is None:
        raise RuntimeError("No stable command-line tools package was found")
    archives = child(package, "archives")
    for archive in archives or []:
        if text(archive, "host-os") != "linux":
            continue
        complete = child(archive, "complete")
        url = text(complete, "url")
        match = re.fullmatch(r"commandlinetools-linux-(\d+)_latest\.zip", url)
        if match:
            checksum = child(complete, "checksum")
            if checksum is None or checksum.get("type") != "sha1" or not checksum.text:
                raise RuntimeError("The command-line tools archive has no SHA-1 checksum")
            return match.group(1), checksum.text.strip()
    raise RuntimeError("No stable Linux command-line tools archive was found")


def resolve(repository):
    with urllib.request.urlopen(repository, timeout=30) as response:
        root = ET.parse(response).getroot()
    packages = [item for item in root if item.tag.rsplit("}", 1)[-1] == "remotePackage"]
    platform, _ = latest(packages, re.compile(r"platforms;android-(\d+(?:\.\d+)*)"))
    build_tools, _ = latest(packages, re.compile(r"build-tools;(\d+(?:\.\d+)*)"))
    ndk, _ = latest(packages, re.compile(r"ndk;(\d+(?:\.\d+)*)"))
    tools, tools_sha1 = command_line_tools(packages)
    return platform, build_tools, ndk, tools, tools_sha1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--versions-file", default="versions.yml")
    args = parser.parse_args()

    versions_path = Path(args.versions_file)
    values = resolve(args.repository)
    output = """android_sdk:
  platform: "{}"
  build_tools: "{}"
  ndk: "{}"
  command_line_tools: "{}"
  command_line_tools_sha1: "{}"
""".format(*values)
    versions_path.write_text(output, encoding="utf-8")
    print(f"Updated {args.versions_file}: platform {values[0]}, build-tools {values[1]}, NDK {values[2]}")


if __name__ == "__main__":
    main()
