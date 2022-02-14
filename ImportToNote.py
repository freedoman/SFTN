import hashlib
import binascii
import os
import re
import filetype
import requests
import magic

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.api.client import EvernoteClient

from PreArticle import PreArticle, deleteSpecialCharacter
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
    rAttribute.fileName = deleteSpecialCharacter(url.split('/')[-1])
    # print(rAttribute)


    resource = Types.Resource()
    resource.data = rData
    # resource.mime = filetype.guess(metaData)
    resource.mime = magic.from_buffer(metaData, mime=True)
    resource.attributes = rAttribute
    # print(resource.mime)

    return resource

def findNote(notestore, notetitle, notebook):
    note_filter = NoteStoreTypes.NoteFilter(5, True, notetitle, notebook.guid)
    note_res_spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)
    note_metadata = notestore.findNotesMetadata(note_filter, 0, 1, note_res_spec)
    # print(note_metadata)
    if note_metadata.notes and note_metadata.notes[0].title == notetitle:
        return True
    return False


def getNotebook(note_store, name):
    notebook_list = note_store.listNotebooks()
    for notebook in notebook_list:
        if notebook.name == name:
            print("Notebook has existed", name)
            return notebook

    notebook = Types.Notebook()
    notebook.name = name
    notebook = note_store.createNotebook(notebook)
    print("Create notebook", name)
    return notebook

def ImportToNote(auth_token):
    notebookName, data = PreArticle()
    # print(notebookName, data)
    # return

    client = EvernoteClient(token=auth_token, sandbox=False, china=True)
    # client.service_host = 'app.yinxiang.com'
    # print(client)

    user_store = client.get_user_store()
    note_store = client.get_note_store()



    # note = Types.Note()
    # note.title = "I'm a test note!"
    # note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    # note.content += '<en-note>Hello, world!</en-note>'
    # note = note_store.createNote(note)

    # print(note.guid)
    # return

    notebook = getNotebook(note_store, notebookName)

    # findNote(note_store, 'jn00  发刊词  从此成为一个懂财务的人', notebook)
    # return

    # # print(note_store)
    # for n in note_store.listNotebooks():
    #     print(n.name, n.guid)

    for title, info in data.items():
        noteTitle = title
        noteBody = ""
        noteResource = []
        # print(title)
        for wav in info["wav"]:
            # print(wav)
            resource = getResource(wav)
            if resource:
                noteResource.append(resource)

        texts = list(info["text"])
        texts.sort()
        for text in texts:
            # print(text)
            resource = getResource(text)
            if resource:
                noteResource.append(resource)

        # print("ok")
        # print(noteTitle, noteBody)
        if findNote(note_store, noteTitle, notebook):
            print("Note has existed", noteTitle)
        else:
            if EvernoteMaking(note_store, noteTitle, noteBody, noteResource, notebook):
                print("Create note", noteTitle)
            else:
                print("Failed create note", noteTitle)

if __name__ == '__main__':
    auth_token = "S=s10:U=111bb6d:E=17f1778bbc6:C=17ef36c34f0:P=1cd:A=en-devtoken:V=2:H=55b907782f13bb927b7f6c1e0e9a9c24"
    ImportToNote(auth_token)



















