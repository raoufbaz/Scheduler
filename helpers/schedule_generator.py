from PIL import Image, ImageDraw, ImageFont
import base64
import io

# Set the dimensions of the main rectangle
main_width = 875
main_height = 500

left_margin = 40
bottom_margin = 10

# Create a new image with white background
image = Image.new("RGB", (main_width, main_height), (248, 249, 250))
# Draw smaller rectangles side by side and add labels
draw = ImageDraw.Draw(image)
system_font_name = "Arial"

try:
    font = ImageFont.truetype(f"{system_font_name}.ttf", 12)
except IOError:
    # If the system font file doesn't exist, use a fallback font
    font = ImageFont.load_default()

days_position = {
        "lun": {"left": 40, "right": 145},
        "mar": {"left": 160, "right": 265},
        "mer": {"left": 280, "right": 385},
        "jeu": {"left": 400, "right": 505},
        "ven": {"left": 520, "right": 625},
        "sam": {"left": 640, "right": 745},
        "dim": {"left": 760, "right": 865}
    }
hours_position = {
        "8:00": 40, "8:30": 55,
        "9:00": 70, "9:30": 85,
        "10:00": 100, "10:30": 115,
        "11:00": 130, "11:30": 145,
        "12:00": 160, "12:30": 175,
        "13:00": 190, "13:30": 205,
        "14:00": 220, "14:30": 235,
        "15:00": 250, "15:30": 265,
        "16:00": 280, "16:30": 295,
        "17:00": 310, "17:30": 325,
        "18:00": 340, "18:30": 355,
        "19:00": 370, "19:30": 385,
        "20:00": 400, "20:30": 415,
        "21:00": 430, "21:30": 445,
        "22:00": 460, "22:30": 475,
        "23:00": 490
    }
colors = {
        # https://colorizer.org/
        "red": {"fill": (204, 46, 46), "shadow": (162, 37, 37)},
        "green": {"fill": (96, 204, 109), "shadow": (37, 162, 87)},
        "blue": {"fill": (3, 140, 252), "shadow": (2, 91, 181)},
        "purple": {"fill": (98, 3, 252), "shadow": (51, 1, 131)},
        "yellow": {"fill": (204, 145, 25), "shadow": (127, 90, 16)},
        "pink": {"fill": (161, 54, 169), "shadow": (100, 33, 104)},
        }


