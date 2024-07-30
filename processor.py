from matplotlib import pyplot
# Import png reader library
import imageIO.png 


def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(input_filename)
    # png reader returns image width, height, and RGB data in rgb_image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

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
def createInitializedPixelArray(image_width, image_height, init_value = 0):
    new_pixel_array = []
    for _ in range(image_height):
        new_row = []
        for _ in range(image_width):
            new_row.append(init_value)
        new_pixel_array.append(new_row)
    return new_pixel_array

def getHistogram(px_array):
    histogram = [0] * 256
    for row in px_array:
        for num in row:
            histogram[num] += 1
    return histogram

def getCumulativeHistogram(histogram):
    cumulative_histogram = [0] * 256
    running_total = 0
    index = 0
    for num in histogram:
        running_total += num
        cumulative_histogram[index] = running_total
        index += 1
    return cumulative_histogram

# Convert RGB colour image to greyscale image using ratio 0.3 : 0.6 : 0.1
def convertRGBtoGreyscale(image_width, image_height, px_array_r, px_array_g, px_array_b):
    greyscale_pixel_array = createInitializedPixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            gs = (px_array_r[i][j] * 0.3) + (px_array_g[i][j] * 0.6) + (px_array_b[i][j] * 0.1)
            gs = round(gs)
            gs = int(gs)
            greyscale_pixel_array[i][j] = gs
    return greyscale_pixel_array

# Stretch the pixel values using the 5-95 percentile mapping strategy to maximise contrast 
def contrastStretch(px_array, image_width, image_height):
    # Compute the histograms
    histogram = getHistogram(px_array)
    cumulative_histogram = getCumulativeHistogram(histogram)
    
    # Find qa (smallest value st cumulative_histogram[qa] > 5% of total pixels) 
    # and qb (largest value st qb < 95% of total pixels)
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
def edgeDetection(px_array, image_width, image_height):
    edge_detection = createInitializedPixelArray(image_width, image_height, 0)
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

def flip(px_array, image_width, image_height):
    for row in range(image_height):
        for col in range(image_width):
            px_array[row][col] = 256 - px_array[row][col]
    return px_array



#############################

def main(input_filename=f'./images/han-chenxu-YdAqiUkUoWA-unsplash.png'):
    # Change the 'image_name' variable to process different images
    image_name = 'han-chenxu-YdAqiUkUoWA-unsplash'
    input_filename = f'./images/{image_name}.png'

    # Read in the png file, and receive three pixel arrays for red, green and blue components
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)
    
    px_array = convertRGBtoGreyscale(image_width, image_height, px_array_r, px_array_g, px_array_b)
    px_array = contrastStretch(px_array, image_width, image_height)
    px_array = edgeDetection(px_array, image_width, image_height)
    px_array = flip(px_array, image_width, image_height)

    # Pop-up the processed image, save it to output folder
    pyplot.axis('off')
    pyplot.tight_layout()
    output_path = f'./output_images/{image_name}_output.png'
    pyplot.savefig(output_path, bbox_inches='tight', pad_inches=0)   
    pyplot.imshow(px_array, cmap='gray', aspect='equal')
    pyplot.show()

main()