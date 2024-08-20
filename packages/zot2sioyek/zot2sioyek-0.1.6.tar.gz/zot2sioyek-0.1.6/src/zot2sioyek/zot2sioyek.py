"""

Script to embed zotero highlights to sioyek.

Author: eduardotcampos@usp.br

Contain also some utils to manage this highlights.

Based on pyzotero and sqlite3.

=======
CONFIGS
=======

To use this script define the variables:

ZOTERO_LIBRARY_ID: Your personal library ID available in https://www.zotero.org/settings/keys,
in the section Your userID for use in API calls.

ZOTERO_API_KEY: Api key, you can obtain in https://www.zotero.org/settings/keys/new.

ZOTERO_LIBRARY_TYPE: Zotero library type, can be 'user' or 'group'.

LOCAL_DATABASE_FILE_PATH: Sioyek .db local database file path.

SHARED_DATABASE_FILE_PATH: Sioyek .db shared database file path.

SIOYEK_PATH: Sioyek program path.

ZOTERO_TO_SIOYEK_COLORS: Sioyek highlight type letter associated to each zotero highlight color.

ZOTERO_LOCAL_DIR: Zotero local PDFs directory like 'home/user/Zotero/storage'

"""

import argparse
import textwrap
from difflib import SequenceMatcher
import hashlib
import datetime
import uuid
import sys
import pathlib
import sqlite3
from pyzotero import zotero
from os import path
from os import walk
from collections import namedtuple
from dataclasses import dataclass
from sioyek.sioyek import Sioyek, DocumentPos, clean_path

ZoteroHighlight = namedtuple("Highlight", ["text", "color", "page", "date_added", "date_modified"])

ZOTERO_LIBRARY_ID = ""
ZOTERO_LOCAL_DIR = ""
ZOTERO_LIBRARY_TYPE = "user"
ZOTERO_API_KEY = ""
LOCAL_DATABASE_FILE_PATH = ""
SHARED_DATABASE_FILE_PATH = ""
SIOYEK_PATH = ""
ZOTERO_TO_SIOYEK_COLORS = {
    "#5fb236": "g",
    "#a28ae5": "a",
    "#e56eee": "p",
    "#2ea8e5": "b",
    "#ff6666": "r",
    "#f19837": "o",
    "#ffd400": "y",
}


