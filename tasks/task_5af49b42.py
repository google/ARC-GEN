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


def generate(width=None, height=None, northwests=None, northeasts=None,
             southwests=None, southeasts=None, rows=None, cols=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    northwests: The colors of north-west corner cells.
    northeasts: The colors of north-east corner cells.
    southwests: The colors of south-west corner cells.
    southeasts: The colors of south-east corner cells.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  def draw():
    if len(set(colors)) != len(colors): return None, None  # All unique colors.
    grid, output = common.grids(width, height)
    # First, draw the legends in all the corners.
    for i, color in enumerate(northwests):
      output[0][i] = grid[0][i] = color
    for i, color in enumerate(northeasts):
      offset = width - len(northeasts)
      output[0][offset + i] = grid[0][offset + i] = color
    for i, color in enumerate(southwests):
      output[height - 1][i] = grid[height - 1][i] = color
    for i, color in enumerate(southeasts):
      offset = width - len(southeasts)
      output[height - 1][offset + i] = grid[height - 1][offset + i] = color
    # Second, draw the pixels, and infer which corners they belong to.
    for row, col, color in zip(rows, cols, colors):
      grid[row][col] = color
      angle_index = []
      if color in northwests: angle_index.append((northwests, northwests.index(color)))
      if color in northeasts: angle_index.append((northeasts, northeasts.index(color)))
      if color in southwests: angle_index.append((southwests, southwests.index(color)))
      if color in southeasts: angle_index.append((southeasts, southeasts.index(color)))
      if len(angle_index) != 1: return None, None
      angle, index = angle_index[0]
      c = col - index
      #  Don't overwrite a color, and don't be adjacent to a color.
      if common.get_pixel(output, row, c - 1) not in [-1, 0]:
        return None, None
      if common.get_pixel(output, row, c + len(angle)) not in [-1, 0]:
        return None, None
      for i, color in enumerate(angle):
        if common.get_pixel(output, row - 1, c + i) not in [-1, 0]:
          return None, None
        if common.get_pixel(output, row, c + i) not in [-1, 0]:
          return None, None
        if common.get_pixel(output, row + 1, c + i) not in [-1, 0]:
          return None, None
        common.draw(output, row, c + i, color)
    return grid, output

  if width is None:
    height = common.randint(12, 18)
    width = height + common.randint(0, 2)
    angles = common.sample([0, 1, 2, 3], common.randint(1, 3))
    while True:
      northwests, northeasts, southwests, southeasts = [], [], [], []
      if 0 in angles: northwests = common.random_colors(common.randint(3, 6))
      if 1 in angles: northeasts = common.random_colors(common.randint(3, 6))
      if 2 in angles: southwests = common.random_colors(common.randint(3, 6))
      if 3 in angles: southeasts = common.random_colors(common.randint(3, 6))
      num_points = common.randint(3, 6)
      point_angles = common.choices(angles, num_points)
      if len(set(point_angles)) != len(angles): continue
      rows = [common.randint(1, height - 2) for _ in range(num_points)]
      cols = [common.randint(0, width - 1) for _ in range(num_points)]
      colors = []
      for angle in point_angles:
        if angle == 0: colors.append(common.choice(northwests))
        if angle == 1: colors.append(common.choice(northeasts))
        if angle == 2: colors.append(common.choice(southwests))
        if angle == 3: colors.append(common.choice(southeasts))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=13, northwests=[], northeasts=[],
               southwests=[1, 2, 4, 3], southeasts=[5, 7, 8, 6],
               rows=[1, 2, 5, 8, 8], cols=[2, 11, 4, 2, 8],
               colors=[2, 8, 1, 6, 4]),
      generate(width=14, height=12, northwests=[], northeasts=[],
               southwests=[2, 3, 5, 1, 6, 4], southeasts=[], rows=[2, 5, 7],
               cols=[7, 2, 11], colors=[2, 1, 4]),
      generate(width=13, height=13, northwests=[], northeasts=[4, 3, 7, 8],
               southwests=[1, 6, 2], southeasts=[], rows=[2, 5, 8, 9],
               cols=[2, 6, 11, 1], colors=[1, 8, 2, 4]),
  ]
  test = [
      generate(width=18, height=17, northwests=[9, 5, 3, 4], northeasts=[],
               southwests=[2, 1, 3, 8], southeasts=[4, 5, 6, 7],
               rows=[1, 3, 5, 9, 11, 13], cols=[11, 3, 13, 7, 13, 4],
               colors=[8, 9, 6, 1, 2, 7]),
  ]
  return {"train": train, "test": test}
