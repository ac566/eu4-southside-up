import math
import sys

# author: ac566
# date: 7/9/2018
# copyright: 2018
class flip_my_shit():
    def __init__(self, path_to_mod):
        # Fix Mod Path
        if path_to_mod[-1] == '/':
            self.mad_path = path_to_mod[0:len(path_to_mod)-2]
        else:
            self.mod_path = path_to_mod

        # Grab the Map File
        default_map_name = self.mod_path + '/map/default.map'
        default_map_file = open(default_map_name, 'r')
        lines = default_map_file.readlines()
        default_map_file.close()

        # Store Map Dimensions
        map_width = float(self.replace_multiple(lines[0].strip(),['width',' ','='],['','','']))
        map_height = float(self.replace_multiple(lines[1].strip(),['height',' ','='],['','','']))
        self.ox = map_width/2.0
        self.oy = map_height/2.0

        # Change map defualt map dimensions
        new_default_map_file = open(default_map_name+'.new', 'w')
        coord = self.flip(map_width, map_height)
        new_default_map_file.write('width = '+str(int(coord[0])))
        new_default_map_file.write('height = '+str(int(coord[1])))
        
        # Write the rest of the file
        i = 2
        while i < range(len(lines)):
            new_default_map_file.write(lines[i])
        new_default_map_file.close()

        # Save sine and cosine of PI for ease
        self.sinpi = math.sin(math.pi)
        self.cospi = math.cos(math.pi)

    def replace_multiple(self, string, array, replacements):
        for i in range(len(array)):
            string = string.replace(array[i],replacements[i])
        return string

    # For Rotations about a center point
    def rotate_180(self, pt):
        return round(pt+math.pi,3)

    # Rotating a point on the map
    def flip(self, px, py):
        ox = self.ox
        oy = self.oy
        xn = ox+self.cospi * (px-ox) - self.sinpi * (py-oy)
        yn = oy+self.sinpi * (px-ox) + self.cospi * (py-oy)

        return [round(xn,3), round(yn,3)]

    # TODO: this should flip the various images to complete a mod.
    def flip_images(self):
        return 0

    # Flips the file
    # param : file - file to parse
    # param : pos  - flipping positions
    # param : rot  - flipping rotations
    # param : con  - flipping control (for trade file)
    def flip_that_shit(self, file, pos=False, rot=False, con=False):
        # Open input file
        in_file = open(self.mod_path+file,'r')
        lines = in_file.readlines()
        in_file.close()

        # Open output file
        out_file = open(self.mod_path+file+'.new','w')

        # Zeros that are added to the end of a rotated point
        zeros = ''
        if pos or rot:
            zeros = '00 '
        else:
            zeros = '00000 '

        # Precision
        ep = 0.0000000005
        pi2 = math.pi * 2

        # Go over every line
        i = 0
        while i < len(lines):
            # Did we find a line worth flipping?
            if (pos and lines[i].find('position={') is not -1) or \
                    (rot and lines[i].find('rotation={') is not -1) or \
                    (con and lines[i].find('control={') is not -1 and lines[i].find('control={}') is -1):
                # YEP! Write the line
                #
                # base format is: position{
                #                     num1 num2 ... numN 
                #                 }
                out_file.write(lines[i])

                # Proceed to next line (the one to be flipped)
                i += 1
                position = lines[i].strip().split(' ')

                # Ignore commented lines
                if position[0][0] != '#':
                    new_position = ''

                    # Flip 2d points on the map
                    if pos or con: # position and control are 2d points on a map sized grid
                        j = 0
                        while j < len(position)-1:
                            new_coord = self.flip(float(position[j]),float(position[j+1]))
                            new_position += str(new_coord[0]) + zeros + str(new_coord[1]) + zeros
                            j += 2

                    # Flip 1d rotation value
                    elif rot: # Rotation values just add pi
                        j = 0
                        while j < len(position):
                            new_coord = self.rotate_180(float(position[j]))

                            # Fix rotation to range [0,2PI]
                            if new_coord > pi2-ep:
                                new_coord = round(new_coord-pi2,3)
                            elif new_coord > math.pi-ep and new_coord < math.pi+ep:
                                new_coord = 0.0

                            new_position += str(new_coord)
                            if len(str(abs(new_coord))) < 5:
                                new_position += zeros
                            else:
                                new_position += ' '

                            j += 1

                    # Extra tab for good luck
                    if con:
                        out_file.write('\t')

                    out_file.write('\t\t' + new_position + '\n')
                # It was commented, so just write the line
                else:
                    out_file.write(lines[i])
            # No match, write the line anyways
            else:
                out_file.write(lines[i])
            i += 1
        #  End While
        out_file.close()
        return 0

def main():
    # Create flippy buddy
    flipper = flip_my_shit(path_to_mod=str(sys.argv[1]))
    # Flip the rotations in positions file
    flipper.flip_that_shit(file='/map/positions.txt',rot=True)
    # Flip positions in positions file
    flipper.flip_that_shit(file='/map/positions.txt.original',pos=True)
    # Flip trade nodes file
    flipper.flip_that_shit(file='/common/tradenodes/00_tradenodes.txt.original',con=True)


if __name__ == '__main__':
    main()