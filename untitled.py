from tkinter import StringVar, image_names
from numpy.lib.type_check import imag
import scipy.fftpack
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
from tkinter import messagebox


class ImageClass:
    no_imgs = 0
    ref_width = 0
    ref_height =0 
    def __init__(self):
        self.no_imgs = ImageClass.no_imgs
        ImageClass.no_imgs +=1
        print('no is ',self.no_imgs)


    def load_image(self):
        if self.no_imgs ==0:
            filename = askopenfilename()
            print('laa')
        else:
            filename = askopenfilename()
            temp = Image.open(filename)
            while temp.size[0] != ImageClass.ref_width and temp.size[1] !=ImageClass.ref_height:
                print('aloo')
                print(temp.size[0])
                print(ImageClass.ref_width)
                messagebox.showerror("Size Error!","Please select images of tha same size.")
                filename = askopenfilename()
                temp = Image.open(filename)
        self.image_data = Image.open(filename)
        self.width,self.height = self.image_data.size
        ImageClass.ref_height = self.height
        ImageClass.ref_width = self.width
        self.image_data = np.asarray(self.image_data)
        self.gray_image = np.mean(self.image_data,axis=2)
        return self.gray_image

    def select_component(self,component):
        self.img_fft = scipy.fftpack.fftshift(scipy.fftpack.fft2(self.image_data))
        self.img_mag = np.abs(self.img_fft) # khod el log hena 3lshan haga tezhar
        self.img_phase = np.angle(self.img_fft)
        if component == 'Mag':
            self.img_display = np.log(self.img_mag)
        elif component == "Phase":
            self.img_display = self.img_phase
        elif component == "Real":
            self.img_display = Image.fromarray(self.img_fft.real)
        elif component == "Imag":
            self.img_display = Image.fromarray(self.img_fft.imag) 
        return self.img_display


    def mixer(self, img1,selected_component,slider_value):
        slider_value = slider_value/100
        out_img = self.gray_image + img1.gray_image
        output_img = scipy.fftpack.fftshift(scipy.fftpack.fft2(out_img))
        if selected_component == "Mag":
            self.reconst_img_fft = output_img - (1-slider_value)*self.img_mag
        elif selected_component == "Phase":
            self.reconst_img_fft = output_img - (1-slider_value)*self.img_phase
        elif selected_component == "Real":
            self.reconst_img_fft = output_img - (1-slider_value)*self.img_fft.real

        elif selected_component == "Imag":
            self.reconst_img_fft = output_img - (1-slider_value)*self.img_fft.imag

        elif selected_component == "UniMag":
            reconst_img_fft = np.dot(1, 1j * output_img.imag)

        elif selected_component == "UniPhase":
            reconst_img_fft = np.dot(output_img.real, 1)
        reconst_img = scipy.fftpack.ifft2(scipy.fftpack.fftshift(reconst_img_fft)).real
        reconst_img = Image.fromarray(reconst_img)
        return reconst_img



image1 = ImageClass()
image2 = ImageClass()
image1.load_image()
image2.load_image()
x = image1.select_component()
y = image2.select_component()
print('x is ',x)
print('y is ',y)