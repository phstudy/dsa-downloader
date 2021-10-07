from dsa_downloader import meta_pb2
import requests


class Metadata:
    def __init__(self, meta):
        self.android_asset_url = f'{meta.asset_cdn_base_url}/assets/{meta.bundle_version}-Android'
        metadata_url = f'{self.android_asset_url}/metadata'

        asset_bundle_metadata = meta_pb2.AssetBundleMetadata()
        asset_bundle_metadata.ParseFromString(requests.get(metadata_url).content)
        self.bundle_info = asset_bundle_metadata.bundle_info
