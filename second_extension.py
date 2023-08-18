import math
import sys
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import imageIO.png
import tkinter
from tkinter import *
# import filedialog module
from tkinter import filedialog

def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
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
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

def seperateArraysToRBG(px_array_r, px_array_g, px_array_b,image_width,image_height):
    new_array = [[[0 for x in range(3)] for y in range(image_width)] for z in range(image_height)]
    for i in range(image_height):
        for j in range(image_width):
            new_array[i][j][0] = px_array_r[i][j]
            new_array[i][j][1] = px_array_g[i][j]
            new_array[i][j][2] = px_array_b[i][j]
    return new_array
# You can add your own functions here:

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(image_height):
        for j in range(image_width):
            greyscale_pixel_array[i][j]  = round(pixel_array_r[i][j]*0.299 + 0.587*pixel_array_g[i][j]+0.114*pixel_array_b[i][j])
            
    return greyscale_pixel_array

# def computeStandardDeviationImage3x3(pixel_array, image_width, image_height):
#     average_array = createInitializedGreyscalePixelArray(image_width, image_height,0.0)
    
#     l = []
#     for i in range(1,image_height-1):
#         for j in range(1,image_width-1):
#             mean = abs(pixel_array[i-1][j-1] + pixel_array[i-1][j] + pixel_array[i-1][j+1] + pixel_array[i][j-1]  + pixel_array[i][j] + pixel_array[i][j+1] + pixel_array[i+1][j-1]+ pixel_array[i+1][j]+ pixel_array[i+1][j+1])/9.0
#             val = ((pixel_array[i-1][j-1]-mean)**2 +(pixel_array[i-1][j]-mean)**2 + (pixel_array[i-1][j+1]-mean)**2 + ( pixel_array[i][j-1]-mean)**2 + (pixel_array[i][j]-mean)**2 + (pixel_array[i][j+1]-mean)**2 + (pixel_array[i+1][j-1]-mean)**2+ (pixel_array[i+1][j]-mean)**2+ (pixel_array[i+1][j+1]-mean)**2)/9.0
#             average_array[i][j] = math.sqrt(val)
#     return average_array

def computeStandardDeviationImage3x3(pixel_array, image_width, image_height):
    average_array = createInitializedGreyscalePixelArray(image_width, image_height,0.0)
    
    l = []
    for i in range(2, image_height - 2):
        for j in range(2, image_width - 2):
            mean = 0.0
            for k in range(i - 2, i + 3):
                for l in range(j - 2, j + 3):
                    mean += pixel_array[k][l]
            mean /= 25.0

            val = 0.0
            for k in range(i - 2, i + 3):
                for l in range(j - 2, j + 3):
                    val += (pixel_array[k][l] - mean) ** 2
            val /= 25.0

            average_array[i][j] = math.sqrt(val)

    return average_array



#function for 
def computeSobelFilter(greyscale_pixel_array, image_width, image_height):
    sobelArray_x = createInitializedGreyscalePixelArray(image_width, image_height)
    sobelArray_y = createInitializedGreyscalePixelArray(image_width, image_height)
    #for the x array
    for i in range(1,image_height-1):
        for j in range(1,image_width-1):
            #check if use absoulte value here
            sobelArray_x[i][j]  = abs(greyscale_pixel_array[i-1][j-1] + 2*greyscale_pixel_array[i-1][j] + greyscale_pixel_array[i-1][j+1] - greyscale_pixel_array[i+1][j-1]  - 2*greyscale_pixel_array[i+1][j] - greyscale_pixel_array[i+1][j+1])/8.0
    #for the y array
    for i in range(1,image_height-1):
        for j in range(1,image_width-1):
            #check if use absoulte value here
            sobelArray_y[i][j]  = abs(-greyscale_pixel_array[i-1][j-1] - 2*greyscale_pixel_array[i][j-1] - greyscale_pixel_array[i+1][j-1] + greyscale_pixel_array[i-1][j+1]  + 2*greyscale_pixel_array[i][j+1] + greyscale_pixel_array[i+1][j+1])/8.0
    
    gradient_magnitude = createInitializedGreyscalePixelArray(image_width, image_height)

    for i in range(image_height):
        for j in range(image_width):
            gradient_magnitude[i][j] = abs(sobelArray_x[i][j] - sobelArray_y[i][j])

    return gradient_magnitude

