from PIL import Image, ImageDraw, ImageFont


class generator():
    def __init__(self):
        # load in the fonts
        self.rubik = ImageFont.truetype(
            "./fonts/Rubik/static/Rubik-Regular.ttf", 36)
        self.rubik_med = ImageFont.truetype(
            "./fonts/Rubik/static/Rubik-Medium.ttf", 36)
        self.qsand = ImageFont.truetype(
            "./fonts/Quicksand/static/Quicksand-Medium.ttf", 60)
        # call the canvas generate method
        a4_canvas = self.gen_a4px()
        canvas = a4_canvas[0]
        a4 = a4_canvas[1]
        base = a4_canvas[2]
        # calling draw methods
        self.draw_grids(canvas)
        self.draw_major_coords(canvas)
        # sub_badge_coords = [(327, 320), (913, 905)]
        badge_coords = [[(183, 257), (1057, 1497)], 
                        [(1423, 257), (2297, 1497)], 
                        [(183, 2011), (1057, 3251)], 
                        [(1423, 2011), (2297, 3251)]]
        userdata = [("Dawit","Solomon","GUR/00000/12","Male","Engeneering","2nd year","Student",),
                    ("Tony","Doe","GUR/00010/12","Male","Construction","2nd year","Student",),
                    ("Deez","Ligma","GUR/01000/12","Male","Architecture","2nd year","Student",),
                    ("Gebresolomon","Hailemichael","GUR/07000/12","Male","Design","2nd year","Student",),
                    ]
        self.paste_badge_background(a4, badge_coords, [])
        self.write_data(canvas, badge_coords, userdata)
        # calling show and save methods
        self.show_a4(a4,base)
        self.save_a4(a4,base)

    def gen_a4px(self):
        # A4 standard size in pixels 2480,3508
        # halved : 1240,1754
        # 874,1240

        base = Image.new('RGBA', (2480, 3508), color=(255, 255, 255, 0))
        a4 = Image.new('RGBA', (2480, 3508), color=(255, 255, 255, 255))
        canvas = ImageDraw.Draw(a4)

        # canvas.text((10,60), "World", font=rubik, fill=(0,0,0,255))

        return canvas, a4,base

    def draw_grids(self, canvas):
        print('- draw grid system  -')
        print('Canvas param - ', canvas)
        for x in range(0, 3508, 200):
            canvas.line([(0, x), (2480, x)], fill=(
                0, 0, 0, 255), width=1, joint="curve")
            # print(x)
        for y in range(0, 3508, 200):
            canvas.line([(y, 0), (y, 3508)], fill=(
                0, 0, 0, 255), width=1, joint="curve")
            # print(y)

    def draw_major_coords(self, canvas):
        print('- draw major coords  -')
        print("Canvas param - ", canvas)
        # verticals
        canvas.line([(620, 0), (620, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(1860, 0), (1860, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(1240, 0), (1240, 3508)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        # horizontals
        canvas.line([(0, 877), (2480, 877)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(0, 1754), (2480, 1754)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        canvas.line([(0, 2631), (2480, 2631)], fill=(
            0, 0, 0, 255), width=3, joint="curve")
        pass

    def paste_badge_background(self, canvas, coord, data):
        print('- draw badge background  -')
        print('Canvas param -', canvas)
        print('Coord param -', coord)
        print('Data param -', data)
        
        for point in coord:
            print("Generating badge on : ", point)
            print("A : ", point[0])
            print("B : ", point[1])
            print("W : ", point[1][0]-point[0][0])
            print("H : ", point[1][1]-point[0][1])
            print('pasting badge background')
            print('pasting qr code ')
            print('pasting photo')
            canvas.paste(Image.open('./badge_bg.png'),point[0])


    def write_data(self, canvas, coord, data):
        print('- Write data operation    -')
        print('Canvas param -', canvas)
        print('Coord param -', coord)
        print('Data param -', data)
        i = 0 
        for point in coord:
            print("Generating badge on : ", point)
            print("A : ", point[0])
            print("B : ", point[1])
            print("W : ", point[1][0]-point[0][0])
            print("H : ", point[1][1]-point[0][1])

            print('Writing user data:')

            canvas.text((coord[i][0][0]+437,coord[i][0][1]+734),f"{data[i][0]} {data[i][1]}", font=self.qsand, fill=(0,0,0,255),anchor='ms')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+794),f"UID : {data[i][2]}", font=self.rubik_med, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+864),f"Gender : {data[i][3]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+934),f"Enrollment : {data[i][4]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+1004),f"Term : {data[i][5]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')
            canvas.text((coord[i][0][0]+60,coord[i][0][1]+1074),f"Access : {data[i][6]}", font=self.rubik, fill=(0,0,0,255),anchor='lt')

            i = i + 1

    def show_a4(self, a4,base):
        out = Image.alpha_composite(base, a4)
        print('--│ Previewing image ')
        out.show()

    def save_a4(self, a4,base):
        out = Image.alpha_composite(base, a4)
        print('--│ Saving image as heow.png')
        out.save('heow.png')

badge = generator()
