import hashlib
import binascii
import os
import filetype
import requests

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

from PreArticle import PreArticle
from EvernoteMaking import EvernoteMaking

def getResource(url):

    with open(url, "rb") as f:
        metaData = f.read()
    
    md5 = hashlib.md5()
    md5.update(metaData)
    metaHash = md5.digest()
    # metaHashHex = binascii.hexlify(metaHash)
    # metaHashStr = metaHashHex.decode("UTF-8")

    rData = Types.Data()
    rData.size = len(metaData)
    rData.bodyHash = metaHash
    # print(rData.bodyHash)
    rData.body = metaData

    rAttribute = Types.ResourceAttributes()
    rAttribute.fileName = url.split('/')[-1]
    # print(rAttribute)


    resource = Types.Resource()
    resource.data = rData
    resource.mime = filetype.guess(metaData).mime
    resource.attributes = rAttribute
    # print(resource.mime)

    return resource



def ImportToNote(auth_token):
    data = PreArticle()

    client = EvernoteClient(token=auth_token, sandbox=True,china=False)

    user_store = client.get_user_store()
    note_store = client.get_note_store()

    for title, info in data.items():
        noteTitle = title
        noteBody = ""
        noteResource = []
        for wav in info["wav"]:
            resource = getResource(wav)
            if resource:
                # print(resourcee)
                noteResource.append(resource)

        for text in info["text"]:
            resource = getResource(text)
            if resource:
                noteResource.append(resource)

        note = EvernoteMaking(note_store, noteTitle, noteBody, noteResource)
        print(note.guid)

if __name__ == '__main__':
    auth_token = ""
    ImportToNote(auth_token)



















