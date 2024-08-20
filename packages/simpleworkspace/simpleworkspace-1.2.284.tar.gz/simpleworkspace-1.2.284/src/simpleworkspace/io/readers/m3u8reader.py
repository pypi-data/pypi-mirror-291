import re as _re
from typing import TextIO, BinaryIO


class _NoneQuotedValue(str):... #basically a string, but this instance of string does not get quoted on export

class M3U8Reader: 
    class Entry:
        def __init__(self, Tag:str, Attributes:dict[str, str] = None, URI:str|None = None):
            self.Tag = Tag
            self.Attributes:dict[str, str] = {} if Attributes is None else Attributes
            '''m3u8 attributes are case insensitive'''
            self.URI = URI
            self._comment = None

        def __str__(self):
            strBuilder = f'{self.Tag}'

            #region special tag formats
            if(self.Tag == ''): # used for comments and empty lines
                return self._comment
            if(self.Tag == '#EXTINF'):                      #format "#EXTINF:<DURATION>, [Optional]<TITLE>"
                strBuilder += f':{self.Attributes[0]}'
                if(1 in self.Attributes):
                    strBuilder += ', ' + self.Attributes[1]
                strBuilder += '\n' + self.URI
                return strBuilder
            elif(self.Tag == '#EXT-X-VERSION'):             #format "#EXT-X-VERSION:<VERSION>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-PLAYLIST-TYPE'):       #format "#EXT-X-PLAYLIST-TYPE:<TYPE>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-TARGETDURATION'):      #format "#EXT-X-TARGETDURATION:<DURATION>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-MEDIA-SEQUENCE'):      #format "#EXT-X-MEDIA-SEQUENCE:<SEQUENCE_NUMBER>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-START'):               #format "#EXT-X-START:<TIME_OFFSET>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-ALLOW-CACHE'):         #format "#EXT-X-ALLOW-CACHE:<yes|no>"
                return strBuilder + ":" + self.Attributes[0]
            elif(self.Tag == '#EXT-X-PROGRAM-DATE-TIME'):   #format "#EXT-X-PROGRAM-DATE-TIME:<DATE_TIME>"
                return strBuilder + ":" + self.Attributes[0]
            #endregion special tag formats

            if(self.Tag == '#EXT-X-STREAM-INF'): #specification states mandatory int attribute bandwidth, therefore reasonable to avoid qouting
                self.Attributes['BANDWIDTH'] = _NoneQuotedValue(self.Attributes['BANDWIDTH'])
                if("RESOLUTION" in self.Attributes): #not mandatory, but specs wants it without quotes eg "<width>x<height>"
                    self.Attributes['RESOLUTION'] = _NoneQuotedValue(self.Attributes['RESOLUTION'])


            if(len(self.Attributes) > 0):
                attributeStrings = []
                for key,value in self.Attributes.items():
                    if(isinstance(value, str)) and (type(value) is not _NoneQuotedValue):
                        value = f'"{value}"'
                    attributeStrings.append(f'{key}={value}')
                strBuilder += ':' + ','.join(attributeStrings)
            if(self.URI):
                strBuilder += '\n' + self.URI
            return strBuilder
    
    _attributePattern = _re.compile(r'\s*(.+?)\s*=\s*((?:".*?")|.*?)\s*(?:,|$)')
    def __init__(self) -> None:
        self.Entries:list[M3U8Reader.Entry] = [] #some lines might not be entries such as empty lines or comments

    @property
    def IsMaster(self):
        for entry in self.Entries:
            if(entry.Tag == '#EXT-X-STREAM-INF'):
                return True
        return False

    def LoadFile(self, filepath:str):
        with open(filepath, 'r') as fp:
            self.Load(fp)

    def Load(self, stream:TextIO|BinaryIO):
        stream.seek(0)
        data = stream.read()
        if isinstance(stream, BinaryIO):
            data = data.decode('utf-8')

        entry = None
        for line in data.splitlines():
            line = line.strip()
            if(entry is not None) and (line == '' or line.startswith('#')):
                #empty line or comment or another entry, marks the finish of previous entry
                self.Entries.append(entry)
                entry = None

            if(line.startswith('#EXT')):
                tagAndAttributes = line.split(':', maxsplit=1)
                entry = M3U8Reader.Entry(tagAndAttributes[0])
                if(entry.Tag == '#EXTINF'):                     #format "#EXTINF:<DURATION>, [Optional]<TITLE>"
                    extinf_attribs = tagAndAttributes[1].split(',', maxsplit=1)
                    entry.Attributes[0] = extinf_attribs[0].strip()
                    if(len(extinf_attribs) > 1):
                        entry.Attributes[1] = extinf_attribs[1].strip()
                elif(entry.Tag == '#EXT-X-VERSION'):            #format "#EXT-X-VERSION:<VERSION>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-PLAYLIST-TYPE'):      #format "#EXT-X-PLAYLIST-TYPE:<TYPE>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-TARGETDURATION'):     #format "#EXT-X-TARGETDURATION:<DURATION>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-MEDIA-SEQUENCE'):     #format "#EXT-X-MEDIA-SEQUENCE:<SEQUENCE_NUMBER>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-START'):              #format "#EXT-X-START:<TIME_OFFSET>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-ALLOW-CACHE'):        #format "#EXT-X-ALLOW-CACHE:<yes|no>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(entry.Tag == '#EXT-X-PROGRAM-DATE-TIME'):  #format "#EXT-X-PROGRAM-DATE-TIME:<DATE_TIME>"
                    entry.Attributes[0] = tagAndAttributes[1].strip()
                elif(len(tagAndAttributes) > 1):
                    for pair in self._attributePattern.findall(tagAndAttributes[1]):
                        key, value = pair
                        entry.Attributes[key] = value.strip('"')
            elif(line == '') or (line.startswith('#')):  #since line starts with # but not #EXT, then it must be comment line
                dummyEntry = M3U8Reader.Entry('')
                dummyEntry._comment = line
                self.Entries.append(dummyEntry) #preserve empty newlines and comments on final export
            else:
                entry.URI = line
        if(entry is not None):
            self.Entries.append(entry)
        stream.seek(0)

    def Save(self, stream:TextIO|BinaryIO):
        stream.seek(0)     # Move the cursor to the beginning of the stream
        stream.truncate(0) # Clear the stream by truncating it

        data = str(self)
        if(isinstance(stream, BinaryIO)):
            data = data.encode('utf-8')
        stream.write(data)
        stream.flush()
        stream.seek(0)     #reset the cursor back to start

    def SaveFile(self, filepath:str):
        with open(filepath, "w") as fp:
            self.Save(fp)

    def GetTags_EXTINF(self):
        """Get entries with tag #EXTINF which points to media URI files"""
        for entry in self.Entries:
            if(entry.Tag == '#EXTINF'):
                yield entry

    def GetTags_EXT_X_STREAM_INF(self):
        """Only master playlist will have these tags, gets #EXT-X-STREAM-INF tags which points to the actual media playlist"""
        for entry in self.Entries:
            if(entry.Tag == '#EXT-X-STREAM-INF'):
                yield entry
    
    def __str__(self):
        return '\n'.join([str(entry) for entry in self.Entries])