#gaussian filter
def computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height):
    Gaussian_array = createInitializedGreyscalePixelArray(image_width, image_height)
    pixel_array.insert(0,pixel_array[0].copy())
    pixel_array.append(pixel_array[len(pixel_array)-1].copy())
    
    # for i in range(image_height):
    #     for j in range(image_width):
    
    for i in range(image_height+2):
        pixel_array[i].append(pixel_array[i][-1])
        pixel_array[i].insert(0,pixel_array[i][0])
        
    for i in range(1,len(pixel_array)-1):
        for j in range(1,len(pixel_array[0])-1):
            Gaussian_array[i-1][j-1] = (4*pixel_array[i][j] + 2*pixel_array[i-1][j]+ 2*pixel_array[i+1][j] + 2*pixel_array[i][j-1] + 2*pixel_array[i][j+1] + pixel_array[i-1][j-1] + pixel_array[i-1][j+1] + pixel_array[i+1][j-1] + pixel_array[i+1][j+1])/16.0
        
    return Gaussian_array


#CHECK ON 22 VALUE AGAI BOY
#19 for standard deviation
#10 works but gives errors for barcode 3 , 6 ,7 
def computethreshold(pixel_array, image_width, image_height):
    threshold_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j] >= 15:
                threshold_array[i][j] = 255
            else:
                threshold_array[i][j] = 0
    return threshold_array

def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    dilation_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    pixel_array.insert(0, [0] * len(pixel_array[0]))
    pixel_array.insert(0, [0] * len(pixel_array[0]))
    pixel_array.append([0] * len(pixel_array[0]))
    pixel_array.append([0] * len(pixel_array[0]))
    
    for row in pixel_array:
        row.insert(0, 0)
        row.insert(0, 0)
        row.append(0)
        row.append(0)
    count = 0
    for i in range(2,len(pixel_array)-2):
        for j in range(2,len(pixel_array[0])-2):
            valid_pixels = any(pixel_array[i+x][j+y] != 0 for x in range(-2, 3) for y in range(-2, 3))
            if valid_pixels:
                dilation_array[i-2][j-2] = 1

    return dilation_array

# def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
#     dilation_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
#     pixel_array.insert(0, [0] * len(pixel_array[0]))
#     pixel_array.append([0] * len(pixel_array[0]))
    
#     for row in pixel_array:
#         row.insert(0, 0)
#         row.append(0)
#     count = 0
#     for i in range(1,len(pixel_array)-1):
#         for j in range(1,len(pixel_array[0])-1):
#             if pixel_array[i-1][j-1] != 0 or  pixel_array[i-1][j] != 0 or pixel_array[i-1][j+1] != 0 or pixel_array[i][j]!= 0 or pixel_array[i][j-1]!= 0 or pixel_array[i][j+1]!= 0 or pixel_array[i+1][j-1]!=0 or pixel_array[i+1][j]!= 0 or  pixel_array[i+1][j+1]!= 0:
#                 dilation_array[i-1][j-1] = 1
    
#     return dilation_array

