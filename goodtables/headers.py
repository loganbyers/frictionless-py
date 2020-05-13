from cached_property import cached_property
from . import helpers
from . import errors


class Headers(list):
    def __init__(self, cells, *, fields, field_positions):
        assert len(fields) == len(field_positions)

        # Set params
        self.__field_positions = field_positions
        self.__errors = []

        # Extra headers
        if len(fields) < len(cells):
            iterator = cells[len(fields) :]
            start = max(field_positions) + 1
            del cells[len(fields) :]
            for field_position, cell in enumerate(iterator, start=start):
                self.__errors.append(
                    errors.ExtraHeaderError(
                        cell=cell, cells=cells, fieldPosition=field_position,
                    )
                )

        # Missing headers
        if len(fields) > len(cells):
            start = len(cells) + 1
            iterator = zip(field_positions[len(cells) :], fields[len(cells) :])
            for field_number, (field_position, field) in enumerate(iterator, start=start):
                self.__errors.append(
                    errors.MissingHeaderError(
                        cells=map(str, cells),
                        fieldName=field.name,
                        fieldNumber=field_number,
                        fieldPosition=field_position,
                    )
                )

        # Iterate items
        field_number = 0
        for field_position, field, cell in zip(field_positions, fields, cells):
            field_number += 1

            # Blank Header
            if not cell:
                self.__errors.append(
                    errors.BlankHeaderError(
                        cells=map(str, cells),
                        fieldName=field.name,
                        fieldNumber=field_number,
                        fieldPosition=field_position,
                    )
                )

            # Duplicated Header
            if cell:
                duplicate_field_positions = []
                seen_cells = cells[0 : field_number - 1]
                seen_field_positions = field_positions[0 : field_number - 1]
                for seen_position, seen_cell in zip(seen_field_positions, seen_cells):
                    if cell == seen_cell:
                        duplicate_field_positions.append(seen_position)
                if duplicate_field_positions:
                    self.__errors.append(
                        errors.DuplicateHeaderError(
                            cell=str(cell),
                            cells=map(str, cells),
                            fieldName=field.name,
                            fieldNumber=field_number,
                            fieldPosition=field_position,
                            details=', '.join(map(str, duplicate_field_positions)),
                        )
                    )

            # Non-matching Header
            if cell:
                if field.name != cell:
                    self.__errors.append(
                        errors.NonMatchingHeaderError(
                            cell=str(cell),
                            cells=map(str, cells),
                            fieldName=field.name,
                            fieldNumber=field_number,
                            fieldPosition=field_position,
                        )
                    )

        # Save headers
        super().__init__(cells)

    @cached_property
    def field_positions(self):
        return self.__field_positions

    @cached_property
    def errors(self):
        return self.__errors
