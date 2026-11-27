import json


def read_note_records(source, *, max_line_chars=200, trace=False):
    if type(max_line_chars) is not int or max_line_chars < 1:
        raise ValueError("max_line_chars must be a positive integer")
    record_number = 0
    while True:
        line = source.readline(max_line_chars + 1)
        if line == "":
            return
        if len(line) > max_line_chars:
            raise ValueError("record line exceeds the character limit")
        record_number = record_number + 1
        if trace:
            print("Read record", record_number)
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError("each record must be a JSON object")
        yield record
