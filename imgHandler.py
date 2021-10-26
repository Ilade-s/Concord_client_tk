"""
Handlers pour le support de l'envoi d'image
Permettent la conversion d'une image en texte pour son envoi par le réseau ainsi que ça reconversion à l'arrivée
"""

import os
from PIL import Image # Gestion d'image
import csv

def convert_image(path_to_file: str, quality_factor: int, path_to_csv_folder: str, pixel_per_motif=1) -> tuple[str, str]:
    """
    Compress the image at path_to_file with the given quality_factor at the colors, then returns the text conversion that can be saved as CSV
    Returns a tuple with the path to the image and the path to the motif

    PARAMETERS :
        - path_to_file : str
            - path of the original image (most format are supported, refer to the pillow docs for more infos)
        - quality_factor : int
            - number which will be used to divide the color bands, as such, must be chosen between 256 and 1 (included)
            - 8 is recommended for best results and speed
            - higher is faster and lighter but less precise, lower is slower and heavier but better quality
        - pixel_per_motif: int
            - used when converting to csv, higher means a lighter convert.csv file, but slower conversion
            - 1 is recommended for best speed (it is the default)
        - path_to_csv_folder : str
            - path for the conversion folder, with convert.csv and motifs.csv
    """
    assert path_to_file, "the path to the orginal image is empty"
    assert 1 <= quality_factor <= 256, "quality factor is invalid : must be contained within [1;256]"

    motifs_path = path_to_csv_folder + 'motifs.csv'

    def create_colors(colors_used: list[tuple[int, int, int]], ecart_colors: int) -> list[tuple[int, int, int]]:
        """
        Renvoie les couleurs utiles pour l'image avec l'écart souhaité (qualité souhaitée)
        """
        colors = [
            get_nearest_color(color, ecart_colors)
            for color in colors_used
        ]

        return list(set(colors))

    def create_motifs(colors: list[tuple[int, int, int]], n_pixels: int) -> list[tuple[tuple[int, int, int]]]:
        """
        create all possible motifs from the colors, with the pixel per motifs according to pixel_per_motif

        PARAMETERS :
            - colors : list[tuple[int, int, int]]
                - list of all the colors used to create the motifs
            - n_pixels : int
                - equal to pixel_per_motif by default, doesn't need to be motified in normal conditions
        
        RETURN :
            - motifs : list[tuple[tuple[int, int, int]]]
                - list of all the motifs possible with the given colors in {n_pixels}-tuple
        """
        motifs = []
        if n_pixels == 1:
            for c1 in colors:
                motifs.append((c1,)) 

        elif n_pixels == 2:
            for c1 in colors:
                for c2 in colors:  
                    motifs.append((c1, c2)) 

        elif n_pixels == 3:
            for c1 in colors:
                for c2 in colors:  
                    for c3 in colors:
                        motifs.append((c1, c2, c3)) 

        return motifs   

    def save_motifs(motifs: list[tuple[tuple[int, int, int]]], save_path=motifs_path) -> None:
        """
        Saves the motifs in hexadecimal
        """
        hexMotifs = [
            [
                ''.join([hex(band)[2:].zfill(2) for band in color])
                for color in motif
            ]
            for motif in motifs
        ]
        with open(save_path, "w+", newline='\n') as file:
            w = csv.writer(file)
            w.writerows(hexMotifs)

    def get_nearest_color(color: tuple[int, int, int], quality_factor: int) -> tuple[int, int, int]:
        """
        Donne la couleur simplifiée la plus proche de la couleur donnée

        PARAMETRES :
            - color : tuple[int, int, int]
                - couleur à simplifier
            - quality_factor : int
                - facteur de division des bandes de couleurs RGB
        SORTIE :
            - color : tuple[int, int, int]
                - couleur identifiée
        """
        nearest_color = [round(band / quality_factor) * quality_factor for band in color]
        nearest_color = [255 if band == 256 else band for band in nearest_color]
        
        return tuple(nearest_color)

    img = Image.open(path_to_file)
    img = img.convert('RGB')
    (xImg, yImg) = img.size
    print(f"Taille image : {xImg}x{yImg}")

    colors_used = list(set([e[1] for e in img.getcolors(2**24)]))
    colors_used = create_colors(colors_used, quality_factor)
    dict_nearest_colors = {} # contains all results from get_nearest_color() et optimise image creation when pixels have the same color
    simplifiedImage = [[] for _ in range(yImg)]
    for y in range(yImg):
        for x in range(xImg//pixel_per_motif):
            tmp_list = []
            for i in range(pixel_per_motif):
                pixel = img.getpixel((x*pixel_per_motif+i, y))
                if pixel in dict_nearest_colors.keys(): # there is already a result
                    tmp_list.append(dict_nearest_colors[pixel])
                else: # first time seeing this color
                    nearest_pixel_color = get_nearest_color(pixel, quality_factor)
                    dict_nearest_colors[pixel] = nearest_pixel_color
                    tmp_list.append(nearest_pixel_color)
            simplifiedImage[y].append(tuple(tmp_list))

    motifs = create_motifs(colors_used, pixel_per_motif)    
    save_motifs(motifs)
    convertedImage = []
    for line in simplifiedImage:
        current_line = []
        n_same_motif = 1
        line_next = line[1:] + [tuple()]
        for motif, next_motif in zip(line, line_next):
            if motif != next_motif:
                if n_same_motif > 1:
                    current_line.append(f'{hex(motifs.index(motif))[2:]}-{hex(n_same_motif)[2:]}')
                else:
                    current_line.append(hex(motifs.index(motif))[2:])
                n_same_motif = 1
            else:
                n_same_motif += 1
        convertedImage.append(current_line)
    
    savePath = path_to_csv_folder + 'convert.csv'
    
    with open(savePath, "w+", newline='\n') as convertFile:
        w = csv.writer(convertFile)
        w.writerows(convertedImage)
    
    return savePath, motifs_path

def get_lines(csv_path):
    """
    Yields the lines of the csv to be sent through the network
    """
    with open(csv_path, 'r', newline='\n') as file:
        reader = csv.reader(file)
        for line in reader:
            yield line

def get_motifs(motifs_path):
    """
    Yields the motifs to be sent through the network (the motifs are lists with only one string in it which represents the motif)
    """
    with open(motifs_path, 'r', newline='\n') as file:
        reader = csv.reader(file)
        for line in reader:
            yield line
    
def get_len_img(path) -> int:
    img = Image.open(path)
    (x, len) = img.size
    return len

def make_img_path(name) -> str:
    """returns the complete path for the image"""
    return f'img/{name}/img.png'

class ImgReceiving:

    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size
        self.received_lines = 0
        self.conversion = []
        self.motifs = []
        self.folder = f'img/{self.name}/'
    
    def add_line(self, line: str) -> None:
        self.conversion.append(line.split(','))
    
    def add_motif(self, motif: str) -> None:
        self.motifs.append([motif])
    
    def save_motifs(self):
        if not os.path.exists(self.folder): os.mkdir(self.folder)
        with open(self.folder + 'motifs.csv', "w+", newline='\n') as file:
            w = csv.writer(file)
            w.writerows(self.motifs)
    
    def save_conversion(self):
        if not os.path.exists(self.folder): os.mkdir(self.folder)
        with open(self.folder + 'convert.csv', "w+", newline='\n') as convertFile:
            w = csv.writer(convertFile)
            w.writerows(self.conversion)

    def retrieve_img_from_CSV(self):
        """
        MUST BE CALLED ONLY AFTER save_motifs AND save_conversion
        ------------
        Transform the convert.csv, with motifs.csv, in self.folder in a image, then save it in self.folder at img.png

        PARAMETERS :
            - PathToCsv : str
                - path to the csv file representing the compressed image, obtained with img_compressor.py
            - SavePath : str
                - path which will be used to save the recreated/compressed image
            - motifsPath : str
                - motifs.csv by default, must be the same file used at creation in img_compressor.py
        """    
        pathToCsv = self.folder + 'convert.csv'
        savePath = self.folder + 'img.png'
        motifsPath = self.folder + 'motifs.csv'

        with open(pathToCsv, 'r', newline='\n') as file:
            reader = csv.reader(file)
            img_matrice = []
            for line in reader:
                current_line = []
                n_motifs_line = 0
                for e in line:
                    if len(e.split('-')) == 2:
                        (i_motif, n_motifs) = e.split('-')
                        n_motifs = int(n_motifs, 16)
                    else:
                        i_motif = e
                        n_motifs = 1
                    n_motifs_line += n_motifs
                    for _ in range(n_motifs):
                        current_line.append(int(i_motif, 16))
                img_matrice.append(current_line)

        with open(motifsPath, 'r', newline='\n') as file:
            reader = csv.reader(file)
            hexMotifs = [*reader]
            motifs = [
                tuple([
                    (
                    int(hexa[:2], 16),
                    int(hexa[2:4], 16),
                    int(hexa[4:], 16),
                    )
                    for hexa in motif
                ])   
                for motif in hexMotifs
            ]
            img_data_matrice = [[] for _ in range(len(img_matrice))]
            current_line = 0
            for line in img_matrice:
                for nMotif in line:
                    img_data_matrice[current_line].extend([*motifs[nMotif]])
                current_line += 1

        img = Image.new('RGB', (len(img_data_matrice[0]), len(img_data_matrice)))

        for line in range(len(img_data_matrice)):
            for col in range(len(img_data_matrice[0])):
                img.putpixel((col, line), img_data_matrice[line][col])

        img.save(savePath)
    



if __name__ == '__main__':
    pass