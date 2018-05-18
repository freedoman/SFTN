import binascii
import evernote.edam.type.ttypes as Types


def EvernoteMaking(noteStore, noteTitle, noteBody, resources=[], parentNotebook=None):
    """
    Create a Note instance with title and body 
    Send Note object to user's account
    """
    newNote = Types.Note()
    newNote.title = noteTitle

    ## Build body of note

    nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
    nBody += "<en-note>{}".format(noteBody)
    if resources:
        ### Add Resource objects to note body
        nBody += "<br />"
        newNote.resources = resources
        for resource in resources:
            hexhash = binascii.hexlify(resource.data.bodyHash).decode('utf8')
            nBody += "<en-media type=\"{0}\" hash=\"{1}\" title=\"{2}\" /><br />"\
                .format(resource.mime, hexhash, resource.attributes.fileName)
    nBody += "</en-note>"
    # print(nBody)

    newNote.content = nBody

    ## parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook and hasattr(parentNotebook, 'guid'):
        newNote.notebookGuid = parentNotebook.guid

    ## Attempt to create note in Evernote account
    try:
        # pass
        note = noteStore.createNote(newNote)
    except Errors.EDAMUserException as edue:
        ## Something was wrong with the note data
        ## See EDAMErrorCode enumeration for error code explanation
        ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print("EDAMUserException:", edue)
        return None
    except Errors.EDAMNotFoundException as ednfe:
        ## Parent Notebook GUID doesn't correspond to an actual notebook
        print("EDAMNotFoundException: Invalid parent notebook GUID")
        return None
    return note