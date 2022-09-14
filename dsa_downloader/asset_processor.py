import click
import UnityPy
import requests
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from dsa_downloader import meta
from dsa_downloader import metadata
import os.path


class AssetHandler:
    def __init__(self, debug, bootstrap_file, output_path, extracted_path, threads):
        self.debug = debug
        self.meta = meta.Meta(bootstrap_file)
        self.metadata = metadata.Metadata(self.meta)
        self.output_path = output_path
        self.extracted_path = extracted_path
        self.threads = threads
        self.pbar = tqdm(total=len(self.metadata.bundle_info))
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(extracted_path, exist_ok=True)

    def process_asset(self, bundle, is_extract):
        is_download = True
        bundle_name = bundle.bundle_name
        bundle_size = bundle.download_size_byte
        file_name = f'{self.output_path}/{bundle_name}'

        if os.path.isfile(file_name):
            size = os.path.getsize(file_name)

            if bundle_size == size:
                is_download = False
                if self.debug:
                    print(f'Skipping {bundle_name}')
        if is_download:
            if self.debug:
                print(f'Downloading {bundle_name}')
            asset = requests.get(f'{self.metadata.android_asset_url}/{bundle_name}')
            with open(file_name, 'wb+') as fout:
                fout.write(asset.content)
                fout.flush()
                fout.close()
            if is_extract:
                self.extract_asset(bundle)
        self.pbar.update(1)

    def process_assets(self, is_extract):
        self.pbar.reset()
        executor = ThreadPoolExecutor(max_workers=self.threads)

        for bundle in self.metadata.bundle_info:
            executor.submit(self.process_asset, bundle, is_extract)
        executor.shutdown()
        self.pbar.close()

    def extract_asset(self, bundle):
        file_name = bundle.bundle_name
        destination_folder = self.extracted_path
        env = UnityPy.load(f'{self.output_path}/{file_name}')

        if file_name.startswith('emote_'):
            image_dict = {}
            for obj in env.objects:
                try:
                    if obj.type in ["Texture2D", "Sprite"]:
                        im = obj.read().image
                        alpha = im.getchannel('A')

                        # Convert the image into P mode but only use 255 colors in the palette out of 256
                        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

                        # Set all pixel values below 128 to 255 , and the rest to 0
                        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

                        # Paste the color of index 255 and use alpha as a mask
                        im.paste(255, mask)

                        # The transparency index is 255
                        im.info['transparency'] = 255

                        image_dict[obj.path_id] = im
                except:
                    if self.debug:
                        print("emote> failed to process " + file_name + ': ' + str(obj))

            for container, obj in env.container.items():
                data = obj.read()

                path_ids = []
                for sprite in data._sprites:
                    if sprite['m_PathID'] != 0:
                        path_ids.append(sprite['m_PathID'])

                images = []
                for path_id in path_ids:
                    if path_id in image_dict:
                        images.append(image_dict[path_id])
                    else:
                        if self.debug:
                            print('emote> ' + file_name + ' missed m_PathID: ' + str(path_id))

                if len(images) == 0 and self.debug:
                    print('emote> ' + file_name + ' has 0 image and was skipped ')
                    continue
                img, *imgs = images

                head, tail = os.path.split(container)
                dest = os.path.join(destination_folder, file_name, tail)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                dest, ext = os.path.splitext(dest)
                dest = dest + ".gif"

                if not os.path.exists(dest):
                    img.save(fp=dest, format='GIF', append_images=imgs, save_all=True, fps=data._fps,
                             duration=data._durationS * 1000 / len(images), loop=0, disposal=2)
        else:
            for path, obj in env.container.items():
                try:
                    if obj.type in ["Texture2D", "Sprite"]:
                        data = obj.read()
                        head, tail = os.path.split(path)
                        dest = os.path.join(destination_folder, file_name, tail)

                        os.makedirs(os.path.dirname(dest), exist_ok=True)

                        if not os.path.exists(dest):
                            data.image.save(dest)
                except:
                    if self.debug:
                        print("container> failed to process " + file_name + " " + str(obj))

            for obj in env.objects:
                try:
                    if obj.type in ["Texture2D", "Sprite"]:
                        data = obj.read()
                        dest = os.path.join(destination_folder, file_name, data.name)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)

                        path, ext = os.path.splitext(dest)
                        if ext == '':
                            dest = path + ".png"

                        if not os.path.exists(dest):
                            img = data.image
                            img.save(dest)
                    elif obj.type == 'AudioClip':
                        clip = obj.read()
                        for name, data in clip.samples.items():
                            dest = os.path.join(destination_folder, file_name, name)
                            os.makedirs(os.path.dirname(dest), exist_ok=True)
                            if not os.path.exists(dest):
                                with open(dest, "wb") as f:
                                    f.write(data)

                    # TODO: unit_XXXX -> .fbx
                    # elif obj.type == 'Animator':
                    #     data = obj.read()
                    #     print(obj.__dict__)
                    #     print(dir(data))

                    #     data.save(dest)
                except:
                    if self.debug:
                        print("objects> failed to process " + file_name + " " + str(obj))
