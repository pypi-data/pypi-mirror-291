#!/usr/bin/env python3.12

from src.util import is_valid_index, is_valid_version_number, is_plain_object
from datetime import datetime, UTC
import json
import re

class Document:
    """
    A JTF Document.
    """
    def __init__(self, data):
        """
        Initialize the Document with data.
        :param data: The document's data.
        """
        JTF.validate(data)  # Validate the data before object creation.
        self.source = data
        self.__clean_metadata()
        self.__clean_dates()

    def update_updated_at(self):
        """
        Update the `updatedAt` value of the document.
        """
        if 'updatedAt' not in self.source:
            self.source['updatedAt'] = datetime.now(UTC).isoformat()

    def __clean_dates(self):
        """
        Clean up the document's `createdAt`/`updatedAt` dates.
        """
        if 'createdAt' not in self.source:
            self.source['createdAt'] =datetime.now(UTC).isoformat()
        self.update_updated_at()

    def __clean_metadata(self):
        """
        Clean up the document's metadata.
        """
        if 'metadata' not in self.source:
            self.source['metadata'] = {}
        if 'jtf' not in self.source['metadata']:
            self.source['metadata']['jtf'] = JTF.supported_versions[0]
    
    @property
    def tables(self):
        return {index: Table(self, index) for index in self.source['data'].keys()}

    def stringify(self):
        """
        :returns: The data object represented by a JSON string.
        """
        return json.dumps(self.source['data'])

    def to_list(self):
        """
        Get lists of each table in the document.
        """
        return {index: table.to_list() for index, table in self.tables.items()}

    def to_csv(self):
        """
        Get CSV strings of each table in the document.
        """
        return {index: table.to_csv() for index, table in self.tables.items()}

    def get_cell(self, table, x, y):
        """
        Get the content of a cell.
        :param table: The index of the table to convert.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :returns: The content of the cell or `None` if the cell does not exist.
        """
        if not is_valid_index(table):
            raise ValueError(f'Provided "table" value "{table}" is not a valid integer string.')
        
        if table not in self.tables:
            raise ValueError(f'No table in document at index "{table}"')

        return self.tables[table].get_cell(x, y)

    def set_cell(self, table, x, y, value):
        """
        Set the content of a cell.
        :param table: The index of the table to convert.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :param value: The value to set.
        """
        if not is_valid_index(table):
            raise ValueError(f'Provided "table" value "{table}" is not a valid integer string.')
        
        if table not in self.tables:
            raise ValueError(f'No table in document at index "{table}"')

        self.tables[table].set_cell(x, y, value)
        self.update_updated_at()

    def set_table(self, index, data):
        """
        Set a table to a value. **Will overwrite existing tables.**
        :param index: The index of the table to set.
        :param data: The table data to set.
        """
        if not is_valid_index(index):
            raise ValueError(f'Provided "index" value "{index}" is not a valid integer string.')

        JTF.validate_table(data)
        self.source['data'][index] = data

    def get_extra_processor_data(self, processor):
        """
        Get a processor's data from the document's `metadata.extra` object.
        :param processor: The processor's unique ID.
        :returns: Returns a data object if found, or `None` if no object was found.
        """
        return self.source['metadata'].get('extra', {}).get(processor)

    def set_extra_processor_data(self, processor, data, extend=False):
        """
        Set extra data in the document's `metadata.extra` object for use in processor feature extension.
        :param processor: The processor's unique identifier.
        :param data: An object of extra data to set.
        :param extend: If `True`, destructures the new data object into existing data instead of overwriting it.
        """
        existing_data = self.get_extra_processor_data(processor)

        if extend and existing_data:
            data = {**existing_data, **data}  # Destructure into existing data.
            self.source['metadata']['extra'] = {}

        self.source['metadata']['extra'][processor] = data

    def get_cell_styles(self, table, x, y):
        """
        Get the styles that must be applied to a cell.
        :param table: The index of the table to convert.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :returns: An object containing the classes and styles to apply to this cell.
        """
        if not is_valid_index(table):
            raise ValueError(f'Provided "table" value "{table}" is not a valid integer string.')

        if table not in self.tables:
            raise ValueError(f'No table in document at index "{table}"')

        return self.tables[table].get_cell_styles(x, y)

