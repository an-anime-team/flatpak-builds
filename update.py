#!/usr/bin/env python3

# This script checks if a newer version of the launcher is available, and if so, updates all relevant files.
#
# Dependencies that aren't in the standard library:
# - requests
# - lxml
# - ruamel.yaml
#
# This script was tested using Python 3.10.4; older versions may not work.

from functools import reduce
from hashlib import sha256
from typing import OrderedDict
import requests
from lxml import etree
from ruamel.yaml import YAML
import re

METADATA_FILE = 'com.gitlab.KRypt0n_.an-anime-game-launcher.metainfo.xml'
MANIFEST_FILE = 'com.gitlab.KRypt0n_.an-anime-game-launcher.yml'

flatpakMetadata = etree.parse(METADATA_FILE)
flatpakReleases = flatpakMetadata.xpath('/component/releases/release')
currentFlatpakRelease = reduce(lambda x, y: x if x.attrib['version'] > y.attrib['version'] else y, flatpakReleases)
print(f'Current flatpak release: {currentFlatpakRelease.attrib["version"]}')

releasesResponse = requests.get('https://gitlab.com/an-anime-team/an-anime-game-launcher/-/releases.json')
releasesResponse.json()
gitlabReleases: list[dict] = releasesResponse.json()
latestRelease = reduce(lambda x, y: x if x['released_at'] > y['released_at'] else y, gitlabReleases)
latestReleaseDate = latestRelease['released_at'].split('T')[0]
print(f'Latest release on GitLab: {latestRelease["tag"]}, released on {latestReleaseDate}')

if(latestRelease['tag'] > currentFlatpakRelease.attrib['version']):
    print('New version available on GitLab!')
    
    newReleaseElement = etree.Element('release', version=latestRelease['tag'], date=latestReleaseDate)

    descriptionElement = etree.SubElement(newReleaseElement, 'description')
    descriptionMarkdown: str = latestRelease['description']
    changesMarkdown = descriptionMarkdown.split("## What's changed?\n\n")[1].split("\n\n")[0]
    changesListItems = changesMarkdown.split('- ')

    for item in changesListItems:
        text = item.strip()
        if text == '':
            continue
        element = etree.SubElement(descriptionElement, 'p')
        element.text = text

    print('Generated release element:')
    print(str(etree.tostring(newReleaseElement, pretty_print=True), 'utf-8'))

    flatpakMetadata.xpath('/component/releases')[0].insert(0, newReleaseElement)

    yaml = YAML()
    with open(MANIFEST_FILE, 'r+') as manifestFile:
        data: OrderedDict = yaml.load(manifestFile)

        for module in data['modules']:
            if module['name'] == 'an-anime-game-launcher':
                for source in module['sources']:
                    if 'url' in source:
                        aaglSource: OrderedDict = source
                        break
                break
        
        appimageRegex = re.compile('/uploads/[\da-f]+/An_Anime_Game_Launcher.AppImage', re.MULTILINE)
        appimageUrl = appimageRegex.search(descriptionMarkdown).group(0)
        appimageUrl = f'https://gitlab.com/KRypt0n_/an-anime-game-launcher{appimageUrl}'
        
        print(f'Calculating SHA256...', end='', flush=True)
        appimageResponse = requests.get(appimageUrl)
        appimageSha256 = sha256(appimageResponse.content).hexdigest()

        print(f'\rDownload URL: {appimageUrl}')
        print(f'SHA256: {appimageSha256}')

        aaglSource['url'] = appimageUrl
        aaglSource['sha256'] = appimageSha256

        manifestFile.seek(0)
        manifestFile.truncate()

        # Update metadata and manifest
        etree.indent(flatpakMetadata, space='  ')
        flatpakMetadata.write(METADATA_FILE, xml_declaration=True, encoding='utf-8')
        yaml.dump(data, manifestFile)

    print(f'\nIf something looks wrong, run `git checkout {METADATA_FILE} {MANIFEST_FILE}` to revert the changes, slap krypton with a fish, and fix this script; he probably changed the format of the description.')

else:
    print('Flatpak is already up to date.')
