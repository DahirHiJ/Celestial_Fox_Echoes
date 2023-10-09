#!/usr/bin/env python

from __future__ import division
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt
import cv2
import os
import wave
import struct
from scipy import signal
from sklearn.cluster import KMeans

class MusicalPicture(object):
    
    SAMPLE_RATE = 44100
    NUM_PITCHES = 7
    
    #          F      F#/Gb  G      G#/Ab  A      A#/Bb  B      C      C#/Db  D      D#/Eb  E
    PITCHES = [361.63, 393.66, 429.63, 449.23, 492.00, 540.00, 593.88]

    def __init__(self, filename, num_sections):
        print("Initializing image: {}\n......................".format(filename))
        self.image = cv2.imread(filename)
        print("Image loaded!")
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.num_sections = num_sections
        self.sections = self.generate_sections() # List of len num_sections
        self.dominant_colors = self.find_dominant_colors() # List of tuples, len num_sections (frequency, hue, saturation, value)
        self.hue_to_pitch = self.calculate_hue_to_pitch()
        self.pitches = self.calculate_pitches()

    def plot_colors(self, hist, centroids):
        """
        Plots the dominant colors previously generated into a histogram with centroids
        Modified from: https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
        """
        bar = np.zeros((50, 300, 3), dtype = "uint8")
        startX = 0
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                color.astype("uint8").tolist(), -1)
            startX = endX
    
        # return the bar chart
        return bar

    def generate_sections(self):
        """
        Divides the image into num_sections sections of even width, with the exception of the last section which includes the remainder. Ex:
            Image width: 100
            num_sections: 7
            First 6 sections width: 100//7
            Last section width: 100//7+100%7

        Args:
            None
        Returns:
            A list of 2d numpy arrays
        """
        sections = []
        section_size = self.width//self.num_sections
        for i in range(self.num_sections-1):
            new_section = self.image[:,i*section_size:(i+1)*section_size,:]
            sections.append(new_section)
        # The last section will likely be different width
        sections.append(self.image[:,(self.num_sections-1)*section_size:,:].astype(np.uint8))
        return sections

    
    def generate_single_wav(self, section_number):
        """
        Generates a wav file of a single period of a sound shaped by the value of the colors
        in a particular section of the image
        
        Args:
            section_number: the section of the image to sonify
        Returns:
            None
        """

        if section_number >= self.num_sections:
            raise IndexError("Invalid section number")
        section = self.sections[section_number]
        grayscale = cv2.cvtColor(section, cv2.COLOR_BGR2GRAY)
        grayscale = grayscale.reshape((grayscale.shape[0], grayscale.shape[1]))
        averaged = np.mean(grayscale, axis=1)
        averaged = np.add(averaged, -np.mean(averaged), casting="unsafe")
        averaged *= 256
        sampled = averaged
        #sampled = signal.resample(averaged.astype(np.float64), int(len(averaged)))#*3000/MusicalPicture.SAMPLE_RATE))
        sampled = np.tile(sampled, len(averaged))
        dir_name = "section_{}".format(section_number)

        try:
            # Create target Directory
            os.mkdir(dir_name)
            print("Directory {} created".format(dir_name))
        except OSError:
            pass
        output_wav = "{}/instrument.wav".format(dir_name)
        obj = wave.open(output_wav, 'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(MusicalPicture.SAMPLE_RATE)
        
        for i in range(len(sampled)):
            if(int(sampled[i])<=-32768 or int(sampled[i])>=32767):
                data_point = struct.pack('<h',0)
            else:
                data_point = struct.pack('<h', int(sampled[i]))
            obj.writeframesraw(data_point)
        obj.close()

    def generate_all_wavs(self):
        """
        Runs generate_single_wav on all sections of the image
        """
        for i in range(self.num_sections):
            self.generate_single_wav(i)


    def find_dominant_colors(self):
        """
        Finds the most dominant colors in each section of the image, and extracts the H, S,
        and V data
        Adapted from: https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
        Args:
            None
        Returns:
            A list of lenth num_sections of tuples, where each tuple value is a list of 
            the following:
                (color_frequency, hue, saturation, value)    
        """
        print("Searching for dominant colors...")
        section_results = []
        counter = 0
        for section in self.sections:
            print("Section {}: ".format(counter)),
            section = cv2.cvtColor(section, cv2.COLOR_BGR2HSV)
            #section = cv2.cvtColor(section, cv2.COLOR_BGR2RGB) 
            image = section.reshape((section.shape[0] * section.shape[1], 3)) # see if this can just be clustered by hue
            clt = KMeans(n_clusters = MusicalPicture.NUM_PITCHES)
            clt.fit(image)
            numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
            (hist, _) = np.histogram(clt.labels_, bins = numLabels)
            # normalize the histogram, such that it sums to one
            hist = hist.astype("float")
            hist /= hist.sum()

            frequencies = []
            hues = []
            saturations = []
            values = []
            for (percent, color) in zip(hist, clt.cluster_centers_):
                frequencies.append(percent)
                hues.append(color[0])
                saturations.append(color[1])
                values.append(color[2])

            section_results.append((frequencies, hues, saturations, values))
            bar = self.plot_colors(hist, clt.cluster_centers_)
            # show our color bart
            plt.figure()
            plt.axis("off")
            plt.imshow(bar)
            #plt.show()
            print("Colors found!")
            counter += 1
        return section_results

    def calculate_hue_to_pitch(self):
        """
        Generates a dictionary mapping hues from 0-180 (standard for OpenCV) to 1 octave of
        a western chromatic scale (in Hz)

        Args:
            None
        Returns:
            A dictionary mapping hue to pitch
        """
        hue_to_pitch = {}
        multiple = round(180/len(MusicalPicture.PITCHES), 1)
        for i in range(len(MusicalPicture.PITCHES)):
            hue_to_pitch[i*multiple] = MusicalPicture.PITCHES[i]
        return hue_to_pitch

    def closest_pitch(self, hue):
        """
        Given a hue, finds the closest western chromatic pitch associated with it

        Args:
            hue: the hue to be converted into a pitch
        Returns:
            The closest pitch
        """

        hues = list(self.hue_to_pitch.keys())
        # find the closest hue by minimizing squared error
        closest_ind = np.argmin((hues-hue)**2) # check the syntax on this
        return self.hue_to_pitch[hues[closest_ind]]
    
    def calculate_pitches(self):
        """
        For all of the hues for each section:
        Given a hue within the range 0-180 (standard for OpenCV), calculate a
        pitch (Hz), which is multiplied by 2 if the saturation is above 50.
        
        Resources: 
            - https://cycling74.com/forums/patch-for-pitch-to-color
            - https://www.flutopedia.com/sound_color.htm

        Args:
            None
        Returns:
            A list of length num_sections, of lists of pitches associated with each
            section
        """
        print("Calculating pitches...")
        pitches = []
        counter = 0
        for section in self.dominant_colors:
            print("Section {}: ".format(counter)),
            section_pitches = []
            for i in range(len(section[1])): # hues
                hue = section[1][i]
                saturation = section[2][i]
                central_pitch = self.closest_pitch(hue)
                if saturation > 50: # can modify to have more octave range
                    central_pitch *= 2
                section_pitches.append(central_pitch)
            pitches.append(section_pitches)
            counter += 1
            print("Complete!")
        return pitches

    def write_all_data(self):
        """
        Runs write_data for all sections
        """

        print("Writing data...")
        for i in range(self.num_sections):
            self.write_data(i)

    def write_data(self, section):
        """
        Generate a text file of pitch, frequency, saturation, and value data for a
        particular section in odot bundle format

        Args:
            section: The section number to convert to data
        Returns:
            None
        """

        print("Section {}: ".format(section)),
        if section >= self.num_sections:
            raise IndexError("Invalid section number")
        dir_name = "section_{}".format(section)
 
        try:
            # Create target Directory
            os.mkdir(dir_name)
            print("Directory " , dir_name ,  " Created ") 
        except OSError:
            pass
        
        filename = "{}/pitches.txt".format(dir_name)

        # output in odot bundle format
        output = "/pitches = " + str(self.pitches[section]) + "\n"
        output = output + "/weights = " + str(self.dominant_colors[section][0]) + "\n"
        output = output + "/saturations = " + str(self.dominant_colors[section][2]) + "\n"
        output = output + "/values = " + str(self.dominant_colors[section][3]) + "\n"
        with open(filename, 'w+') as f:
            f.write(output)
        print("Complete!")


if __name__ == "__main__":
    yay = MusicalPicture("C:\\Users\\Usuario\\Downloads\\sonifying-images-master\\sonifying-images-master\\hsv.png", 5)
    yay.generate_all_wavs()
    yay.write_all_data()