class Table:
    """
    A JTF Table.
    """
    def __init__(self, document: Document, index):
        """
        :param document: This table's parent document
        :param index: The table's index in the document.
        """
        if not is_valid_index(index):
            raise ValueError(f'Provided index value "{index}" is not a valid integer string.')

        self.document = document
        self.index = index

    @property
    def source(self):
        """
        Get the source data for this table.
        """
        return self.document.source['data'][self.index]

    @source.setter
    def source(self, value):
        """
        Set the source data for this table.
        """
        self.document.source['data'][self.index] = value

    @property
    def label(self):
        """
        Get the table's label.
        """
        return self.source.get('label')

    @label.setter
    def label(self, value):
        """
        Set the table's label.
        """
        if not value or not isinstance(value, str):
            raise SyntaxError('Each table in the document must have a "label" string value.')
        self.source['label'] = value

    def to_list(self):
        """
        Convert a table into a 2D list.
        :returns: The table as a 2D list.
        """
        data = self.source['data']
        result = []

        for y, row in data.items():
            y = int(y)
            while (len(result) <= y): 
                result.append([])            

            for x, cell in row.items():
                x = int(x)
                while (len(result[y]) <= x): 
                    result[y].append(None) 

                result[y][x] = cell

        return result

    def to_csv(self):
        """
        :returns: The data object in CSV format.
        """
        table = self.to_list()

        # Determine the widest the CSV should be.
        widest_row = max(len(row) for row in table)

        csv = "" 
        for row in table:
            if not row:
                csv += "," * widest_row + "\n"
            else:
                csv += ",".join(str(cell) if cell is not None else "" for cell in row) + "\n" 
        
        return csv.strip()

    def get_cell(self, x, y):
        """
        Get the content of a cell.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :returns: The content of the cell or `None` if the cell does not exist.
        """
        if not is_valid_index(x):
            raise ValueError(f'Provided x-coordinate value "{x}" is not a valid integer string.')

        if not is_valid_index(y):
            raise ValueError(f'Provided y-coordinate value "{y}" is not a valid integer string.')

        x = str(x)
        y = str(y)

        data = self.source['data']
        return data.get(y, {}).get(x)

    def set_cell(self, x, y, value):
        """
        Set the content of a cell.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :param value: The value to set.
        """
        JTF.validate_cell(value)

        if not is_valid_index(x):
            raise ValueError(f'Provided x-coordinate value "{x}" is not a valid integer string.')

        if not is_valid_index(y):
            raise ValueError(f'Provided y-coordinate value "{y}" is not a valid integer string.')

        x = str(x)
        y = str(y)

        data = self.source['data']
        if y not in data:
            data[y] = {}

        data[y][x] = value

        self.document.update_updated_at()

    def get_cell_styles(self, x, y):
        """
        Get the styles that must be applied to a cell.
        :param x: The x-coordinate of the cell.
        :param y: The y-coordinate of the cell.
        :returns: An object containing the classes and styles to apply to this cell.
        """
        if not is_valid_index(x):
            raise ValueError(f'Provided x-coordinate value "{x}" is not a valid integer string.')

        if not is_valid_index(y):
            raise ValueError(f'Provided y-coordinate value "{y}" is not a valid integer string.')

        styles_to_check = (self.document.source.get('style', []) + self.source.get('style', []))

        styles = {
            'style': [],
            'class': []
        }

        for definition in styles_to_check:
            target, type_, data = definition['target'], definition['type'], definition['data']
            if JTF.target_list_includes_cell(target, x, y):
                if type_ == 'class':
                    styles['class'].append(data.strip())
                elif type_ == 'style':
                    styles['style'].append(data.strip())

        styles['class'] = " ".join(styles['class'])
        styles['style'] = "; ".join(style if style.endswith(";") else f"{style};" for style in styles['style'])

        return styles