# saves the baseline image used to generate schedules from
def draw_base_template():
    # Set the dimensions of each smaller rectangle
    small_width = (main_width - left_margin) // 7
    small_height = main_height - bottom_margin
    days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi",
                    "Samedi", "Dimanche"]
    # Draws the rectangles for the days of the week
    for i in range(7):
        draw.rectangle((days_position["dim"]["left"], 40,
                        days_position["dim"]["right"], 490),
                       fill=(227, 231, 232))
        # Calculate the coordinates for each smaller rectangle
        left = left_margin + i * small_width

        # Add the day of the week label
        label = days_of_week[i]
        label_width = draw.textlength(label, font=font)
        label_x = (left + (small_width - label_width) // 2)-15
        label_y = 5  # Adjust label position as needed
        draw.text((label_x, label_y), label, font=ImageFont.
                  truetype("arial.ttf", 17), fill=(64, 64, 64))

    hours_of_day = list(range(8, 24))  # Hours from 8 to 23
    label_y_hour = left_margin  # Initial y-coordinate for the first label
    distance = (small_height - label_y_hour) // 15

    # Draws the hours of the day and the horizontal lines
    for j in range(16):
        if j < 2:
            label_hour = "0"+str(hours_of_day[j])+":00"
        else:
            label_hour = str(hours_of_day[j])+":00"
        label_x_hour = 5  # Adjust label position as needed
        draw.text((label_x_hour, label_y_hour-5), label_hour, font=font,
                  fill=(64, 64, 64), align="left")  # Dark grey

        if j == 0:
            color = "red"
            line_width = 2
        else:
            color = "black"
            line_width = 1
        draw.line([(40, label_y_hour), (main_width-10, label_y_hour)],
                  fill=color, width=line_width)
        # Draw the dashed line using a custom line style
        line_y = label_y_hour + (distance // 2)
        dash_length = 5  # Adjust the length of each dash
        space_length = 5  # Adjust the length of each space between dashes
        dashes = [(x, x + dash_length) for x in
                  range(40, main_width - 10, dash_length + space_length)]
        for dash_start, dash_end in dashes:
            draw.line([(dash_start, line_y), (dash_end, line_y)],
                      fill="grey", width=1)

        label_y_hour += distance

    # Save the image
    image.save("static/images/schedule_template.png")


# generates the course on the schedule depending on given parameters
def draw_course_rectangle(day, name, start_time, end_time, color, draw):
    left = days_position[day]["left"]
    right = days_position[day]["right"]
    top = hours_position[start_time]
    bottom = hours_position[end_time]
    shadow_pos = (left, bottom - 5, right, bottom)

    rounded_radius = 5  # Radius for rounded corners

    # Draw the rounded rectangle on the image
    draw.rounded_rectangle((left, top, right, bottom), rounded_radius,
                           fill=colors[color]["fill"])
    # shadow rectangle
    draw.rounded_rectangle(shadow_pos, rounded_radius,
                           fill=colors[color]["shadow"])
    # hour label
    text_position = (left+5, top+2)  # Text position (left, top)
    text_font = ImageFont.truetype("arial.ttf", 12)
    draw.text(text_position, start_time+" - "+end_time, fill="white",
              font=text_font)

    # name label
    text_position = (left+5, top+15)  # Text position (left, top)
    text_font = ImageFont.truetype("arial.ttf", 12)
    draw.text(text_position, name, fill="white", font=text_font)

    # uncomment to save the image in png format
    # image.save("static/images/schedule_template.png")


color_assignments = {}


def assignColor(name):
    if name in color_assignments:
        return color_assignments[name]
    else:
        # Assign a color dynamically (you can use any method to assign colors)
        available_colors = ["red", "blue", "green", "purple", "yellow"]
        for color in available_colors:
            if color not in color_assignments.values():
                color_assignments[name] = color
                return color
        # If all colors are assigned, return a default color or raise an error
        return "pink"


def resetColorAssignments():
    color_assignments.clear()


# draws the courses on the baseline image.
# Requires 5 params (day, name, start_hour, end_hour, color)
def draw_courses(courses, draw):
    for course in courses:
        day, name, start_hour, end_hour = course
        draw_course_rectangle(day, name, start_hour, end_hour,
                              assignColor(name), draw)


# Generate the schedule image and return it as base64 encoded PNG
def generate_for_frontend(combinaison):
    images = []  # Initialize an empty list to store the images
    template_path = "static/images/schedule_template.png"

    for comb in combinaison:
        resetColorAssignments()
        combined_image = Image.open(template_path).copy()
        draw = ImageDraw.Draw(combined_image)
        for course in comb:
            draw_courses([course], draw)

            img_byte_array = io.BytesIO()
            combined_image.save(img_byte_array, format="PNG")
            img_byte_array.seek(0)
            base64_image = base64.b64encode(img_byte_array.read()).decode()
        images.append(base64_image)  # Add the base64 image to the list of imgs

    return images  # Return the list of base64-encoded images


# Example usage:
courses_data = [
    ("lun", "GTI525", "18:00", "20:00", "red"),
    ("mer", "GTI525", "18:00", "21:30", "red"),
    ("mar", "GTI611", "8:30", "11:30", "green"),
    ("ven", "GTI611", "8:30", "12:00", "green"),
    ("mer", "LOG635", "8:30", "12:00", "blue"),
    ("ven", "LOG635", "13:30", "17:00", "blue"),
    ("lun", "PHY335", "13:30", "17:00", "purple"),
    ("jeu", "PHY335", "13:30", "17:00", "purple")
]

# draw_courses(courses_data)
draw_base_template()
