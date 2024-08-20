# Zotero to Sioyek Highlights Manager

---

**Python script to embed zotero highlights to [sioyek](https://github.com/ahrm/sioyek), and other utils.**

- 🐍 Python [sqlite3](https://docs.python.org/3/library/sqlite3.html) and [pyzotero](https://github.com/urschrei/pyzotero) Based Script

[![updatebadge]][update] [![pypibadge]][pypi] [![mitbadge]][license]

[![emailbadge]][email]

[update]: https://github.com/eduardotlc/zot2sioyek/commits/master/
[license]: https://opensource.org/licenses/mit
[pypi]: https://pypi.org/project/zot2sioyek/
[pypibadge]: https://img.shields.io/pypi/v/zot2sioyek.svg?logo=python&logoColor=yellow&color=7e7edd&style=for-the-badge
[email]: mailto:eduardotcampos@usp.br
[emailbadge]: https://img.shields.io/badge/Email-7e7edd?style=for-the-badge&logo=gmail
[mitbadge]: https://img.shields.io/badge/License-MIT-9aefea?style=for-the-badge&logo=gitbook
[updatebadge]: https://img.shields.io/badge/Updated-August_2024-93ddfb?style=for-the-badge&logo=googlecalendar

## 📖 Contents

- ✨ [Features](#-features)
- 📚 [Requirements](#-requirements)
  - 🐍 [Conda](#-conda)
- 📦 [Installation](#-installation)
- 🔧 [Configuration](#-configuration)
  - 🎨 [Colors](#-colors)
- 📝 [TODO](#-todo)
- 🤝 [Contributing](#-contributing)
- 💓 [Aknowledgements](#-aknowledgements)

## ✨ Features

- Embed zotero highlights to the sioyek database:

```bash
python zot2sioyek.py --insert-highlights "/path/to/file.pdf"
```

- Print in terminal the text of all the highlights from a zotero file, colored with the highlight
  color

```bash
python zot2sioyek.py --print-annotation-text "/path/to/file.pdf"
```

- To see all available commands:

```bash
python zot2sioyek.py --help
```
> [!NOTE]
> If installed through pip, you can run only zot2sioyek instead of python zot2sioyek.py

## 📚 Requirements

Requirements are automatic installed when this script is installed with pip

- pyzotero

- pymupdf

- PyQt5

- regex

- sqlite3

```bash
python -m pip install pyzotero pymupdf PyQt5 regex sqlite3
```

### 🐍 Conda

If wanted, requirements may be installed with conda, to run this script in a conda environment.

Inside this repo, run:

```bash
conda env create --file env.yml
```

## 📦 Installation

```bash
python -m pip install zot2sioyek
```

## 🔧 Configuration

To use this script define the variables in zot2sioyek.py:

- `SIOYEK_PATH`: Sioyek binary path.

- `LOCAL_DATABASE_FILE_PATH`: Sioyek .db local database file path.

- `SHARED_DATABASE_FILE_PATH`: Sioyek .db shared database file path.

- `ZOTERO_LIBRARY_ID`: Your personal library ID available [Here](https://www.zotero.org/settings/keys),
  in the section Your userID for use in API calls.

- `ZOTERO_API_KEY`: Api key, you can obtain [Here](https://www.zotero.org/settings/keys/new).

- `ZOTERO_LIBRARY_TYPE`: Zotero library type, can be `'user'` or `'group'`.

- `ZOTERO_LOCAL_DIR`: Zotero local storage folder, like `/home/user/Zotero/storage`.

- `ZOTERO_TO_SIOYEK_COLORS`: Sioyek highlight type letter associated to each zotero highlight color
  (Optional).

### 🎨 Colors

- This script defines `ZOTERO_TO_SIOYEK_COLORS` variable based on the most close colors of default
  sioyek config, to the zotero highlight colors. The conversion looks like the following (Zotero
  colors in the upper row, sioyek colors in the lower row):

![comparison colors](/images/coparison_colors.png)

- If you want to have the exact same colors of zotero highlights in sioyek, add the following to
  your sioyek `prefs_user.config`:

```
highlight_color_g 0.37 0.70 0.21
highlight_color_a 0.63 0.54 0.90
highlight_color_p 0.90 0.43 0.93
highlight_color_b 0.18 0.66 0.90
highlight_color_r 1.00 0.40 0.40
highlight_color_o 0.95 0.60 0.22
highlight_color_y 1.00 0.83 0.00
```

- Or to any highlight letter you want, since the defined letter on `prefs_user.config` and the script
  variable `ZOTERO_TO_SIOYEK_COLORS` match.

## 📝 TODO

- Embed all zotero database highlights starting from a specified date.

- Create import from sioyek database to zotero database highlights.

  - Currently, I couldn't find a way of adding zotero highlights through pyzotero, or through
    zotero api/sql. If anyone knows how to do it, please message or email me so that I can update
    this script, or feel free to implement the needed updates and send a pull request, I'll be
    very thankful.

## 🤝 Contributing

Feel free to make [pending](#-todo) or other optimizations and pull requests, this script is
still under development and any contribution is very much appreciated.

- Clone the repo to your local environment:

## 💓 Aknowledgements

- [Ahrm](https://github.com/ahrm) for developing [Sioyek](https://github.com/ahrm/sioyek) PDF reader.

- [Urschrei](https://github.com/urschrei) for [Pyzotero](https://github.com/urschrei/pyzotero)

- [Blob42](https://github.com/blob42) for [Koreader-sioyek-import](https://github.com/blob42/koreader-sioyek-import),
  which parts of this script was based from.

- The [Zotero](https://www.zotero.org/) team.