def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    erosian_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    pixel_array.insert(0, [0] * len(pixel_array[0]))
    pixel_array.insert(0, [0] * len(pixel_array[0]))
    pixel_array.append([0] * len(pixel_array[0]))
    pixel_array.append([0] * len(pixel_array[0]))
    
    for row in pixel_array:
        row.insert(0, 0)
        row.insert(0, 0)
        row.append(0)
        row.append(0)
    count = 0
    for i in range(2,len(pixel_array)-2):
        for j in range(2,len(pixel_array[0])-2):
            valid_pixels = all(pixel_array[i+x][j+y] != 0 for x in range(-2, 3) for y in range(-2, 3))
            valid_pixels2 = any(pixel_array[i+x][j+y] != 0 for x in range(-2, 3) for y in range(-2, 3))
            valid_pixels3 = all(pixel_array[i+x][j+y] == 0 for x in range(-2, 3) for y in range(-2, 3))
            if valid_pixels:
                 erosian_array[i-2][j-2] = 1
            elif valid_pixels2:
                erosian_array[i-2][j-2] = 0
            elif valid_pixels3:
                erosian_array[i-2][j-2] = 0
            else:
                erosian_array[i-2][j-2] = 1
    
    return erosian_array

# def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
#     erosian_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
#     pixel_array.insert(0, [0] * len(pixel_array[0]))
#     pixel_array.append([0] * len(pixel_array[0]))
    
#     for row in pixel_array:
#         row.insert(0, 0)
#         row.append(0)
#     count = 0
#     for i in range(1,len(pixel_array)-1):
#         for j in range(1,len(pixel_array[0])-1):
#             if pixel_array[i-1][j-1] != 0 and  pixel_array[i-1][j] != 0 and pixel_array[i-1][j+1] != 0 and pixel_array[i][j-1]!= 0 and pixel_array[i][j]!= 0 and pixel_array[i][j+1]!= 0 and pixel_array[i+1][j-1]!=0 and pixel_array[i+1][j]!= 0 and  pixel_array[i+1][j+1]!= 0:
#                 erosian_array[i-1][j-1] = 1
#             elif pixel_array[i-1][j-1] != 0 or  pixel_array[i-1][j] != 0 or pixel_array[i-1][j+1] != 0 or pixel_array[i][j-1]!= 0 or pixel_array[i][j]!= 0 or pixel_array[i][j+1]!= 0 or pixel_array[i+1][j-1]!=0 or pixel_array[i+1][j]!= 0 or  pixel_array[i+1][j+1]!= 0:
#                 erosian_array[i-1][j-1] = 0
#             elif pixel_array[i-1][j-1] == 0 and  pixel_array[i-1][j] == 0 and pixel_array[i-1][j+1] == 0 and pixel_array[i][j-1] == 0 and pixel_array[i][j] == 0 and pixel_array[i][j+1] == 0 and pixel_array[i+1][j-1] == 0 and pixel_array[i+1][j] == 0 and  pixel_array[i+1][j+1] == 0:
#                 erosian_array[i-1][j-1] = 0
#             else:
#                 erosian_array[i-1][j-1] = 1
    
#     return erosian_array

def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    current_label = 1
    visited = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            visited[i][j] = False
    labeled_image = createInitializedGreyscalePixelArray(image_width, image_height)
    component_sizes = {}
    count = 0
    
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j] > 0 and not visited[i][j]:
                count+=1
                q = Queue()
                q.enqueue((i, j))
                visited[i][j] = True
                size = 0
                
                while not q.isEmpty():
                    i_current, j_current = q.dequeue()
                    labeled_image[i_current][j_current] = current_label
                    size += 1
                   
                    #left
                    if j_current - 1 >= 0 and pixel_array[i_current][j_current-1] > 0 and not visited[i_current][j_current-1]:
                        q.enqueue((i_current, j_current-1))
                        visited[i_current][j_current-1] = True
                    #right
                    if j_current + 1 < image_width and pixel_array[i_current][j_current+1] > 0 and not visited[i_current][j_current+1]:
                        q.enqueue((i_current, j_current+1))
                        visited[i_current][j_current+1] = True
                    #top
                    if i_current - 1 >= 0 and pixel_array[i_current-1][j_current] > 0 and not visited[i_current-1][j_current]:
                        q.enqueue((i_current-1, j_current))
                        visited[i_current-1][j_current] = True
                    #bottom
                    if  i_current + 1 < image_height and pixel_array[i_current+1][j_current] > 0 and not visited[i_current+1][j_current]:
                        q.enqueue((i_current+1, j_current))
                        visited[i_current+1][j_current] = True
                        
                component_sizes[current_label] = size
                current_label+=1
    if count==0:
        component_sizes[current_label] = count
                
    return labeled_image,component_sizes

