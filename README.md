# HuabanDownloader
Python downloader script for Huaban ([huaban.com](huaban.com)) boards.

A simple script for downloading every pin from a huaban board.

* Images are saved into a `huaban\<board_title>` folder.
* Script will skip images that were already downloaded on subsequent runs (makes it easy to rerun the script, if one or more pins fail). To redownload an existing image, just remove it from the target folder (`huaban\<board_title>`) before running script again
* If certain images fail to download (timeout) their list can be found in the `huaban\<board_title>\failReport.txt` file.


## USAGE
`python3 HuabanDownloader.py <board_url>`

### Example 
`python3 HuabanDownloader.py https://huaban.com/boards/43414935/`

### Disclaimer
Based partially on [https://gist.github.com/magicdawn/1242ce87e713c9a3898a](https://gist.github.com/magicdawn/1242ce87e713c9a3898a)
, but 90% of the script was rewritten since huaban api has changed since the creation of that script apparently.
