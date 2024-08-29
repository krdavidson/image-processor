# Image Processor
 
Tool to process an image to output a line drawing of the image. 

![alt text](images/example2.png) ![alt text](images/example1.png)

## Getting Started 
To run the project locally:

1. Clone the project:
    ```bash
    git clone <repository_url>
    cd path/to/image-processor
    ```

2. Run the program:
- If you would like to use the default test image:
    ```bash
    python processor.py
    ```

- If you would like to use your own PNG image:
    ```bash
    python processor.py <image_input_path> <image_output_path>
    ```
    Ex: `python processor.py ./images/image_name.png ./output_images/image_name_output.png`

The output image will pop-up when processing has completed. A copy of the image will also be saved to the output_images folder.

## Acknowledgements
Default and test images sourced from Unsplash:
- https://unsplash.com/photos/pink-petaled-flower-YdAqiUkUoWA 
- https://unsplash.com/photos/a-man-walking-down-a-sidewalk-next-to-a-building-pOkImMZ29c0