class JTF:
    supported_versions = ["v1.1.9"]

    @staticmethod
    def __validate_keys(keys):
        """
        Validate the key indices of an object.

        Args:
            keys (list[str]): The list of keys returned by `list(obj.keys())`.

        Raises:
            SyntaxError: If the provided keys object is not a list or if any key is not a valid index.
        """
        if not isinstance(keys, list):
            raise SyntaxError('Provided keys object is not of type "list".')

        for key in keys:
            if not is_valid_index(key):
                raise SyntaxError(
                    f'Each object key-index must be a string containing an integer. "{key}" is invalid.'
                )
  
    @staticmethod
    def stringify(document):
        """
        Converts a document to a string.

        Args:
            document (any): The document to stringify.

        Returns:
            str: A stringified version of the document.

        Raises:
            TypeError: If the provided object is not of type 'Document'.
        """
        if not isinstance(document, Document):
            raise TypeError('Provided object is not of type "Document".')

        return document.stringify()

    @staticmethod
    def validate_cell(cell):
        """
        Validate the contents of a table's cell.

        Args:
            cell (any): The cell to validate.

        Raises:
            SyntaxError: If the cell contains data of an invalid type.
        """
        if not isinstance(cell, (str, int, float, bool)) or cell is None:
            raise SyntaxError(
                'Cell data of invalid type provided. Must be one of: ["string", "number", "boolean", null]'
            )

    @staticmethod
    def validate_table_data(data):
        """
        Validate a table's data object.

        Args:
            data (dict): The data to validate.

        Raises:
            SyntaxError: If the keys or cells are invalid.
        """
        # Validate keys.
        JTF.__validate_keys(list(data.keys()))

        # Validate cells.
        for cell in data.values():
            JTF.validate_cell(cell)

    @staticmethod
    def validate_table(table):
        """
        Validate a table within a JTF document's data object.

        Args:
            table (dict): The table to validate.

        Raises:
            SyntaxError: If the table contains invalid keys, label, or data.
        """
        valid_keys = ["data", "label", "style"]

        for key in table.keys():
            if key not in valid_keys:
                raise SyntaxError(f'Invalid key "{key}" provided to table.')

        data = table.get("data")
        label = table.get("label")
        style = table.get("style")

        # Validate label.
        if not label or not isinstance(label, str):
            raise SyntaxError(
                'Each table in the document must have a "label" string value.'
            )

        # Validate data.
        if not is_plain_object(data):
            raise SyntaxError(
                f'Expected a plain object but received a value of type {"list" if isinstance(data, list) else type(data).__name__}.'
            )

        JTF.__validate_keys(list(data.keys()))
        for table_data in data.values():
            JTF.validate_table_data(table_data)

        # Validate styles.
        if style:
            JTF.validate_style(style)

    @staticmethod
    def __validate_data(data):
        """
        Validate a JTF document's data object.

        Args:
            data (dict): The data object to validate.

        Raises:
            SyntaxError: If the data object is invalid.
        """
        if not data:
            raise SyntaxError("No data object provided to document.")

        if not is_plain_object(data):
            raise SyntaxError(
                f'Expected a plain object but received a value of type {"list" if isinstance(data, list) else type(data).__name__}.'
            )

        # Validate the index keys of the object.
        JTF.__validate_keys(list(data.keys()))

        # Validate tables.
        tables = list(data.values())

        for table in tables:
            JTF.validate_table(table)

    @staticmethod
    def __validate_metadata(metadata):
        """
        Validate a JTF document's metadata object.

        Args:
            metadata (dict): The metadata object to validate.

        Raises:
            SyntaxError: If the metadata or its properties are invalid.
        """
        if not is_plain_object(metadata):
            raise SyntaxError(
                f'Expected a plain object but received a value of type '
                f'{"list" if isinstance(metadata, list) else type(metadata).__name__}.'
            )

        valid_keys = {"author", "title", "jtf", "extra", "css"}

        for key in metadata.keys():
            if key not in valid_keys:
                raise SyntaxError(f'Invalid key "{key}" provided to metadata.')

        author = metadata.get("author")
        title = metadata.get("title")
        jtf = metadata.get("jtf")
        css = metadata.get("css")
        extra = metadata.get("extra")

        if author and not isinstance(author, str):
            raise SyntaxError(f'Expected type "string" for metadata "author" parameter. Got: "{type(author).__name__}".')

        if title and not isinstance(title, str):
            raise SyntaxError(f'Expected type "string" for metadata "title" parameter. Got: "{type(title).__name__}".')

        if jtf:
            if not isinstance(jtf, str):
                raise SyntaxError(f'Expected type "string" for metadata "jtf" parameter. Got: "{type(jtf).__name__}".')

            if not is_valid_version_number(jtf):
                raise SyntaxError(f'"jtf" parameter not in valid format. Expected format "v0.0.0", got: "{jtf}".')

            if jtf not in JTF.supported_versions:
                raise SyntaxError(
                    f'Document indicated JTF syntax standard version "{jtf}" is not supported. '
                    f'Supported versions: {", ".join(JTF.supported_versions)}'
                )
        else:
            print(
                'A JTF syntax standard version was not provided in metadata. Document compatibility unknown. '
                'To stop this message from appearing, configure a "jtf" version number in document metadata:',
                {'jtf': JTF.supported_versions[0]}
            )

        if css:
            if isinstance(css, list):
                for path in css:
                    if not isinstance(path, str):
                        raise SyntaxError('Invalid CSS configuration provided to document metadata. CSS list should contain only strings.')
            elif not isinstance(css, str):
                raise SyntaxError('Invalid CSS configuration provided to document metadata. Should be a single string, or an list of strings containing CSS data.')

        if extra:
            if not is_plain_object(extra):
                raise SyntaxError(
                    f'Expected a plain object but received a value of type '
                    f'{"list" if isinstance(extra, list) else type(extra).__name__}.'
                )

            length = len(extra)
            print(
                f'During parsing, extra data for {length} processor{"s" if length > 1 else ""} was detected within JTF document. No action is required.'
            )

    @staticmethod
    def validate_targeting_list(targeting_list):
        """
        Validate a targeting list.

        Args:
            targeting_list (list): The targeting list to validate.

        Raises:
            SyntaxError: If the targeting list or its parameters are invalid.
        """
        if not isinstance(targeting_list, list):
            raise SyntaxError('Invalid targeting list provided. Proper format: "[x, y]".')

        if len(targeting_list) > 2:
            raise SyntaxError('Targeting list provided too many parameters. Proper format: "[x, y]".')

        if not targeting_list:
            return

        def validate_targeting_parameter(parameter):
            if parameter is None:
                return

            if isinstance(parameter, list):
                for sub_parameter in parameter:
                    validate_targeting_parameter(sub_parameter)

            if isinstance(parameter, (int, float)) and not isinstance(parameter, int):
                raise SyntaxError(f'Invalid parameter "{parameter}" provided. Number parameters in targeting lists must be integers.')

            if isinstance(parameter, str):
                parameter = parameter.strip()

                if not re.match(r'^[0-9:]+$', parameter):
                    raise SyntaxError(f'Invalid parameter "{parameter}" provided. String parameters must contain either an integer or a colon-delimited target.')

                if ':' in parameter:
                    parts = [part.strip() for part in parameter.split(':')]

                    for part in parts:
                        if part == "":
                            return

                        if not part.isdigit():
                            raise SyntaxError(f'Invalid parameter "{part}" provided. Colon-delimited parameters can only use integers.')

                if parameter.isdigit():
                    return

        for parameter in targeting_list:
            validate_targeting_parameter(parameter)

    @staticmethod
    def validate_style(style):
        """
        Validate a JTF style list.

        Args:
            style (list[dict]): The style list to validate.

        Raises:
            SyntaxError: If the style list or any style definition is invalid.
        """
        if style is None:
            raise SyntaxError("No style list provided to document.")

        if not isinstance(style, list):
            raise SyntaxError(
                f'Expected a list but received a value of type "{type(style).__name__}".'
            )

        valid_keys = {"type", "target", "data"}
        type_enum = {"class", "style"}

        for definition in style:
            if not isinstance(definition, dict):
                raise SyntaxError(
                    f'Expected a dictionary but received a value of type "{type(definition).__name__}".'
                )

            # Validate keys in the style definition
            for key in definition.keys():
                if key not in valid_keys:
                    raise SyntaxError(
                        f'Invalid key "{key}" provided to style definition.'
                    )

            type_ = definition.get("type")
            target = definition.get("target")
            data = definition.get("data")

            # Validate the style definition's type
            if not type_ or type_ not in type_enum:
                raise SyntaxError(
                    f'Invalid style definition type provided. Must be one of: {", ".join(type_enum)}'
                )

            JTF.validate_targeting_list(target)  # Validate the targeting list

            if not isinstance(data, str):
                raise SyntaxError(
                    'Style definition "data" value must be of type string.'
                )
            
    @staticmethod
    def validate(document):
        """
        Validate a JTF document.

        Args:
            document (dict): The document to validate.

        Raises:
            SyntaxError: If the document or its properties are invalid.
        """
        if document is None:
            raise SyntaxError("No data provided.")

        if not is_plain_object(document):
            raise SyntaxError(
                f'Expected a plain object but received a value of type '
                f'{"list" if isinstance(document, list) else type(document).__name__}.'
            )

        valid_keys = {"data", "metadata", "style", "createdAt", "updatedAt"}

        for key in document.keys():
            if key not in valid_keys:
                raise SyntaxError(f'Invalid key "{key}" provided to document.')

        data = document.get("data")
        metadata = document.get("metadata")
        style = document.get("style")
        created_at = document.get("createdAt")
        updated_at = document.get("updatedAt")

        # Validate data object.
        JTF.__validate_data(data)
        JTF.validate_style(style)

        if metadata:
            JTF.__validate_metadata(metadata)

        if created_at:
            if not isinstance(created_at, str):
                raise SyntaxError(f'"createdAt" parameter expected to be of type string. Got "{type(created_at).__name__}".')

            try:
                datetime.fromisoformat(created_at)
            except ValueError:
                raise SyntaxError(
                    'Invalid date string provided to "createdAt" parameter. '
                    'An ISO 8601 conforming date string is required.'
                )

        if updated_at:
            if not isinstance(updated_at, str):
                raise SyntaxError(f'"updatedAt" parameter expected to be of type string. Got "{type(updated_at).__name__}".')

            try:
                datetime.fromisoformat(updated_at)
            except ValueError:
                raise SyntaxError(
                    'Invalid date string provided to "updatedAt" parameter. '
                    'An ISO 8601 conforming date string is required.'
                )

    @staticmethod
    def parse(data: list[str, dict]) -> Document:
        """
        Parse JTF data into a readable object.

        Args:
            data (Union[str, dict]): The data to parse.

        Returns:
            Document: A Document object initialized with the parsed data.
        """
        if isinstance(data, str):
            data = json.loads(data)  # Convert the data into a Python dictionary.

        return Document(data)
    
    @staticmethod
    def target_list_includes_cell(target: list[list[int, str]], x: list[int, str], y: list[int, str]) -> bool:
        """
        Check if a target list targets a specific coordinate.

        Args:
            target (list[list[int, str]]): The target list to check.
            x (list[int, str]): The x-coordinate to check.
            y (list[int, str]): The y-coordinate to check.

        Returns:
            bool: Whether the coordinates are included in the target list.
        """
        JTF.validate_targeting_list(target)

        if not is_valid_index(x):
            raise ValueError(f'Provided x-coordinate value "{x}" is not a valid integer string.')

        if not is_valid_index(y):
            raise ValueError(f'Provided y-coordinate value "{y}" is not a valid integer string.')

        target_x, target_y = target

        def compare_index(target: any, index: int) -> bool:
            # Check if target values are None, unprovided, or equal to the requested index.
            if target is None or target == index or (isinstance(target, list) and len(target) == 0):
                return True
            elif isinstance(target, str):
                if target.isdigit() and int(target) == index:
                    return True
                if ':' in target:
                    a_part, b_part = map(str.strip, target.split(':'))
                    if not a_part:
                        a_part = '0'
                    if not b_part:
                        b_part = 'Infinity'

                    a_part = int(a_part)
                    b_part = float('inf') if b_part == 'Infinity' else int(b_part)

                    if a_part <= index < b_part:
                        return True
            elif isinstance(target, list):
                return any(compare_index(sub_target, index) for sub_target in target)

            return False

        return compare_index(target_x, int(x)) and compare_index(target_y, int(y))
