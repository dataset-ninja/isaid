# https://captain-whu.github.io/iSAID/dataset.html
import os
from collections import defaultdict

import supervisely as sly
from dotenv import load_dotenv
from PIL import Image
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
from supervisely.io.json import load_json_file

Image.MAX_IMAGE_PIXELS = None
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_size
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    # project_name = "iSAID"
    train_anns_path = (
        "/home/grokhi/rawdata/isaid/train/Annotations/iSAID_train.json"
    )
    val_anns_path = (
        "/home/grokhi/rawdata/isaid/val/Annotations/iSAID_val.json"
    )
    val_images_path = "/home/grokhi/rawdata/dota/1_0/val/images"
    train_images_path = "/home/grokhi/rawdata/dota/1_0/train/images"
    batch_size = 30
    test_images_path = "/home/grokhi/rawdata/isaid/test"

    name_to_path = {
        "train": (train_images_path, train_anns_path),
        "val": (val_images_path, val_anns_path),
        "test": (test_images_path, None),
    }

    img_ext = '.png'


    def create_ann(image_path):
        labels = []

        image = Image.open(image_path)
        img_height = image.height
        img_wight = image.width

        im_name = get_file_name_with_ext(image_path)

        ann_data = image_name_to_ann_data[im_name]
        for curr_ann_data in ann_data:
            category_id = curr_ann_data[0]
            polygons_coords = curr_ann_data[1]
            for coords in polygons_coords:
                exterior = []
                for i in range(0, len(coords), 2):
                    exterior.append([int(coords[i + 1]), int(coords[i])])
                if len(exterior) < 3:
                    continue
                poligon = sly.Polygon(exterior)
                label_poly = sly.Label(poligon, idx_to_obj_class[category_id])
                labels.append(label_poly)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta()

    idx_to_obj_class = {}

    for ds_name in ["train", "val", "test"]:
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path = name_to_path[ds_name][0]
        anns_path = name_to_path[ds_name][1]
        images_names = [name for name in os.listdir(images_path) if img_ext in name]

        if ds_name != "test":
            ann = load_json_file(anns_path)
            image_id_to_name = {}
            image_name_to_ann_data = defaultdict(list)
            for curr_category in ann["categories"]:
                if idx_to_obj_class.get(curr_category["id"]) is None:
                    obj_class_poly = sly.ObjClass(curr_category["name"].lower(), sly.Polygon)
                    meta = meta.add_obj_class(obj_class_poly)
                    idx_to_obj_class[curr_category["id"]] = obj_class_poly
            api.project.update_meta(project.id, meta.to_json())

            for curr_image_info in ann["images"]:
                image_id_to_name[curr_image_info["id"]] = curr_image_info["file_name"]

            for curr_ann_data in ann["annotations"]:
                image_id = curr_ann_data["image_id"]
                image_name_to_ann_data[image_id_to_name[image_id]].append(
                    [curr_ann_data["category_id"], curr_ann_data["segmentation"]]
                )

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [os.path.join(images_path, im_name) for im_name in img_names_batch]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            if ds_name != "test":
                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))
    return project


