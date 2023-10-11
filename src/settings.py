from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "iSAID"
PROJECT_NAME_FULL: str = "iSAID: A Large-scale Dataset for Instance Segmentation in Aerial Images"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="https://captain-whu.github.io/iSAID/dataset.html")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Domain.Geospatial()]
CATEGORY: Category = Category.Aerial(extra=Category.Satellite())

CV_TASKS: List[CVTask] = [CVTask.InstanceSegmentation(), CVTask.SemanticSegmentation(), CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2019

HOMEPAGE_URL: str = "https://captain-whu.github.io/iSAID/index.html"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 7040826
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/isaid"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = "https://captain-whu.github.io/iSAID/dataset.html"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "storage_tank": [230, 25, 75],
    "large_vehicle": [60, 180, 75],
    "small_vehicle": [255, 225, 25],
    "plane": [0, 130, 200],
    "ship": [245, 130, 48],
    "swimming_pool": [145, 30, 180],
    "harbor": [70, 240, 240],
    "tennis_court": [240, 50, 230],
    "ground_track_field": [210, 245, 60],
    "soccer_ball_field": [250, 190, 212],
    "baseball_diamond": [0, 128, 128],
    "bridge": [220, 190, 255],
    "basketball_court": [170, 110, 40],
    "roundabout": [255, 250, 200],
    "helicopter": [128, 0, 0],

}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://arxiv.org/abs/1905.12886"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = "https://github.com/CAPTAIN-WHU/iSAID_Devkit"

CITATION_URL: Optional[str] = "https://captain-whu.github.io/iSAID/index.html"
AUTHORS: Optional[List[str]] = ["Syed Waqas Zamir", "Aditya Arora", "Akshita Gupta", "Salman Khan", "Guolei Sun", "Fahad Shahbaz Khan", "Fan Zhu", "Ling Shao", "Gui-Song Xia", "Xiang Bai"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["Inception.AI, UAE", "Wuhan UNiversity, China", "Huazhong University of Science and Technology, China"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://www.inceptioniai.org/", "https://www.whu.edu.cn/", "https://www.hust.edu.cn/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = None
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
