"""
Lab Work #4 - Task 2: Entry Point
"""

import zipfile
import os
from .analyzer import AdvancedTextAnalyzer

SAMPLE_TEXT = (
    "Sample text v1 about various values. Error 404. "
    "IP address: 192.168.1.1. Smile :-) and ;--[[ Happy! "
    "Some strange s-word and server42 here. Visit www site2."
)


def run_task_2():

    print("\n--- TASK 2: Text Analysis & Regex (Variant 29) ---")

    input_file   = "task2/textfile.txt"
    output_file  = "result_task2.txt"
    archive_file = "archive_task2.zip"

    os.makedirs("task2", exist_ok=True)
    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_TEXT)
        print(f"Created sample input file: {input_file}")

    analyzer = AdvancedTextAnalyzer(input_file)

    test_ip = input("Enter an IP address to validate: ").strip()

    v_word, v_idx         = analyzer.find_first_v_word()
    smile_count, smiles   = analyzer.count_smiles()
    by_type               = analyzer.find_sentences_by_type()

    report_lines = [
        "=== TASK 2 RESULTS (Variant 29) ===",
        "",
        "--- General analysis ---",
        f"Total sentences:              {analyzer.find_sentences()}",
        f"  Declarative   (ends with .): {by_type['declarative']}",
        f"  Interrogative (ends with ?): {by_type['interrogative']}",
        f"  Exclamatory   (ends with !): {by_type['exclamatory']}",
        f"Avg sentence length (letters): {analyzer.avg_sentence_length():.2f} chars",
        f"Average word length:           {analyzer.avg_word_length():.2f} chars",
        f"Smiley count:                  {smile_count}  =>  {smiles}",
        "",
        "--- Variant 29 ---",
        f"Mixed (lowercase+digit) words: {analyzer.find_words_mixed()}",
        f"IP '{test_ip}':               {'VALID' if analyzer.is_valid_ip(test_ip) else 'INVALID'}",
        f"Lowercase letter count:        {analyzer.count_lowercase()}",
        f"First word with 'v':           '{v_word}' at position {v_idx}",
        f"Text without 's' words:        {analyzer.exclude_s_words()}",
    ]

    final_text = "\n".join(report_lines)
    print("\n" + final_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)

    with zipfile.ZipFile(archive_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(output_file)
        info = zf.getinfo(output_file)
        print(f"\nArchive: {archive_file}")
        print(f"  File inside: {info.filename}, size: {info.file_size} bytes, "
              f"compressed: {info.compress_size} bytes")

    print(f"\nResults saved to '{output_file}' and archived in '{archive_file}'")
