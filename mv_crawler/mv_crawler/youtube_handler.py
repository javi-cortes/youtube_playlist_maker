#!/usr/bin/python

import os
import sys

import httplib2
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "client_secrets.json")
)

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % CLIENT_SECRETS_FILE

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(
    CLIENT_SECRETS_FILE,
    message=MISSING_CLIENT_SECRETS_MESSAGE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()),
)


def create_playlist():
    # # This code creates a new, private playlist in the authorized user's channel.
    return (
        youtube.playlists()
        .insert(
            part="snippet,status",
            body=dict(
                snippet=dict(
                    title="Test Playlist",
                    description="A private playlist created with the YouTube API v3",
                ),
                status=dict(privacyStatus="private"),
            ),
        )
        .execute()
    )


def get_list():
    playlists_list_response = (
        youtube.playlists()
        .list(
            part="id,snippet,status",
            channelId="UCAr548-qU8aVVIZt7yjUKDA",
        )
        .execute()
    )

    print(playlists_list_response)


def add_video(playlist_id, resource_id):
    try:
        return (
        youtube.playlistItems()
        .insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    playlistId=playlist_id,
                    resourceId={
                        "kind": "youtube#video",
                        "videoId": resource_id,
                    },
                ),
            ),
        )
        .execute()
    )
    except Exception as e:
        print("\n")
        print(e)
        print(f"resource not found: {resource_id}")
        print("\n")


if __name__ == "__main__":
    playlist_response = create_playlist()
    playlist_id = playlist_response['id']
    print(f"{playlist_id} createad")
    print("END")
