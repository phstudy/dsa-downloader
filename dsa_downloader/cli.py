import click
from dsa_downloader import config_extractor
from dsa_downloader import language_downloader
from dsa_downloader import asset_processor
from dsa_downloader import gamedata_downloader


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command(help='Extract bootstrap config from APK file.')
@click.pass_context
@click.argument('path_to_apk', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(dir_okay=False), default='out/bootstrap_config.json')
def extract_config(ctx, path_to_apk, output_path):
    extractor = config_extractor.ConfigExtractor(ctx.obj['DEBUG'])
    extractor.bootstrap_extract_config(path_to_apk, output_path)


@cli.command(help='Download gamedata.')
@click.pass_context
@click.argument('path_to_boostrap_config', type=click.Path(exists=True), default='out/bootstrap_config.json')
@click.argument('output_path', type=click.Path(), default='out/gamedata')
def download_gamedata(ctx, path_to_boostrap_config, output_path):
    downloader = gamedata_downloader.GamedataDownloader(ctx.obj['DEBUG'], path_to_boostrap_config, output_path)
    downloader.download_gamedata()


@cli.command(help='Download localization files.')
@click.pass_context
@click.argument('path_to_boostrap_config', type=click.Path(exists=True), default='out/bootstrap_config.json')
@click.argument('output_path', type=click.Path(), default='out/langs')
@click.option('--langs', type=click.Choice(
    ["ChineseTraditional", "ChineseSimplified", "English", "French", "German", "Italian", "Japanese", "Korean",
     "PortugueseBrazilian", "Russian", "Spanish"], case_sensitive=False), default=["English"],
              multiple=True, help="Languages to be extracted.")
def download_langs(ctx, path_to_boostrap_config, output_path, langs):
    lang_downloader = language_downloader.LanguageDownloader(ctx.obj['DEBUG'], path_to_boostrap_config, output_path)

    for lang in langs:
        lang_downloader.download_lang(lang)


@cli.command(help='Download assets.')
@click.pass_context
@click.argument('path_to_boostrap_config', type=click.Path(exists=True), default='out/bootstrap_config.json')
@click.argument('output_path', type=click.Path(), default='out/assets')
@click.argument('extracted_path', type=click.Path(), default='out/assets_extracted')
@click.option('--extract-asset', type=click.BOOL, default=True,
              help="Flag to turn on/off asset extraction.")
@click.option('--threads', type=click.INT, default=5,
              help="Threads count to download/extract assets.", metavar='<int>')
def download_assets(ctx, path_to_boostrap_config, output_path, extract_asset, extracted_path, threads):
    handler = asset_processor.AssetHandler(ctx.obj['DEBUG'], path_to_boostrap_config, output_path, extracted_path,
                                           threads)
    handler.process_assets(extract_asset)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
