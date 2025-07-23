import re
import json
import shutil

def reformat():
    # Load configuration
    with open("setting.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    keyword_set = set()
    for lang in settings:
        words = lang.get("separator_words")
        if words:
            keyword_set.update(words)
    keywordList = list(keyword_set)

    for lang in settings:
        input_data_file = lang.get("input_data_file")
        if input_data_file:
            raise Exception(f"input_data_file is not allowed for {lang['name']}")

        # Read the input file
        with open(input_data_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Backup for safety
        backup_path = input_data_file + "reformat" + ".bak"
        shutil.copy(input_data_file, backup_path)

        new_content = replace_with_br(lang.get("separator"), content)

        # Process each keyword
        for kw in keywordList:
            # Define pattern with word boundaries
            pattern = rf'\b({re.escape(kw)})'

            def insert_br(match):
                start = match.start()
                # Insert <br> if not already present before the keyword
                if new_content[max(0, start - 4):start].lower() != '<br>':
                    return '<br>' + match.group(1)
                else:
                    return match.group(1)

            new_content = re.sub(pattern, insert_br, new_content)

        # Write the reformatted result
        with open(input_data_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

def replace_with_br(separator, content):
    segments = content.splitlines()
    result = []
    i = 0
    while i < len(segments):
        if not segments[i].split():
            continue
        if "<start>" in segments[i]:
            result.append(segments[i])
            continue
        if separator not in segments[i]:
            # Merge lines that don't have the separator
            while i + 1 < len(segments) and separator not in segments[i + 1]:
                segments[i] += "<br>" + segments[i + 1]
                i += 1
            while i + 1 < len(segments) and separator in segments[i + 1]:
                segments[i] += "<br>" + segments[i + 1]
                i += 1
        if separator in segments[i]:
            # Merge following lines that also contain the separator
            while i + 1 < len(segments) and separator in segments[i + 1]:
                segments[i] += "<br>" + segments[i + 1]
                i += 1
        result.append(segments[i])
        i += 1
    return ('\n').join(result)

