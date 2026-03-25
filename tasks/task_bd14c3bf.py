# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             angles=None, shapes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row starting positions of the boxes.
    bcols: The column starting positions of the boxes.
    angles: The angles of the boxes.
    shapes: The shapes of the boxes.
  """

  def randint(a, b, i):
    return common.randint(a, b if i else a)

  def get_wide(shape, angle, i):
    if shape == "A" and angle in [0, 2]: return randint(3, 5, i)
    if shape == "A" and angle in [1, 3]: return randint(4, 5, i)
    if shape == "C" and angle in [0, 2]: return randint(3, 5, i)
    if shape == "C" and angle in [1, 3]: return randint(2, 5, i)
    if shape == "H": return randint(3, 5, i)
    if shape == "L": return randint(2, 5, i)
    if shape == "O": return randint(3, 5, i)
    if shape == "P" and angle in [0, 2]: return 5
    if shape == "P" and angle in [1, 3]: return randint(2, 5, i)
    if shape == "Y" and angle in [0, 2]: return 2 * randint(1, 2, i) + 1
    if shape == "Y" and angle in [1, 3]: return randint(3, 5, i)
    if shape == "8" and angle in [0, 2]: return 5
    if shape == "8" and angle in [1, 3]: return randint(3, 5, i)
    return -1

  if size is None:
    size, num_boxes = common.randint(15, 20), 7
    if size >= 18: num_boxes = common.randint(8, 9)
    box_types = common.sample(["A", "C", "H", "L", "O", "P", "Y", "8"], 3)
    while True:
      shapes = common.choices(box_types, num_boxes)
      if shapes.count(shapes[0]) < num_boxes // 2: continue
      if len(set(shapes)) == len(box_types): break
    while True:
      angles = [common.randint(0, 3) for _ in range(num_boxes)]
      wides, talls = [], []
      for i, (shape, angle) in enumerate(zip(shapes, angles)):
        wides.append(get_wide(shape, angle, i))
        talls.append(get_wide(shape, 3 - angle, i))
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      brows[0] = bcols[0] = 0
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    shapes = "".join(shapes)

  grid, output = common.grids(size, size)
  def get_mid(bcol, wide, brow, tall, angle):
    if angle == 0: return brow + (tall - 1) // 2
    if angle == 1: return bcol + wide // 2
    if angle == 2: return brow + tall // 2
    if angle == 3: return bcol + (wide - 1) // 2
    return -1
  def draw_a(g, wide, tall, brow, bcol, angle, color):
    mid = get_mid(bcol, wide, brow, tall, angle)
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    if angle == 0: wide, tall, brow, bcol = wide - 2, tall - 1, brow, bcol + 1
    if angle == 1: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol + 1
    if angle == 2: wide, tall, brow, bcol = wide - 2, tall - 1, brow + 1, bcol + 1
    if angle == 3: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol
    common.rect(g, wide, tall, brow, bcol, 0)
    if angle in [0, 2]:
      for col in range(bcol, bcol + wide):
        g[mid][col] = color
    else:
      for row in range(brow, brow + tall):
        g[row][mid] = color
  def draw_c(g, wide, tall, brow, bcol, angle, color):
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    if angle == 0: wide, tall, brow, bcol = wide - 2, tall - 1, brow, bcol + 1
    if angle == 1: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol + 1
    if angle == 2: wide, tall, brow, bcol = wide - 2, tall - 1, brow + 1, bcol + 1
    if angle == 3: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol
    common.rect(g, wide, tall, brow, bcol, 0)
  def draw_h(g, wide, tall, brow, bcol, angle, color):
    mid = get_mid(bcol, wide, brow, tall, angle)
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    if angle == 0: wide, tall, brow, bcol = wide - 2, tall, brow, bcol + 1
    if angle == 1: wide, tall, brow, bcol = wide, tall - 2, brow + 1, bcol
    if angle == 2: wide, tall, brow, bcol = wide - 2, tall, brow, bcol + 1
    if angle == 3: wide, tall, brow, bcol = wide, tall - 2, brow + 1, bcol
    common.rect(g, wide, tall, brow, bcol, 0)
    if angle in [0, 2]:
      for col in range(bcol, bcol + wide):
        g[mid][col] = color
    else:
      for row in range(brow, brow + tall):
        g[row][mid] = color
  def draw_l(g, wide, tall, brow, bcol, angle, color):
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    wide, tall = wide - 1, tall - 1
    if angle == 0: brow = brow + 1
    if angle == 1: bcol = bcol + 1
    if angle == 2: brow, bcol = brow + 1, bcol + 1
    common.rect(g, wide, tall, brow, bcol, 0)
  def draw_o(g, wide, tall, brow, bcol, color):
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    common.rect(g, wide - 2, tall - 2, brow + 1, bcol + 1, 0)
  def draw_p(g, wide, tall, brow, bcol, angle, color):
    if angle in [0, 2]:
      for row in range(brow, brow + tall):
        g[row][bcol + 1] = g[row][bcol + 3] = color
    else:
      for col in range(bcol, bcol + wide):
        g[brow + 1][col] = g[brow + 3][col] = color
    if angle == 0:
      for col in range(bcol, bcol + wide):
        g[brow + tall - 1][col] = color
    if angle == 1:
      for row in range(brow, brow + tall):
        g[row][bcol] = color
    if angle == 2:
      for col in range(bcol, bcol + wide):
        g[brow][col] = color
    if angle == 3:
      for row in range(brow, brow + tall):
        g[row][bcol + wide - 1] = color
  def draw_y(g, wide, tall, brow, bcol, angle, color):
    if angle in [0, 2]:
      for row in range(brow, brow + tall):
        g[row][bcol + wide // 2] = color
    else:
      for col in range(bcol, bcol + wide):
        g[brow + tall // 2][col] = color
    if angle == 0: tall = tall - (tall - 1) // 2
    if angle == 1: wide, bcol = wide - (wide - 1) // 2, bcol + (wide - 1) // 2
    if angle == 2: tall, brow = tall - (tall - 1) // 2, brow + (tall - 1) // 2
    if angle == 3: wide = wide - (wide - 1) // 2
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    if angle == 0: wide, tall, brow, bcol = wide - 2, tall - 1, brow, bcol + 1
    if angle == 1: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol + 1
    if angle == 2: wide, tall, brow, bcol = wide - 2, tall - 1, brow + 1, bcol + 1
    if angle == 3: wide, tall, brow, bcol = wide - 1, tall - 2, brow + 1, bcol
    common.rect(g, wide, tall, brow, bcol, 0)
  def draw_8(g, wide, tall, brow, bcol, angle, color):
    common.hollow_rect(g, wide, tall, brow, bcol, color)
    if angle in [0, 2]:
      for row in range(brow, brow + tall):
        g[row][bcol + wide // 2] = color
    else:
      for col in range(bcol, bcol + wide):
        g[brow + tall // 2][col] = color
  for i, (wide, tall, brow, bcol, angle, shape) in enumerate(zip(wides, talls, brows, bcols, angles, shapes)):
    color = 1 if i else 2
    if shape == "A": draw_a(grid, wide, tall, brow, bcol, angle, color)
    if shape == "C": draw_c(grid, wide, tall, brow, bcol, angle, color)
    if shape == "H": draw_h(grid, wide, tall, brow, bcol, angle, color)
    if shape == "L": draw_l(grid, wide, tall, brow, bcol, angle, color)
    if shape == "O": draw_o(grid, wide, tall, brow, bcol, color)
    if shape == "P": draw_p(grid, wide, tall, brow, bcol, angle, color)
    if shape == "Y": draw_y(grid, wide, tall, brow, bcol, angle, color)
    if shape == "8": draw_8(grid, wide, tall, brow, bcol, angle, color)
    color = 1 if shapes[i] != shapes[0] else 2
    if shape == "A": draw_a(output, wide, tall, brow, bcol, angle, color)
    if shape == "C": draw_c(output, wide, tall, brow, bcol, angle, color)
    if shape == "H": draw_h(output, wide, tall, brow, bcol, angle, color)
    if shape == "L": draw_l(output, wide, tall, brow, bcol, angle, color)
    if shape == "O": draw_o(output, wide, tall, brow, bcol, color)
    if shape == "P": draw_p(output, wide, tall, brow, bcol, angle, color)
    if shape == "Y": draw_y(output, wide, tall, brow, bcol, angle, color)
    if shape == "8": draw_8(output, wide, tall, brow, bcol, angle, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=18, wides=[3, 3, 5, 4, 7, 4, 4, 3],
               talls=[3, 3, 3, 3, 4, 3, 5, 3],
               brows=[0, 0, 3, 6, 8, 12, 13, 14],
               bcols=[0, 13, 5, 11, 0, 9, 14, 2],
               angles=[0, 0, 1, 1, 1, 0, 1, 2], shapes="HHHYHHPC"),
      generate(size=15, wides=[3, 3, 3, 3, 3, 4, 4],
               talls=[3, 4, 4, 3, 4, 4, 3], brows=[0, 1, 1, 5, 6, 8, 12],
               bcols=[0, 8, 12, 1, 5, 10, 1], angles=[1, 2, 0, 0, 2, 3, 3],
               shapes="CCHCHCA"),
      generate(size=18, wides=[3, 3, 3, 3, 4, 3, 3, 4, 4],
               talls=[3, 3, 4, 3, 3, 2, 3, 4, 4],
               brows=[0, 0, 3, 4, 8, 9, 9, 13, 14],
               bcols=[0, 13, 8, 2, 1, 8, 14, 4, 10],
               angles=[0, 0, 0, 3, 0, 2, 0, 0, 0], shapes="OHOCOCOOH"),
  ]
  test = [
      generate(size=19, wides=[5, 3, 3, 4, 3, 4, 3, 5, 5],
               talls=[3, 3, 4, 4, 5, 3, 4, 5, 4],
               brows=[0, 1, 1, 5, 7, 7, 13, 13, 14],
               bcols=[0, 8, 15, 1, 7, 12, 8, 12, 1],
               angles=[0, 0, 2, 3, 1, 3, 0, 1, 0], shapes="8OHC8CO88"),
  ]
  return {"train": train, "test": test}
