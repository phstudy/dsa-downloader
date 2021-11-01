import click
import requests
import os
from dsa_downloader import meta


class GamedataDownloader:
    def __init__(self, debug, bootstrap_file, output_path):
        self.debug = debug
        self.meta = meta.Meta(bootstrap_file)
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def download_gamedata(self):
        gamedata_res = requests.get(f'{self.meta.asset_cdn_base_url}/gamedata/{self.meta.gamedata_version}/gamedata-static.bin')

        with open(f"{self.output_path}/{self.meta.gamedata_version}_gamedata.bin", 'wb') as fout:
            fout.write(gamedata_res.content)
            fout.flush()
            fout.close()
            click.echo(f"gamedata-static.bin is written to {self.output_path}/{self.meta.gamedata_version}_gamedata.bin")
