# DSA Downloader

DSA Downloader is a Disney Sorcerer's Arena resources downloader, 
which allow developers to download localization files and assets.

## How to use

Show supported commands

```
$ dsa-downloader --help
Usage: dsa-downloader [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  download-assets  Download assets.
  download-langs   Download localization files.
  extract-config   Extract bootstrap config from APK file.
```

Install the library using pip

```
$ pip install dsa-downloader -U
```

Extract bootstrap config from *APK* file

```
$ dsa-downloader extract-config com.glu.disneygame.apk
bootstrap_config file is written to out/bootstrap_config.json.
```

Download localization files

```
$ dsa-downloader download-langs --langs ChineseTraditional --langs English
ChineseTraditional localization file is written to out/langs/Loc_ChineseTraditional.txt.
ChineseTraditional localization file is written to out/langs/Loc_ChineseTraditional.json.
English localization file is written to out/langs/Loc_English.txt.
English localization file is written to out/langs/Loc_English.json.
```

Download assets

```
$ dsa-downloader download-assets
  2%|██▋                                         | 81/3896 [00:03<03:00, 21.08it/s]
```

## Docker

Use docker container to extract bootstrap config from *APK* file 

```
$ docker run --rm -v "$PWD":/dsa study/dsa-downloader dsa-downloader \
        extract-config com.glu.disneygame.apk
bootstrap_config file is written to out/bootstrap_config.json.
```