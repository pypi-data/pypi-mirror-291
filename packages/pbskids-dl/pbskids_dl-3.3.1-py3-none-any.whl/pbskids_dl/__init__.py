#!/usr/bin/env python3
#   Copyright 2024 The pbskids-dl team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import pbskids_dl.api
def download(url, argument=None):
    args = pbskids_dl.api.download_gen_args(url, argument)
    script, soup = pbskids_dl.api.download_fetch_script(args["url"])
    pbskids_dl.api.download_check_drm(soup)
    assets, videos = pbskids_dl.api.download_find_assets(script)
    if (args["filename"] != None):
        vid_title = args["filename"]
    else:
        vid_title = assets['title'].replace('/','+').replace('\\','+') + '.mp4'
    print(vid_title)
    for video in videos:
        if (video['profile'] == 'mp4-16x9-baseline'):
            pbskids_dl.api.download_dl_video(vid_title, video, args["filename"])
            print("\nDownload Complete!")
            return True
    print("\nThe operation failed...")
    return False