def main(image_width, image_height, px_array_r, px_array_g, px_array_b,filename):
    
    command_line_arguments = sys.argv[1:]

    SHOW_DEBUG_FIGURES = True

    # this is the default input image filename
    input_filename = filename

    if command_line_arguments != []:
        input_filename = command_line_arguments[0]
        SHOW_DEBUG_FIGURES = False

    output_path = Path("output_images")
    if not output_path.exists():
        # create output directory
        output_path.mkdir(parents=True, exist_ok=True)

    output_filename = output_path / Path(filename+"_output.png")
    if len(command_line_arguments) == 2:
        output_filename = Path(command_line_arguments[1])
        
    # setup the plots for intermediate results in a figure
    fig1, axs1 = pyplot.subplots(2, 2)
    axs1[0, 0].set_title('Input red channel of image')
    axs1[0, 0].imshow(px_array_r, cmap='gray')
    axs1[0, 1].set_title('Input green channel of image')
    axs1[0, 1].imshow(px_array_g, cmap='gray')
    axs1[1, 0].set_title('Input blue channel of image')
    axs1[1, 0].imshow(px_array_b, cmap='gray')


    # STUDENT IMPLEMENTATION here
    (greyscale_pixel_array) = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)





    Standard_Deviation_array = computeStandardDeviationImage3x3(greyscale_pixel_array, image_width, image_height)
    #THE PART BELOW IS USING THE SOBEL SOLUTION#

    # sobel_edge_array = computeSobelFilter(greyscale_pixel_array, image_width, image_height)

    #doing a gaussian filter on the sobel passed image 4 times
    gaussian_array_1 = computeGaussianAveraging3x3RepeatBorder(Standard_Deviation_array, image_width, image_height)
    gaussian_array_2 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_1, image_width, image_height)
    gaussian_array_3 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_2, image_width, image_height)
    gaussian_array_4 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_3, image_width, image_height)
    gaussian_array_5 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_4, image_width, image_height)
    gaussian_array_6 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_5, image_width, image_height)
    # gaussian_array_7 = computeGaussianAveraging3x3RepeatBorder(gaussian_array_6, image_width, image_height)



    threshold_array =  computethreshold(gaussian_array_6, image_width, image_height)

    # dilation_array_1 = computeDilation8Nbh3x3FlatSE(threshold_array, image_width, image_height)
    # dilation_array_2 = computeDilation8Nbh3x3FlatSE(dilation_array_1, image_width, image_height)
    # dilation_array_3 = computeDilation8Nbh3x3FlatSE(dilation_array_2, image_width, image_height)
    # dilation_array_4 = computeDilation8Nbh3x3FlatSE(dilation_array_3, image_width, image_height)

    # erosion_array_1 = computeErosion8Nbh3x3FlatSE(dilation_array_2, image_width, image_height)
    # erosion_array_2 = computeErosion8Nbh3x3FlatSE(erosion_array_1, image_width, image_height)

    erosion_array_1 = computeErosion8Nbh3x3FlatSE(threshold_array, image_width, image_height)
    erosion_array_2 = computeErosion8Nbh3x3FlatSE(erosion_array_1, image_width, image_height)
    erosion_array_3 = computeErosion8Nbh3x3FlatSE(erosion_array_2, image_width, image_height)

    dilation_array_1 = computeDilation8Nbh3x3FlatSE(erosion_array_3, image_width, image_height)
    dilation_array_2 = computeDilation8Nbh3x3FlatSE(dilation_array_1, image_width, image_height)



    connected_array, component_sizes = computeConnectedComponentLabeling(dilation_array_2, image_width, image_height)
    while True:
        max_key = max(component_sizes, key=lambda k: component_sizes[k])
        
        min_x = 10000000000
        min_y = 10000000000
        max_x = 0
        max_y = 0 
        for i in range(image_height):
            for j in range(image_width):
                if connected_array[i][j] == max_key:
                    if i<min_y:
                        min_y = i
                    if i>max_y:
                        max_y = i
        
                    if j<min_x:
                        min_x = j
                    if j>max_x:
                        max_x = j

        #px_array is the real image
        total_count = 0
        pixel_count = 0
        for i in range(min_y,max_y):
            for j in range(min_x,max_x):
                total_count+=1
                if connected_array[i][j] != 0:
                    pixel_count+=1

        if pixel_count/total_count >= 0.67:
            break
        width_final = max_x - min_x
        height_final = max_y - min_y

        max_value = max(width_final, height_final)
        min_value = min(width_final, height_final)

        aspect_ratio = max_value / min_value
        
        if pixel_count/total_count >= 0.67 and aspect_ratio<=1.8:
            break

        del component_sizes[max_key]

        if not component_sizes: 
            print("No suitable connected component found.")
            break  

    px_array = seperateArraysToRBG(px_array_r, px_array_g, px_array_b,image_width,image_height)

    # Compute a dummy bounding box centered in the middle of the input image, and with as size of half of width and height
    # Change these values based on the detected barcode region from your algorithm
    # center_x = image_width / 2.0
    # center_y = image_height / 2.0
    # bbox_min_x = center_x - image_width / 4.0
    # bbox_max_x = center_x + image_width / 4.0
    # bbox_min_y = center_y - image_height / 4.0
    # bbox_max_y = center_y + image_height / 4.0

    bbox_min_x = min_x
    bbox_max_x = max_x
    bbox_min_y = min_y
    bbox_max_y = max_y


    # The following code is used to plot the bounding box and generate an output for marking
    # Draw a bounding box as a rectangle into the input image
    # px_array = np.stack((px_array_r, px_array_g, px_array_b), axis=-1)
    # image = Image.fromarray(px_array, 'RGB')
    # photo = ImageTk.PhotoImage(image)
    # label = Label(window, image=photo)
    # label.pack()
    # window.mainloop()



    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array, cmap='gray')
    rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
                     edgecolor='#ff10f0', facecolor='none')
    # rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
    #                  edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)

    # write the output image into output_filename, using the matplotlib savefig method
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)

    img = PhotoImage(file=output_filename)
    label = Label(container,image=img).grid(row = 3,column = 1 )
    print("test")
    # photo = Image.open(output_filename)
    # resized_image = photo.resize((300,150),Image.ANTIALIAS)
    # converted_image =ImageTk.PhotoImage(resized_image)

    # label = Label(window,image=converted_image).pack()



    window.update()
    label.image = img
    window.update()

    if SHOW_DEBUG_FIGURES:
        # plot the current figure
        pyplot.show()
    
    #image = Image.fromarray(px_array, 'RGB')
    # global photo
    # photo = ImageTk.PhotoImage(output_filename)
    # label = Label(window, image=photo)
    # label.pack()
    # window.mainloop()

def browseFiles():
    filetypes = (("PNG files", "*.png"),)
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=filetypes)
    #filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("PNG files","*.png*")))
    file = open(filename,'rb')
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    file.close()
    if __name__ == "__main__":
      main(image_width, image_height, px_array_r, px_array_g, px_array_b,filename)
    # Change label contents
    #label_file_explorer.configure(text="File Opened: "+filename)

window  = Tk()
labelText = Label(window, text = "Select a png image that contains a barcode and once the image is selected allow a few seconds for it to be processed",font=("Helvetica", 32),bg="grey")
labelText.pack()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.minsize(screen_width, screen_height)
button = Button(text = "Select Image", command= browseFiles)
button.configure(width=20, height=2,fg="white", bg="green",font=("Helvetica", 16))
button.pack()
window.title("PNG Image Barcode Scanner")

window.configure(bg="grey")
container = Frame(window)
container.pack()

window.mainloop()





