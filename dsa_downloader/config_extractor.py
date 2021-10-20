import click
import pathlib
import UnityPy


class ConfigExtractor:
    def __init__(self, debug):
        self.debug = debug

    def bootstrap_extract_config(self, apk_path, output_path):
        env = UnityPy.load(apk_path)
        pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        if self.debug:
            click.echo("try to find bootstrap_config")

        for obj in env.objects:
            if obj.type == "TextAsset":
                data = obj.read()
                if data.name == "bootstrap_config":
                    if self.debug:
                        click.echo("bootstrap_config is found")
                        click.echo("try to extract bootstrap_config")
                    output_file = open(output_path, 'w')
                    output_file.write(data.text)
                    output_file.flush()
                    output_file.close()
                    click.echo(f"bootstrap_config file is written to {output_path}.")
                    exit(0)
