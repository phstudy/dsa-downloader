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
  download-assets   Download assets.
  download-langs    Download localization files.
  download-gamedata Download gamedata.
  extract-config    Extract bootstrap config from APK file.
```

Install the library using pip

```
$ python -m pip install dsa-downloader
```

Extract bootstrap config from *[Disney Sorcerer's Arena APK](https://apkcombo.com/apk-downloader/#package=com.glu.disneygame)* file

```
$ dsa-downloader extract-config com.glu.disneygame.apk
bootstrap_config file is written to out/bootstrap_config.json.
```

Download gamedata

```
$ dsa-downloader download-gamedata
gamedata-static.bin is written to out/gamedata/9c49b3b7-1479-4c28-8894-d1da716e36ce_gamedata.bin

# Convert gamedata binary to json
$ curl -O https://github.com/phstudy/dsa_proto_dumper/blob/main/gamedata/gamedata.fbs
$ flatc --json --defaults-json --strict-json --raw-binary gamedata.fbs -- out/gamedata/9c49b3b7-1479-4c28-8894-d1da716e36ce_gamedata.bin
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
