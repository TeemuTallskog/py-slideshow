import pygame
import sys
import glob
import os
import argparse
from PIL import Image, ExifTags
from random import shuffle

class Display:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Divide resolution into squares based on xy string.')
        parser.add_argument('-grid', type=self.validate_xy_string, help='XY string in the format "X_axisxY_axis" (e.g., "3x2").', default='2x2')
        parser.add_argument('-path', type=str, required=True, nargs='+', help="Path/paths to a folder containing images ex. ( -path <path/to/folder/> <c:/path/to/folder/> ... )")
        parser.add_argument('-speed', type=float, help="Speed in seconds at which a new image gets added to display (e.g. -speed 2 or -speed 0.5 )", default=2)
        parser.add_argument('-fill', action='store_true', help="Ignore image aspect ratio and strech fill squares.")
        parser.add_argument('-background', '--background-color', type=self.validate_rgb, help="Choose backgroud color with an rgb string RED,GREEN,BLUE (e.g., 255,255,255 #White 0,0,0 #Black)", default="0,0,0")
        parser.add_argument('-border', nargs='?', type=self.validate_rgb, const=(255,255,255), help="Draw images with a border, optinally pass rgb value (e.g. -border | -border 0,0,0 )")
        parser.add_argument('-border-width', type=int, help="Set border width, positive integer.", default=5)
        parser.add_argument('-gap', type=int, help="Pixels. Set a pixel gap between images", default=0)
        parser.add_argument('-shuffle', action="store_true", help="Display images in random order.")
        args = parser.parse_args()
        self.speed = args.speed
        self.image_paths = [img_path for dir_path in args.path for img_path in self.get_image_paths(dir_path)]
        if args.shuffle:
            shuffle(self.image_paths)
        self.border = args.border
        self.border_width = args.border_width
        self.gap = args.gap

        pygame.init()
        self.fill = args.fill
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.squares = self.divide_resolution((self.screen_width, self.screen_height), args.grid)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Slideshow")
        self.backgroud_color = args.background_color

    def validate_rgb(self, rgb_string):
        parts = rgb_string.split(',')

        if len(parts) != 3:
            raise argparse.ArgumentTypeError(f"Invalid rbg format, please input 3 positive integers separated by commas (e.g., 128,70,128)")

        try:
            r, g, b = map(int, parts)
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                return (r,g,b)
            else:
                raise argparse.ArgumentTypeError(f"Invalid rbg format, please input 3 positive integers separated by commas (e.g., 128,70,128)")
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid rbg format, please input 3 positive integers separated by commas (e.g., 128,70,128)")

    def validate_xy_string(self, xy_string):
        parts = xy_string.split('x')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(f"Invalid format for xy_string: {xy_string}. Should be 'X_axisxY_axis' (e.g., '3x2').")
        try:
            x_axis = int(parts[0])
            y_axis = int(parts[1])
            if x_axis <= 0 or y_axis <= 0:
                raise argparse.ArgumentTypeError(f"Invalid values in xy_string: {xy_string}. Values must be greater than zero.")
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid values in xy_string: {xy_string}. Values must be integers.")
        return xy_string

    def get_image_paths(self, dir_path):
        image_extensions = ["*.jpg", "*.jpeg", "*.png"]
        image_paths = []

        for extension in image_extensions:
            image_paths.extend(glob.glob(os.path.join(dir_path, extension)))

        return image_paths

    def divide_resolution(self, resolution, xy_string):
        x_axis, y_axis = map(int, xy_string.split('x'))
        width, height = resolution

        x_size = (width - (x_axis - 1) * self.gap) // x_axis
        y_size = (height - (y_axis - 1) * self.gap) // y_axis

        squares = []
        for i in range(x_axis):
            for j in range(y_axis):
                left = i * x_size + i * self.gap
                right = (i + 1) * x_size + i * self.gap if i != x_axis - 1 else width
                top = j * y_size + j * self.gap
                bottom = (j + 1) * y_size + j * self.gap if j != y_axis - 1 else height
                squares.append((left, top, right, bottom))

        return squares

    def resize_with_pad(self, image, square):
        image_width, image_height = image.get_size()
        aspect_ratio= image_width / image_height
        square_width = abs(square[0] - square[2])
        square_height = abs(square[1] - square[3])

        if self.fill:
            if not self.border:
                return pygame.transform.scale(image, (square_width, square_height))
            scaled = pygame.transform.scale(image, ((square_width - self.border_width * 2), (square_height - self.border_width * 2)))
        elif (square_width / square_height) > aspect_ratio:
            if self.border:
                new_width = int((square_height - self.border_width * 2) * aspect_ratio)
                scaled = pygame.transform.scale(image, (new_width, (square_height - self.border_width * 2)))
            else:
                new_width = int(square_height * aspect_ratio)
                scaled = pygame.transform.scale(image, (new_width, square_height))
        elif (square_width / square_height) < aspect_ratio:
            if self.border:
                new_heigth = int((square_width - self.border_width * 2) / aspect_ratio)
                scaled = pygame.transform.scale(image, ((square_width - self.border_width * 2), new_heigth))
            else:
                new_heigth = int(square_width / aspect_ratio)
                scaled = pygame.transform.scale(image, (square_width, new_heigth))
        else:
            if self.border:
                scaled = pygame.transform.scale(image, ((square_width - self.border_width * 2), (square_height - self.border_width * 2)))
            else:
                scaled = pygame.transform.scale(image, (square_width, square_height))

        offset_x = (square_width - scaled.get_width()) // 2
        offset_y = (square_height - scaled.get_height()) // 2

        surface = pygame.Surface((square_width, square_height))
        surface.fill(self.backgroud_color)
        if self.border:
            pygame.draw.rect(surface, self.border, (offset_x - self.border_width, offset_y - self.border_width, (scaled.get_width() + self.border_width * 2), (scaled.get_height() + self.border_width * 2)))
        surface.blit(scaled, (offset_x, offset_y))
        return surface
    
    def process_image(self, image_path):
        image = Image.open(image_path)

        try:
            exif = image._getexif()
            if exif is not None:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break

                if orientation in exif:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
        except AttributeError:
            pass
        
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)


    def main(self):
        running = True
        self.screen.fill(self.backgroud_color)
        clock = pygame.time.Clock()
        image_index = 0
        square_index = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            try:
                image = self.resize_with_pad(self.process_image(self.image_paths[image_index]), self.squares[square_index])
                self.screen.blit(image, self.squares[square_index])
                if square_index < (len(self.squares) - 1):
                    square_index += 1
                else:
                    square_index = 0
            except Exception as e:
                if image_index < (len(self.image_paths) - 1):
                    image_index += 1
                else:
                    image_index = 0
                continue
            pygame.display.flip()
            clock.tick( 1 / self.speed )
            if image_index < (len(self.image_paths) - 1):
                image_index += 1
            else:
                image_index = 0
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    display = Display()
    display.main()


