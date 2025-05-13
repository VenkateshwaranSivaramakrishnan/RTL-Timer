import matplotlib.pyplot as plt
from PIL import Image
import textwrap
import os

def text_to_image(text_lines, out_path, width=120, fontsize=10):
    # Wrap each line if needed
    wrapped_text = "\n".join([line if len(line) <= width else "\n".join(textwrap.wrap(line, width)) for line in text_lines])
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.text(0, 1, wrapped_text, fontsize=fontsize, va='top', family='monospace')
    ax.axis('off')
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.2)
    plt.close()

def combine_images(left_img_path, right_img_path, out_path):
    img1 = Image.open(left_img_path)
    img2 = Image.open(right_img_path)

    h = max(img1.height, img2.height)
    w = img1.width + img2.width

    combined = Image.new("RGB", (w, h), color=(255, 255, 255))
    combined.paste(img1, (0, 0))
    combined.paste(img2, (img1.width, 0))
    combined.save(out_path)

# === TIMING REPORT ===
timing_report = """
****************************************
Report : timing
	-path_type full
	-delay_type max
	-nets
	-slack_lesser_than 10.000
	-max_paths 1000000
	-transition_time
	-capacitance
	-sort_by slack
Design : Rocket
Version: T-2022.03-SP1
Date   : Wed Sep 13 02:24:41 2023
****************************************


Startpoint: mem_ctrl_jalr_reg
               (rising edge-triggered flip-flop clocked by CLK_clock)
  Endpoint: wb_reg_wdata_reg_63_
               (rising edge-triggered flip-flop clocked by CLK_clock)
  Path Group: CLK_clock
  Path Type: max
  Max Data Paths Derating Factor  : 1.000
  Min Clock Paths Derating Factor : 1.000
  Max Clock Paths Derating Factor : 1.000

  Point                       Fanout    Cap      Trans       Incr       Path
  -----------------------------------------------------------------------------
  clock CLK_clock (rise edge)                    0.000      0.000      0.000
  clock network delay (ideal)                               0.000      0.000
  mem_ctrl_jalr_reg/CK (DFF_X1)                  0.000      0.000      0.000 r
  mem_ctrl_jalr_reg/QN (DFF_X1)                  0.021      0.076      0.076 r
  n22008 (net)                   4    6.699 
  U12079/ZN (AND2_X1)                            0.087      0.131      0.207 r
  n15792 (net)                  16   36.579 
  U16573/ZN (INV_X2)                             0.045      0.119      0.326 f
  n12705 (net)                  27   61.068 
  U12037/ZN (INV_X1)                             0.073      0.134      0.460 r
  n15744 (net)                  14   30.937 
  U16530/Z (MUX2_X1)                             0.024      0.092      0.553 r
  n15544 (net)                   4    8.618 
  U18039/ZN (NAND2_X1)                           0.014      0.040      0.593 f
  n17169 (net)                   2    4.527 
  U19679/ZN (XNOR2_X1)                           0.009      0.059      0.651 f
  n17170 (net)                   1    1.205 
  U12819/ZN (OR2_X1)                             0.011      0.062      0.714 f
  n17173 (net)                   2    3.821 
  U19680/ZN (INV_X1)                             0.008      0.028      0.742 r
  n17171 (net)                   1    2.036 
  U11829/ZN (AND2_X2)                            0.111      0.154      0.896 r
  n17282 (net)                  40   94.480 
  U11281/ZN (NAND2_X1)                           0.106      0.202      1.098 f
  n20596 (net)                  25   55.266 
  U24790/ZN (NAND4_X1)                           0.030      0.072      1.170 r
  n7625 (net)                    1    1.450 
  wb_reg_wdata_reg_63_/D (DFF_X1)                0.030      0.009      1.179 r
  data arrival time                                                    1.179

  clock CLK_clock (rise edge)                    0.000      0.500      0.500
  clock network delay (ideal)                               0.000      0.500
  clock reconvergence pessimism                             0.000      0.500
  clock uncertainty                                        -0.150      0.350
  wb_reg_wdata_reg_63_/CK (DFF_X1)                                     0.350 r
  library setup time                                       -0.037      0.313
  data required time                                                   0.313
  -----------------------------------------------------------------------------
  data required time                                                   0.313
  data arrival time                                                   -1.179
  -----------------------------------------------------------------------------
  slack (VIOLATED)                                                    -0.866
"""  # Replace this line with your actual report string

# === Split lines in half ===
lines = timing_report.strip().splitlines()
mid = len(lines) // 2
left_lines = lines[:mid]
right_lines = lines[mid:]

# === Generate individual images ===
text_to_image(left_lines, "left.png")
text_to_image(right_lines, "right.png")

# === Combine side by side ===
combine_images("left.png", "right.png", "timing_combined.png")

# === Cleanup ===
os.remove("left.png")
os.remove("right.png")

print("✅ Saved: timing_combined.png")
