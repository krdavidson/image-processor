import sys
from matplotlib import pyplot
import imageIO.png 

def rgb_image_to_pixels(input_filename):
    image_reader = imageIO.png.Reader(input_filename)
    # png reader returns image width, height, and RGB data in rgb_image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()
    print("Reading image width={}, height={}".format(image_width, image_height))

    # The pixel arrays are lists of lists, where each inner list stores one row of image pixels
    # Each pixel is an 8 bit integer value between 0-255 encoding the color values 
    # which contribute to the overall pixel colour
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for px in range(len(row)):
            if px % 3 == 0:
                r = row[px]
            elif px % 3 == 1:
                g = row[px]
            else:
                b = row[px]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)
    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# Create a list of lists which represents the pixel matrix of an image, initialized with a pixel value
def create_initialized_pixel_array(image_width, image_height, init_value = 0):
    new_pixel_array = []
    for _ in range(image_height):
        new_row = []
        for _ in range(image_width):
            new_row.append(init_value)
        new_pixel_array.append(new_row)
    return new_pixel_array

def get_histogram(px_array):
    histogram = [0] * 256
    for row in px_array:
        for num in row:
            histogram[num] += 1
    return histogram

def get_cumulative_histogram(histogram):
    cumulative_histogram = [0] * 256
    running_total = 0
    index = 0
    for num in histogram:
        running_total += num
        cumulative_histogram[index] = running_total
        index += 1
    return cumulative_histogram

# Convert RGB colour image to greyscale image using RGB ratio 0.3 : 0.6 : 0.1
def convert_rgb_to_greyscale(image_width, image_height, px_array_r, px_array_g, px_array_b):
    greyscale_pixel_array = create_initialized_pixel_array(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            gs = (px_array_r[i][j] * 0.3) + (px_array_g[i][j] * 0.6) + (px_array_b[i][j] * 0.1)
            gs = round(gs)
            gs = int(gs)
            greyscale_pixel_array[i][j] = gs
    return greyscale_pixel_array

# Find qa (smallest value st cumulative_histogram[qa] > 5% of total pixels) 
# and qb (largest value st qb < 95% of total pixels)
def get_qa_qb(image_width, image_height, cumulative_histogram):
    total_px = image_width * image_height
    a = total_px * 0.05
    b = total_px * 0.95
    qa = 0
    qb = 0
    for i in range(256):
        if cumulative_histogram[i] > a:
            qa = i
            break
    for i in range(255, -1, -1):
        if cumulative_histogram[i] < b:
            qb = i
            break
    return (qa, qb)

# Stretch the pixel values using the 5-95 percentile mapping strategy to maximise contrast 
def contrast_stretch(px_array, image_width, image_height):
    histogram = get_histogram(px_array)
    cumulative_histogram = get_cumulative_histogram(histogram)
    qa, qb = get_qa_qb(image_width, image_height, cumulative_histogram)

    # Linear mapping of px_array to contrast stretch each pixel value in the image
    for i in range(image_height):
        for j in range(image_width):
            cs = 255/(qb - qa) * (px_array[i][j] - qa)
            if cs < 0:
                cs = 0
            elif cs > 255:
                cs = 255
            px_array[i][j] = cs
    return px_array

# Apply a 3x3 Scharr filter in horizontal and vertical directions to detect the edges in the image
def edge_detection(px_array, image_width, image_height):
    edge_detection = create_initialized_pixel_array(image_width, image_height, 0)
    scharr_h = [3, 0, -3, 10, 0, -10, 3, 0, -3]
    scharr_v = [3, 10, 3, 0, 0, 0, -3, -10, -3]

    for row in range(image_height):
        for col in range(image_width):
            # Ignore border pixels - set to 0
            if (row == 0) or (row == image_height-1) or (col == 0) or (col == image_width-1):
                edge_detection[row][col] = 0.0
            else:
                total_h = 0
                total_v = 0
                index = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        total_h += px_array[row+i][col+j] * scharr_h[index]
                        total_v += px_array[row+i][col+j] * scharr_v[index]
                        index += 1
                total_h = total_h/32
                total_v = total_v/32                
                edge_detection[row][col] = abs(total_h) + abs(total_v)
    return edge_detection

# Segment main object(s) from background
def threshold(px_array, image_width, image_height):
    for row in range(image_height):
        for col in range(image_width):
            if px_array[row][col] < 20:
                px_array[row][col] = 0
            else:
                px_array[row][col] = 255
    return px_array

# Output black lines and white background 
def flip_black_and_white(px_array, image_width, image_height):
    for row in range(image_height):
        for col in range(image_width):
            px_array[row][col] = 255 - px_array[row][col]
    return px_array

#############################

def main(input_path='./images/han-chenxu-YdAqiUkUoWA-unsplash.png',
         output_path='./output_images/han-chenxu-YdAqiUkUoWA-unsplash_output.png'):
    # Read in the png file, and receive three pixel arrays for red, green and blue components
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = rgb_image_to_pixels(input_path)
    
    # Image processing steps
    print("Processing your image... Thank you for waiting")
    px_array = convert_rgb_to_greyscale(image_width, image_height, px_array_r, px_array_g, px_array_b)
    px_array = contrast_stretch(px_array, image_width, image_height)
    px_array = edge_detection(px_array, image_width, image_height)
    px_array = threshold(px_array, image_width, image_height)
    px_array = flip_black_and_white(px_array, image_width, image_height)

    # Pop-up the processed image, save it to output folder
    pyplot.axis('off')
    pyplot.imshow(px_array, cmap='gray', aspect='equal')
    pyplot.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0)  
    pyplot.show()

if __name__ == "__main__":
    num_of_args = len(sys.argv) - 1
    if num_of_args > 0:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)
    else:
        main()