# -TODO:Check annotationSortIndex value meaning
@dataclass
class ZoteroHighlights:
    """

    A class to extract and store zotero highlight annotations from the user database.

    Class to handle highlight type annotations from zotero pdfs, being possible to specify
    the documents to manipulate based on the pdf file name or on the the highlight date of creation.

    Attributes
    ----------
    highlights : list
        list containing Highlight class elements, with the keys:
        text, text of the highlight;
        color, str of the html hex code;
        page, str of the page number;
        date_added, Addition of the highlight, formatted like %Y-%m-%d %H:%M:%S
        date_modified, Addition of the highlight, formatted like %Y-%m-%d %H:%M:%S

    zotero : pyzotero.zotero.Zotero
        pyzotero class object, obtained from the user zotero database, from the given
        library id, library type, and api key

    annotation_data : list
        list of dicts, being each dict a highlight/annotation formatted like:

            key : str
                attachment item id, like 'VENEZY2N'

            version : int
                version of the api

            parentItem : str
                item id of the zotero library parent item of the attachment, like 'I9M4ZAZ9'

            itemType : str
                type of the data, like 'annotation'

            annotationType : str
                type of the annotation, like 'highlight'

            annotationText : str
                The text that is highlighted

            annotationComment : str
                Comment of the annotation

            annotationColor : str
                Html hex code string

            annotationPageLabel : str
                Page number string or label if exists

            annotationSortIndex : str
                Formated like '0000|001579|0359'

            annotationPosition : str
                string of a dict formatted like:
                    pageIndex : int
                        page number index (start in 0)
                    rects : list[list]
                        list of a list containing start x position, start y position,
                        end x position and end y position of the highlight

            tags : list
                Tags of the item

            relations : dict

            dateAdded : str
                Date formatted like %Y-%m-%dT%H:%M:%SZ, like '2024-08-13T15:28:42Z'

            dateModified : str
                Date formatted like %Y-%m-%dT%H:%M:%SZ, like '2024-08-13T15:28:42Z'

    Methods
    -------
    get_highlights_by_filename() -> dict
        Returns Main data of the given filename highlight if exists. The dict keys are
        annotationText, annotationColor, annotationPageLabel, and the rectangular values from
        annotationPosition (top, left, bottom, right; x2).

    get_highlights_by_date() -> dict
        Same from above Method, but instead of inputting the filename string, takes a date, and
        queryes all the files more recent than the given date.

    _extract_highlights()
        Used to build the the 2 methods above.

    list_annotation_attribute_by_filename(filename:str) -> ZoteroHighlights.set
        Return all file available attributes names, like annotationPosition.

    assign_annotation_attributes(filename:str) -> list
        Return a zotero documen list of highlight dicts.

    Examples
    --------
    annotation_data example:
    [{'key': 'VENEZY2N', 'version': 8758, 'parentItem': 'I9M4ZAZ9', 'itemType': 'annotation',
      'annotationType': 'highlight', 'annotationText': 'photosystem (PS) II photoinhibition',
      'annotationComment': '', 'annotationColor': '#ff6666', 'annotationPageLabel': '1',
      'annotationSortIndex': '00000|001579|00359',
      'annotationPosition': '{"pageIndex":0,"rects":[[47.849,410.948,190.332,423.397]]}',
      'tags': [], 'relations': {}, 'dateAdded': '2024-08-13T15:28:42Z',
      'dateModified': '2024-08-13T15:28:42Z'},
     {'key': 'NJNN4SEF', 'version': 8757, 'parentItem': 'I9M4ZAZ9', 'itemType': 'annotation',
      'annotationType': 'highlight',
      'annotationText': 'and this accumulation was correlated with the extent of',
      'annotationComment': '', 'annotationColor': '#a28ae5', 'annotationPageLabel': '1',
      'annotationSortIndex': '00000|001537|00351',
      'annotationPosition': '{"pageIndex":0,"rects":[[306.815,422.555,549.921,431.441]]}',
      'tags': [], 'relations': {}, 'dateAdded': '2024-08-13T15:28:36Z',
      'dateModified': '2024-08-13T15:28:36Z'}
     ]

    """

    def __init__(self, library_id, library_type, api_key):
        self.zotero = zotero.Zotero(library_id, library_type, api_key)
        self.highlights = []
        self.annotations_data = []

    def _extract_highlights(self, item_key):
        """

        Given a zotero item key, extract it highlights.

        Parameters
        ----------
        item_key : str
            str of a zotero item key

        Notes
        -----
        This function extracts the higlights to the class lists highlights and annotation_data

        Seee Also
        ---------
        get_highlights_by_filename(filename:str)

        """
        annotations = self.zotero.children(item_key, itemType="annotation")
        for annotation in annotations:
            if annotation["data"]["annotationType"] == "highlight":
                text = annotation["data"].get("annotationText", "")
                color = annotation["data"].get("annotationColor", "")
                page = annotation["data"].get("annotationPageLabel", "")
                date_added = annotation["data"].get("dateAdded", "")
                date_modified = annotation["data"].get("dateModified", "")
                highlight = ZoteroHighlight(text, color, page, date_added, date_modified)
                self.highlights.append(highlight)
                self.annotations_data.append(annotation["data"])

    def get_highlights_by_filename(self, filename):
        """
        Given a zotero file name, extracts it highlights to the class lists.

        Parameters
        ----------
        filename : str
            Zotero database containing file name

        Returns
        -------
        None

        """
        items = self.zotero.items(q=filename, itemType="attachment")
        for item in items:
            if "filename" in item["data"] and item["data"]["filename"] == filename:
                self._extract_highlights(item["key"])
                break

    def get_highlights_by_date(self, date):
        """

        Given a date, return all zotero highlights made after that.

        Parameters
        ----------
        date : datetime.datetime
            Date to filter highlights to start at

        Returns
        -------
        None

        """
        date_str = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        items = self.zotero.everything(self.zotero.items(since=date_str, itemType="attachment"))
        for item in items:
            self._extract_highlights(item["key"])

    def list_annotation_attributes_by_filename(self, filename):
        """

        Return all file available attributes names, like annotationPosition.

        Parameters
        ----------
        filename : str
            File name of a zotero database present pdf file.

        Returns
        -------
        all_keys : ZoteroHighlights.set
            All available attributes names, seted on the class object

        Examples
        --------
        Example of a returned all_keys
        {'annotationColor', 'annotationPosition', 'annotationSortIndex',
         'parentItem', 'annotationType', 'itemType', 'version', 'annotationText',
         'tags', 'annotationComment', 'key', 'dateAdded', 'annotationPageLabel',
         'dateModified', 'relations',
        }

        """
        items = self.zotero.items(q=filename, itemType="attachment")
        all_keys = set()
        for item in items:
            if "filename" in item["data"] and item["data"]["filename"] == filename:
                annotations = self.zotero.children(item["key"], itemType="annotation")
                for annotation in annotations:
                    all_keys.update(annotation["data"].keys())
                break
        return all_keys

    def assign_annotation_attributes(self, filename):
        """

        Get a zotero documen list of highlight dicts.

        Parameters
        ----------
        filename : str
            File name of a zotero pdf document.

        Returns
        -------
        attributes_list : list
            List of dicts, with the keys:
                key : str
                    Zotero item id
                version : int
                parentItem : str
                    Zotero parent item id
                itemType : str
                    Type of the dict, like 'annotation'
                annotationType : str
                    Type of the annotation, like 'highlight'
                annotationText : str
                    The text highlighted itself
                annotationComment : str
                annotationColor : str
                    Html hex code
                annotationPageLabel : str
                    page number
                annotationSortIndex : str
                    like '00001|000655|00281'
                annotationPosition : str
                    str of a dict , with the keys:
                        pageIndex : int
                        rects : list
                            list with begin_x begin_y, end_x end_y
                tags : list
                relations : dict
                dateAdded : str
                    date formatted like "%Y-%m-%dT%H:%M:%SZ"
                dateModified : str
                    date formatted like "%Y-%m-%dT%H:%M:%SZ"

        """
        self.get_highlights_by_filename(filename)
        attributes_list = []
        for annotation_data in self.annotations_data:
            attributes = {}
            for attr, value in annotation_data.items():
                attributes[attr] = value
            attributes_list.append(attributes)
        return attributes_list


