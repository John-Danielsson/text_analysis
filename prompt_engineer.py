"""This file contains the string templates used for formatting
text data in a way that makes it more easily readable to the
ChatGPT API."""

primer_str = """
All of the text after the 10 consecutive asterisks consists of text
extracted from {} files in .pdf, .txt, .html, .docx, or .epub format.
The text of each file is formatted as follows:

==========
BEGIN FILE (file number)
File Name: (file name)
File Content:
(text of file)
END FILE (file number)
==========

**********

"""

prompt_engineer_str = """

==========
BEGIN FILE {}
File Name: {}
File Content:
{}
END FILE {}
==========

"""
