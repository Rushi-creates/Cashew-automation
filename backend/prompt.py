prompt_template = '''
Extract the following transaction details from the text below:
- Amount
- Note (if present)
- Sender
- Sent or received (based on sender name; your name is Rushi Nitin Patil)
- Date and time

Please list the values clearly as labeled fields.

Transaction Text:
\"\"\"{ocr_text}\"\"\"

Transaction Details:
'''