@dataclass
class SioyekHighlights:
    """
    Sioyek highligts class.

    Attributes
    ----------
    local_database_file_path : str
        Path to the local database .db file path

    shared_database_file_path : str
        Path to the shared database .db file path

    sioyek_path : str
        Path to the sioyek executable

    column_names : list
        List of strings, with the name of the sql columns from the database, like:
            ['id', 'path', 'hash']

    zotero_hl_to_sioyek : dict
        Dictionary wich keys are zotero highlight html colors, and the value is the sioyek
        highlight letter, to which this highlights should be when embedding in sioyek

    docs : list
        list of dicts, containing the documents in the sioyek database, having each dict the id
        of a file, the path to this file, and the hash to this file path, for example:

    sioyek : sioyek.sioyek.Sioyek
        Sioyek python class object, to execute sioyek commands

    Methods
    -------
    list_files()
        List all file paths and hashes in the sioyek database

    list_hash(file:str)
        Given a file, print this file hash

    _get_hash(file:str) -> str
        Similar to list_hash, but return this file hash

    _get_attributes(file:str) -> dict
        Return a dict with the highlights data fields.

    list_attributes(file:str)
        Print all attributes from sioyek database file, and this attributes values.
        the attributes are bookmarks, highlights, links and marks.

    _to_abs(highlights:ZoteroHighlights.highlights, file_path:str) -> tuple
        Get the absolute position of a document highlight, based on the highlight text, the
        highlight page, and the document file path.

    _convert_zot_date_to_sioyek(date_str:str) -> str
        Convert a date from zotero default format to sioyek format.

    _calculate_md5(file_path:str) -> str
        Calculate a file md5sum hash.

    get_zotero_to_sioyek_highlights(file_path:str,
                                     zotero_highlights:__main__.ZoteroHighlights) -> list
        Get a zotero file highlights, formatted in a dict with essential data to embed to sioyek.

    insert_highlight(file_path:str, zotero_highlights:__main__.ZoteroHighlights)
        Insert a zotero file annotations to this sioyek file database.

    Examples
    --------
    docs attribute example of list:
    [{'id': 1,
      'path': '/home/user/Zotero/storage/RZ54E2RK/processing_of_calcium_sulfate_the_.pdf',
      'hash': '04456fccdb9854ca3bea51d6442d9bb2',
     },
     {'id': 2,
      'path': '/home/user/Programação/LaTeX/tutorial/tut.pdf',
      'hash': '4e35e5dca3a3f648ba6594453347f498',
     },
     {'id': 3,
      'path': '/home/user/Library/python/numpydoc.pdf',
      'hash': '82f60ed6cc8e494a82d24d84105065b0',
     }
    ]
    """

    def __init__(self):
        self.local_database_file_path = LOCAL_DATABASE_FILE_PATH
        self.shared_database_file_path = SHARED_DATABASE_FILE_PATH
        self.sioyek_path = SIOYEK_PATH
        self.column_names = []
        self.zotero_hl_to_sioyek = ZOTERO_TO_SIOYEK_COLORS
        with sqlite3.connect(self.local_database_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM document_hash")
            documents = cursor.fetchall()
            self.column_names = [description[0] for description in cursor.description]
        self.docs = [dict(zip(self.column_names, book)) for book in documents]
        self.sioyek = Sioyek(
            self.sioyek_path, self.local_database_file_path, self.shared_database_file_path
        )

    def list_files(self):
        """List all file paths and hashes in the sioyek database."""
        for doc in self.docs:
            print(doc["hash"], ":", doc["path"])

    def list_hash(self, file):
        """

        Given a file, prints this file hash.

        Parameters
        ----------
        file : str

        Returns
        -------
        None

        """
        found = False
        for doc in self.docs:
            if pathlib.Path(doc["path"]).samefile(file):
                print(doc["hash"])
                found = True
                break
        if not found:
            print("File not found in the database.")

    def _get_hash(self, file_path):
        """

        Similar to list_hash, but return this file hash.

        Parameters
        ----------
        file_path : str
            file complete path

        Returns
        -------
        result : str
            String of the file md5sum hash

        """
        found = False
        for doc in self.docs:
            if pathlib.Path(doc["path"]).samefile(file_path):
                result = doc["hash"]
                found = True
                break
        if not found:
            print("File not found in the database.")
        return result

    def _get_attributes(self, file_path):
        """

        Return a dict with the highlights data fields.

        Parameters
        ----------
        file_path : str
            String of a file path.

        Returns
        -------
        from_annotation : dict
            dict with the keys:
                bookmarks : list
                highlights : list
                    list of dicts, with the keys:
                        id : int
                            number of the highlight index
                        document_path : str
                            hash str of the document path
                        desc : str
                            text of the highlight
                        text_annot : str
                            annotation of the highlight
                        type : str
                            letter of the sioyek highlight type
                        creation_time : str
                            date formatted like %Y-%m-%d %H:%M:%S
                        modification_time : str
                            date formatted like %Y-%m-%d %H:%M:%S
                        uuid : str
                            uuid of the highlight
                        begin_x : float
                            coordinate of the sioyek absolute position x begin
                        begin_y : float
                            coordinate of the sioyek absolute position y begin
                        end_x : float
                            coordinate of the sioyek absolute position x end
                        end_y : float
                            coordinate of the sioyek absolute position y end

        Examples
        --------
        An example of a returned from_annotations dict:
        {'bookmarks': [],
         'highlights': [{'id': 1,
                         'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
                         'desc': 'thermodynamic databases.',
                         'text_annot': 'None',
                         'type': 'i', 'creation_time': '2024-08-13 15:53:45',
                         'modification_time': '2024-08-13 15:53:45',
                         'uuid': '0b573e66-66aa-4fc7-886b-2e21d94104af',
                         'begin_x': -198.7873992919922, 'begin_y': 1121.375,
                         'end_x': -156.77529907226562, 'end_y': 1155.4794921875}],
         'links': [],
         'marks': []}

        """
        table_names = [
            ("bookmarks", "document_path"),
            ("highlights", "document_path"),
            ("links", "src_document"),
            ("marks", "document_path"),
        ]
        from_annotations = dict()
        from_hash = self._get_hash(file_path)
        for table, column_name in table_names:
            with sqlite3.connect(self.shared_database_file_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE {column_name} = ?", (from_hash,))
                annotations = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                from_annotations[table] = [dict(zip(column_names, bm)) for bm in annotations]
        return from_annotations

    def list_attributes(self, file_path):
        """

        Print all attributes from sioyek database file, and this attributes values.

        the attributes are bookmarks, highlights, links and marks.

        Parameters
        ----------
        file_path : str
            String of a file path.

        Returns
        -------
        None

        """
        from_annotations = self._get_attributes(file_path)
        for key, attribute in from_annotations.items():
            print(f"{key}\n{'=' * len(key)}")
            for idx, value in enumerate(attribute):
                print(f"{idx + 1}\n--------")
                for i, j in value.items():
                    print(f"{i}: {j}")
                print("\n")

    def _to_abs(self, highlight, file_path):
        """

        Get the absolute position of a document highlight, based on the text, page and file path.

        Parameters
        ----------
        highlight : ZoteroHighlights.highlight
            Zotero highlights class object

        file_path : str
            String of a file path

        """
        doc = self.sioyek.get_document(file_path)
        highlight_page = int(highlight.page)
        begin, end = doc.get_text_selection_begin_and_end((highlight_page) - 1, highlight.text)
        if begin == (None, None) or end == (None, None):
            raise ValueError("highlight text not found")
        offset_x = (doc.page_widths[highlight_page - 1]) / 2
        begin_pos = DocumentPos(highlight_page - 1, begin[0] - offset_x, begin[1])
        end_pos = DocumentPos(highlight_page - 1, end[0] - offset_x, end[1])
        return (doc.to_absolute(begin_pos), doc.to_absolute(end_pos))

    def _convert_zot_date_to_sioyek(self, date_str):
        """

        Convert a date from zotero default format to sioyek format.

        Parameters
        ----------
        date_str : str
            Date string in zotero default format, '%Y-%m-%dT%H:%M:%SZ'

        Returns
        -------
        formatted_date_str : str
            Date string in sioyek default format, '%Y-%m-%d %H:%M:%S'

        Examples
        --------
        >>> time_test = _convert_zot_date_to_sioyek(
        ...     "2024-08-13T15:53:45Z"
        ... )
        >>> print(time_test)
        2024-08-13 15:53:45

        """
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        formatted_date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date_str

    def _calculate_md5(self, file_path):
        """

        Calculate a file md5sum hash.

        Parameters
        ----------
        file_path : str
            Complete file path

        Returns
        -------
        hash : str
            md5sum hash string of the file

        """
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def get_zotero_to_sioyek_highlights(self, file_path, zotero_highlights):
        """

        Get a zotero file highlights, formatted in a dict with essential data to embed to sioyek.

        Parameters
        ----------
        file_path : str
            Complete file path

        zotero_highlights : __main__.ZoteroHighlights
            Main zotero highlights class

        Returns
        -------
        zotero_annotations : list
            list containing highlight dicts, being one dict per highlight

        Examples
        --------
        zotero_annotations example list of dict:
        [{'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
          'desc': 'thermodynamic databases.,
          'type': 'i', 'begin_x': '-198.7873992919922',
          'begin_y': '1121.375', 'end_x': '-156.77529907226562', 'end_y': '1155.4794921875',
          'text_annot': 'None', 'creation_time': '2024-08-13 15:53:45',
          'modification_time': '2024-08-13 15:53:45',
          'uuid': 'cc3366af-b523-4a67-a802-c7afd846d942',
         },
         {'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
          'desc': 'reported by many authors and used in practice for several decades,',
          'type': 'd', 'begin_x': '-165.0081024169922', 'begin_y': '997.185546875',
          'end_x': '-152.75357055664062', 'end_y': '1031.2900390625',
          'text_annot': 'None', 'creation_time': '2024-08-13 15:53:42',
          'modification_time': '2024-08-13 15:53:42',
          'uuid': '58d238b6-1b42-4b52-97aa-4773b9b6c734',
          }]
        """
        filename = f"{path.basename(file_path)}"
        zotero_highlights.get_highlights_by_filename(filename)
        highlights = zotero_highlights.highlights
        zotero_annotations = []
        for highlight in highlights:
            abs_pos = self._to_abs(highlight, file_path)
            zotero_annotations.append(
                {
                    "document_path": self._calculate_md5(file_path),
                    "desc": highlight.text,
                    "type": self.zotero_hl_to_sioyek[highlight.color],
                    "begin_x": str(abs_pos[0].offset_x),
                    "begin_y": str(abs_pos[0].offset_y),
                    "end_x": str(abs_pos[1].offset_x),
                    "end_y": str(abs_pos[1].offset_y),
                    "text_annot": "None",
                    "creation_time": self._convert_zot_date_to_sioyek(highlight.date_added),
                    "modification_time": self._convert_zot_date_to_sioyek(highlight.date_modified),
                    "uuid": str(uuid.uuid4()),
                }
            )
        return zotero_annotations

    def insert_highlight(self, file_path, zotero_highlights):
        """

        Insert a zotero file annotations to this sioyek file database.

        Inser a zotero file highlights into a sioyek file, through sqlite3.
        The colors association is based on the color dict of the start of this file, and the
        function checks for repeated annotations through both databases, to not insert repeated
        highlights. Repeated highlights is checked through the highligh similarity, if above
        90%.
        When a highlight is inserted in the sioyek file, it also prints the execed sqlite3 command.

        Parameters
        ----------
        file_path : str
            Complete file path present in zotero and sioyek database

        zotero_highlights : __main__.ZoteroHighlights
            ZoteroHighlights class

        Returns
        -------
        None

        Notes
        -----
        The only field not present in the inserted highlight is the highlight id number, this way
        it permits to add highlights to files that already contain sioyek highlights, and the id
        number is automatically generated by sioyek.

        """
        db = sqlite3.connect(clean_path(self.shared_database_file_path))
        tables = self.get_zotero_to_sioyek_highlights(file_path, zotero_highlights)
        from_annotations = self._get_attributes(file_path)

        # Create a list of tables to keep
        tables_to_keep = [
            table
            for table in tables
            if not any(
                SequenceMatcher(None, table["desc"], annotation["desc"]).ratio() >= 0.9
                for annotation in from_annotations["highlights"]
            )
        ]

        for table in tables_to_keep:
            q_hi_insert = """
            INSERT INTO highlights (document_path,desc,type,begin_x,begin_y,
                                    end_x,end_y,text_annot,creation_time,modification_time,uuid)
            VALUES ('{}','{}','{}',{},{},{},{},'{}','{}','{}','{}');
            """.format(
                table["document_path"],
                table["desc"],
                table["type"],
                table["begin_x"],
                table["begin_y"],
                table["end_x"],
                table["end_y"],
                table["text_annot"],
                table["creation_time"],
                table["modification_time"],
                table["uuid"],
            )
            print(q_hi_insert)
            db.execute(q_hi_insert)
            db.execute("commit")

        db.close()
        self.sioyek.close()


def check_filename_in_lib(path_or_filename: str) -> str:
    """

    Use in argparse type to check a file name or path, and return the complete path.

    Parameters
    ----------
    path_or_filename : str
        file name or file complete path

    Returns
    -------
    path : str
        file complete path

    """
    directory = ZOTERO_LOCAL_DIR
    try:
        exists = path.exists(path_or_filename)
        if exists:
            return path_or_filename
        else:
            for root, _, files in walk(directory):
                if path_or_filename in files:
                    return path.join(root, path_or_filename)
            raise (ValueError)
    except ValueError:
        print("\033[31;1mMust be a file name or file path!\033[0m")
        return None


def hex_to_rgb(hex_color):
    """

    Convert a html hex to rgb.

    Parameters
    ----------
    hex_color : str
        Html hex color code

    Returns
    -------
    rgb : tuple
        r,g,b tuple, rangin each color from 0 to 255

    Examples
    --------
    >>> rgb = hex_to_rgb("#ff6666")
    >>> print(rgb)
    (255, 102, 102)

    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def print_colored_string(string, hex_color):
    """

    Print to terminal a string colored with a html hex code color.

    Parameters
    ----------
    string : str
        string to be printted

    hex_color : str
        html hex code color

    Returns
    -------
    None

    """
    rgb = hex_to_rgb(hex_color)
    ansi_escape = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    reset_escape = "\033[0m"
    print(f"{ansi_escape}{string}{reset_escape}")


def main():
    library_id = ZOTERO_LIBRARY_ID
    library_type = ZOTERO_LIBRARY_TYPE
    api_key = ZOTERO_API_KEY
    zotero_highlights = ZoteroHighlights(library_id, library_type, api_key)
    sioyek_highlights = SioyekHighlights()
    parser = argparse.ArgumentParser(
        prog="zot2sioyek.py",
        description="Zotero highlights to sioyek manager.",
        epilog="Author: eduardotcampos@usp.br",
        allow_abbrev=True,
        add_help=True,
    )
    parser.add_argument(
        "--get-highlights",
        "-g",
        type=check_filename_in_lib,
        help="Print all highlights from a given zotero file",
        metavar=("[file_name_or_path]",),
    )
    parser.add_argument(
        "--list-attributes",
        "-L",
        type=check_filename_in_lib,
        help="List all available attributes from a zotero file",
        metavar=("[file_name_or_path]",),
    )
    parser.add_argument(
        "--print-annotation-text",
        "-p",
        type=check_filename_in_lib,
        help="Print all highlilighted text for a given zotero file",
        metavar=("[file_name_or_path]",),
    )
    parser.add_argument(
        "--list-sioyek-files",
        "-f",
        action="store_true",
        help="Print all files in sioyek local database",
    )
    parser.add_argument(
        "--list-sioyek-hash",
        "-H",
        type=check_filename_in_lib,
        help="Print a sioyek database file hash",
        metavar=("[file_name_or_path]",),
    )
    parser.add_argument(
        "--list-sioyek-attributes",
        "-l",
        type=check_filename_in_lib,
        help="Print all attributes  and values present in a sioyek file.",
        metavar=("[file_name_or_path]",),
    )
    parser.add_argument(
        "--insert-highlight",
        "-i",
        type=check_filename_in_lib,
        help="Print all files in sioyek local database",
        metavar=("file_name_or_path",),
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.get_highlights:
        filename = path.basename(args.get_highlights)
        zotero_highlights.get_highlights_by_filename(filename)
        highlights = zotero_highlights.highlights
        n = 1
        print("\n")
        for highlight in highlights:
            print(
                textwrap.dedent(f"""\
                {n}
                -----
                Text: {highlight.text}
                Color: {highlight.color}
                Page: {highlight.page}
                Creation Date: {highlight.date_added}
                Modification Date: {highlight.date_modified}
                """)
            )
            n += 1

    if args.list_attributes:
        filename = path.basename(args.list_attributes)
        attributes = zotero_highlights.list_annotation_attributes_by_filename(filename)
        print(attributes)

    if args.print_annotation_text is not None:
        filename = path.basename(args.print_annotation_text)
        attributes_list = zotero_highlights.assign_annotation_attributes(filename)
        for attrs in attributes_list:
            print_colored_string(attrs.get("annotationText"), attrs.get("annotationColor"))

    if args.list_sioyek_files:
        sioyek_highlights.list_files()

    if args.list_sioyek_hash is not None:
        sioyek_highlights.list_hash(args.list_sioyek_hash)

    if args.list_sioyek_attributes is not None:
        sioyek_highlights.list_attributes(args.list_sioyek_attributes)

    if args.insert_highlight is not None:
        file_path = args.insert_highlight
        sioyek_highlights.insert_highlight(file_path, zotero_highlights)


if __name__ == "__main__":
    main()
