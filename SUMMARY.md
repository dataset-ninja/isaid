**iSAID: A Large-scale Dataset for Instance Segmentation in Aerial Images** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the geospatial domain. 

The dataset consists of 2806 images with 471760 labeled objects belonging to 15 different classes including *small_vehicle*, *large_vehicle*, *tennis_court*, and other: *ground_track_field*, *ship*, *harbor*, *storage_tank*, *swimming_pool*, *plane*, *bridge*, *roundabout*, *baseball_diamond*, *soccer_ball_field*, *basketball_court*, and *helicopter*.

Images in the iSAID dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 937 (33% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *train* (1411 images), *test* (937 images), and *val* (458 images). The dataset was released in 2019 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Inception.AI, UAE</span>, <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Wuhan UNiversity, China</span>, and <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Huazhong University of Science and Technology, China</span>.

Here are the visualized examples for the classes:

[Dataset classes](https://github.com/dataset-ninja/isaid/raw/main/visualizations/classes_preview.webm)
