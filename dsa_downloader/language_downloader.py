import click
import requests
import json
import os
from dsa_downloader import meta


class LanguageDownloader:
    def __init__(self, debug, bootstrap_file, output_path):
        self.debug = debug
        self.meta = meta.Meta(bootstrap_file)
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def download_lang(self, lang):
        loc_res = requests.get(f'{self.meta.loc_cdn_base_url}/localization/{self.meta.loc_version}/Loc_{lang}.txt')
        loc_res.encoding = 'utf-8'

        with open(f'{self.output_path}/Loc_{lang}.txt', 'w', encoding='utf8') as fout:
            fout.write(loc_res.text)
            fout.flush()
            fout.close()
            click.echo(f"{lang} localization file is written to {self.output_path}/Loc_{lang}.txt.")

        with open(f'{self.output_path}/Loc_{lang}.json', 'w', encoding='utf8') as fout:
            rst = dict()
            for line in loc_res.text.splitlines():
                words = line.rstrip('\n').split("|", 1)
                if len(words) > 1:
                    rst[words[0]] = words[1]
                else:
                    rst[words[0]] = ''
            json_dumps_str = json.dumps(rst, sort_keys=True, ensure_ascii=False, indent=2)
            print(json_dumps_str, file=fout)
            click.echo(f"{lang} localization file is written to {self.output_path}/Loc_{lang}.json.")
