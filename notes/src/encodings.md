# Character Encodings

Check out the [source code](../src/encodings.py)

- [US-ASCII](https://en.wikipedia.org/wiki/ASCII)
  - American Standard Code for Information Interchange
  - 7 bit representations of 128 chars
    - [control codes](https://en.wikipedia.org/wiki/C0_and_C1_control_codes#C0)
      - decimal: 0-31, 127
      - hex: 00-1F, 7F
    - printable chars
      - decimal: 32-126
      - hex: 20-7E
      - starts with "space" char
      ```
       !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
      ```

- [UTF-8](https://en.wikipedia.org/wiki/UTF-8)
  - Unicode (Universal) Transformation Format
  - variable-width, 1-4 bytes
  - backwards compatible with ASCII
  - first 128 characters of UTF-8 are a one byte representation of ASCII

- [Base64](https://en.wikipedia.org/wiki/Base64)
  - binary-to-text encoding scheme

**UTF-8** is the dominant encoding for the World Wide Web (and internet technologies), accounting for 98% of all web pages, and up to 100.0% for some languages, as of 2022

| First code point | Last code point | Byte 1 | Byte 2 | Byte 3 | Byte 4 |
|:-:|:-:|:-:|:-:|:-:|:-:|
| U+0000 | U+007F | 0xxxxxxx | - | - | - |
| U+0080 | U+07FF | 110xxxxx | 10xxxxxx | - | - |
| U+0800 | U+FFFF | 1110xxxx | 10xxxxxx | 10xxxxxx | - |
| U+10000 | U+10FFFF | 11110xxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |
