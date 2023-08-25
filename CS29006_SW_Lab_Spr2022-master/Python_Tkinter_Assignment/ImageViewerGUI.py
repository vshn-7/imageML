####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from tkinter import *
from tkinter import ttk,filedialog
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from my_package.model import InstanceSegmentationModel
from my_package.data.dataset import Dataset
from my_package.analysis.visualize import plot_visualization
from my_package.data.transforms.flip import FlipImage
from my_package.data.transforms.rescale import RescaleImage
from my_package.data.transforms.blur import BlurImage
from my_package.data.transforms.blur import BlurImage
from my_package.data.transforms.crop import CropImage
from my_package.data.transforms.rotate import RotateImage
from PIL import Image

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######


# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):

    ####### CODE REQUIRED (START) #######
    global file
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    file = filedialog.askopenfile(title = 'open file', initialdir='./data/imgs', filetypes =[('img files', '*.jpg,*.png')])
    if file is not None:
        e.delete(0, "end")
        idx = int(os.path.spiltext(os.path.basename(file))[0])
        ouTput = ['./outputs/' + f'Bounding-box/{os.path.basename(file)}','./outputs/' + f'Segmentation/{os.path.basename(file)}']
        if not (os.path.exists(ouTput[0]) or os.path.exists(ouTput[1])):
            box, mask, clases, score = segmentor(dataset[idx]['image'])
            plot_visualization(dataset[idx]['image'],mask, box, clases, output=ouTput)
        process(clicked)
    ####### CODE REQUIRED (END) #######

# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):

    ####### CODE REQUIRED (START) #######
    global file,canv
    canv.get_tk_widget().destroy()
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
    if file:
        clickimg = PIL.Image.open('./outputs/' + clicked.get() + '/' +os.path.basename(file))
        img = PIL.Image.open(file)
        figure = plt.figure(figsize=(14, 6))
        p1 = figure.add_subplot(121)
        p1.axis('off')
        p2 = figure.add_subplot(122)
        p2.axis('off')
        p1.imshow(img)
        p2.imshow(clickimg)
        plt.close()
        canv = FigureCanvasTkAgg(figure, master=root)
        canv.draw()
        canv.get_tk_widget().grid(row=1, column=0, columnpan=4)
        e.delete(0, 'end')
    else:
        e.delete(0, 'end')
        e.insert(0, "")
    ####### CODE REQUIRED (END) #######

# `main` function definition starts from here.
if __name__ == '__main__':
    
    ####### CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.geometry('200x100')
    root.title("window")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    
    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = StringVar()
    clicked.set(options[0])

    e = Entry(root, width=70)
    e.grid(row=0, column=0)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    fil = Button(root,text="Browse files",command=partial(process,fileClick(clicked, dataset, segmentor ) ))
    fil.grid(row=0,column=1)
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    drop = OptionMenu( root , clicked , *options )
    drop.grid(row=0,column=2)

    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    process = Button(root, text="Process", command=partial(process, clicked))
    process.grid(row=0, column=3)

    
    ####### CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    ####### CODE REQUIRED (END) #######