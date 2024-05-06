
import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

#Global Variables Section.
loaded_image = 0 #A flag (global variable) to check whether the image is loaded or not.
last_modified_image = 0 #A global variable to store the latest modified image.
converted_to_grayscale = 0 #A flag (global variable) to check whether the image is converted to grayscale or not.
thresholded = 0 #A flag to check whether the image is thresholded or not.

functions_menu = {
    'o': 'Open and show a color input image.',
    'g': 'Convert the image to gray-scale.',
    '+': 'Modify the brightness of the image by increasing it.',
    '-': 'Modify the brightness of the image by decreasing it.',
    'c': 'Improve the contrast of the image.',
    't': 'Apply thresholding to the image.',
    's': 'Save the processed image.',
    'e': 'exit.'
}

#Functions' Section: This section defines the required functions in my code.

#A function that prints the previously defined menu of the available functionalities.
def display_menu():
    print("\n These are the functionalities that can be applied to the input image:")
    #keys() method in Python Dictionary returns a view object that displays a list of all the keys in the dictionary in order of insertion.
    for key in functions_menu.keys():
        print('  ',key,':',functions_menu[key])

def open_image():
    #To change the value of the global variable inside a function, I have refered to the variable by using the global keyword.
    global loaded_image
    global last_modified_image
    global converted_to_grayscale

    converted_to_grayscale = 0
    last_modified_image = cv2.imread('inputImg.jpg', 1) #To load a color image.
    loaded_image = 1
    cv2.imshow("The Color Input Image", last_modified_image) #To display the image on a window called "The Color Input Image".
    cv2.waitKey(0) #To show the image window until I close it manually. 
    cv2.destroyAllWindows() #Simply, this allows me to destroy all windows I have created at any time.
    
def convert_to_grayscale():
    if loaded_image == 1:
        global converted_to_grayscale
        global last_modified_image
        global thresholded
        thresholded = 0
        if converted_to_grayscale == 0:
            last_modified_image = cv2.cvtColor(last_modified_image, cv2.COLOR_BGR2GRAY) #To convert the color input image to gray-scale.
            converted_to_grayscale = 1;
            cv2.imshow("The Obtained Grayscale Image", last_modified_image)
        else:
            messagebox.showinfo("Information Message", "The image is already grayscale!")
            cv2.imshow("The Obtained Grayscale Image", last_modified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        messagebox.showerror("Invalid Action", "Grayscale conversion of an input image is only possible after it has been loaded!" + 
                             " First, load the input image using the open function.")

def increase_brightness():
    #Only check if the image is converted to grayscale, no need to check if it is loaded,
    #as if it is converted to grayscale, then it will be loaded.
    if converted_to_grayscale == 1:
        global last_modified_image
                
        if(thresholded == 1):
            messagebox.showinfo("Information Message", "Since the image is thresholded, increasing the brightness won't have any effect on it.")
        
        else: 
            lookUpTable = np.empty((1, 256), np.uint8)
            for i in range(256):
                lookUpTable[0, i] = np.clip(pow(i / 255.0, 0.67) * 255.0, 0, 255)
            last_modified_image = cv2.LUT(last_modified_image, lookUpTable)

        cv2.imshow("The Obtained Brightened Image", last_modified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        messagebox.showerror("Invalid Action", "Brightening an image will only be possible after it has been converted to grayscale!" + 
                             " First, you must convert the input image to grayscale using the conversion function.")


def decrease_brightness():
    if converted_to_grayscale == 1:
        global last_modified_image
        
        if(thresholded == 1):
            messagebox.showinfo("Information Message", "Since the image is thresholded, decreasing the brightness won't have any effect on it.")

        else:
            lookUpTable = np.empty((1, 256), np.uint8)
            for i in range(256):
                lookUpTable[0, i] = np.clip(pow(i / 255.0, 1.5) * 255.0, 0, 255)
            last_modified_image = cv2.LUT(last_modified_image, lookUpTable)


        cv2.imshow("The Obtained Darkened Image", last_modified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        messagebox.showerror("Invalid Action", "Darkening an image will only be possible after it has been converted to grayscale!" +
                            " First, you must convert the input image to grayscale using the conversion function.")

def improve_contrast():
    if converted_to_grayscale == 1:
        global last_modified_image
        global thresholded
      
        thresholded = 0
        last_modified_image = cv2.equalizeHist(last_modified_image)
        cv2.imshow("The Enhanced-Contrast Image", last_modified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        messagebox.showerror("Invalid Action", "Improving the contrast of an image will only be possible after it has been converted to" +
                             " grayscale! First, you must convert the input image to grayscale using the conversion function.")


def apply_thresholding():
    if converted_to_grayscale == 1:
        threshold_value = int(input('\n Please enter a threshold value in range of 50 - 200: '))
        while threshold_value < 50 or threshold_value > 200:
            threshold_value = int(input('\n Please enter a valid threshold value within the predefined range: '))

        global last_modified_image
        global thresholded
        thresholded = 1
        _, last_modified_image = cv2.threshold(last_modified_image, threshold_value, 255, cv2.THRESH_BINARY)
        cv2.imshow("The Thresholded Image",  last_modified_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        messagebox.showerror("Invalid Action", "Thresholding an image will only be possible after it has been converted to" +
                             " grayscale! First, you must convert the input image to grayscale using the conversion function.")


def save_image():
    #At least the image should be loaded before it can be saved.
    if loaded_image == 1:
        root = tk.Tk()
        root.withdraw()
        #An input dialog to receive the name of the image to be saved.
        image_name = simpledialog.askstring(title = "Save Image", prompt = "Enter a name for the image you wish to save:")
        if image_name == None:
            pass
        else:
            cv2.imwrite(image_name + ".jpg", last_modified_image)
            messagebox.showinfo("Information Message", "The image has been successfully saved.")
    else:
        messagebox.showerror("Invalid Action", "The ability to save an image is only available after it has at least been loaded!" + 
                             " First, load the input image using the open function.")

#The end of the Functions' Section.

while(True):
    display_menu()
    selected_function = input('\n Using the list above, please enter the command character of the functionality you wish to apply to the image: ')
    if selected_function == 'o':
        open_image()

    elif selected_function == 'g':
        convert_to_grayscale()

    elif selected_function == '+':
        increase_brightness()

    elif selected_function == '-':
        decrease_brightness()

    elif selected_function == 'c':
        improve_contrast()

    elif selected_function == 't':
        apply_thresholding()

    elif selected_function == 's':
        save_image()

    elif selected_function == 'e':
        print("\n The program is successfully terminated.")
        exit(0)

    else:
        messagebox.showerror("Invalid Action", "Invalid command character!" + 
                             " Please enter only one of the available command characters from the list.")