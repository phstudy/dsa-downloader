import click
from dsa_downloader import config_extractor
from dsa_downloader import language_downloader
from dsa_downloader import asset_processor


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
@click.argument('path_to_apk', type=click.Path())
@click.argument('output_path', type=click.Path(dir_okay=False), default='out/bootstrap_config.json')
def extract_config(ctx, path_to_apk, output_path):
    extractor = config_extractor.ConfigExtractor(ctx.obj['DEBUG'])
    extractor.bootstrap_extract_config(path_to_apk, output_path)


@cli.command()
@click.pass_context
@click.argument('path_to_boostrap_config', type=click.Path(), default='out/bootstrap_config.json')
@click.argument('output_path', type=click.Path(), default='out/langs')
@click.option('--langs', type=click.Choice(
    ["ChineseTraditional", "ChineseSimplified", "English", "French", "German", "Italian", "Japanese", "Korean",
     "PortugueseBrazilian", "Russian", "Spanish"], case_sensitive=False), default=["English"],
              multiple=True)
def download_langs(ctx, path_to_boostrap_config, output_path, langs):
    lang_downloader = language_downloader.LanguageDownloader(ctx.obj['DEBUG'], path_to_boostrap_config, output_path)

    for lang in langs:
        lang_downloader.download_lang(lang)


@cli.command()
@click.pass_context
@click.argument('path_to_boostrap_config', type=click.Path(), default='out/bootstrap_config.json')
@click.argument('output_path', type=click.Path(), default='out/assets')
@click.argument('extracted_path', type=click.Path(), default='out/assets_extracted')
@click.option('--extract_asset', type=click.BOOL, default=True)
@click.option('--threads', type=click.INT, default=10)
def download_assets(ctx, path_to_boostrap_config, output_path, extract_asset, extracted_path, threads):
    handler = asset_processor.AssetHandler(ctx.obj['DEBUG'], path_to_boostrap_config, output_path, extracted_path,
                                           threads)
    handler.process_assets(extract_asset)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
