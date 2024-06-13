# Py Slideshow
Full screen slide show of images written in python!
## Install
```bash
pip install pygame
git clone https://https://github.com/TeemuTallskog/py-slideshow.git
cd py-slideshow
python3 display.py
```

## Usage

### Commands:
  - ``-h``, ``--help``
    - Display commands and exit.
  - ``-grid GRID``      
    - XY string in the format "X_axisxY_axis" (e.g., "3x2").
  - ``-path PATH [PATH ...]``
    - Path/paths to a folder containing images ex. ( -path <path/to/folder/> <c:/path/to/folder/>
                        ... )
  - ``-speed SPEED``          
    - Speed in seconds at which a new image gets added to display (e.g. -speed 2 or -speed 0.5 )
  - ``-fill``
    - Ignore image aspect ratio and strech fill squares.
  - ``-background BACKGROUND_COLOR``, ``--background-color BACKGROUND_COLOR``
    - Choose backgroud color with an rgb string RED,GREEN,BLUE (e.g., 255,255,255 #White 0,0,0
                        #Black)
  - ``-border [BORDER]``
    - Draw images with a border, optinally pass rgb value (e.g. -border | -border 0,0,0 )
  - ``-border-width BORDER_WIDTH``
    - Set border width, positive integer. ``-border`` must be set in order for this to have an effect.
  - ``-gap GAP``              
    - Pixels. Set a pixel gap between images

To exit slide show you can press and hold the **ESCAPE** key
### Example:
```bash
python display.py -squares 4x6 -speed 2 -path ~/images/ /path/to/images/ -fill -gap 20 -border -border-width 10
```

## Limitations
If you are running this on a secondary monitor and the resolution doesn't match your main monitor, images will be out of alignment.  
This is a limitation with `pygame`.  
To bypass this switch your desired monitor as your main monitor.