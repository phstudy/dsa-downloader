# DSA Downloader

DSA Downloader is a Disney Sorcerer's Arena resources downloader, 
which allow developers to download localization files and assets.

## How to use
Installing the library using pip:

```
$ pip install dsa-downloader
```

Extracting bootstrap config from apk

```
$ dsa-downloader extract-config com.glu.disneygame.apk
```

Downloading localization files

```
$ dsa-downloader download-langs --langs ChineseTraditional --langs English
```

Downloading assets

```
$ dsa-downloader download-assets
```

