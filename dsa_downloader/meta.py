from dsa_downloader import meta_pb2
import requests
import json


class Meta:
    def __init__(self, boostrap_file):
        boostrap = json.load(open(boostrap_file))
        req = meta_pb2.RequestEnvelope()
        req.payload.device_info.platform = meta_pb2.DevicePlatform.ANDROID_DEVICE_PLATFORM
        req.payload.device_info.gpu_name = 'Adreno (TM) 660'
        req.client_version = boostrap['client_version']
        req.rpc_name = 'meta'

        meta = requests.post(f'{boostrap["service_url"]}meta', data=req.SerializeToString())

        res = meta_pb2.ResponseEnvelope()
        res.ParseFromString(meta.content)

        self.loc_version = res.payload.loc_version
        self.loc_cdn_base_url = res.payload.loc_cdn_base_url
        self.asset_cdn_base_url = res.payload.asset_cdn_base_url
        self.bundle_version = res.payload.bundle_version
        self.gamedata_version = res.payload.gamedata_version