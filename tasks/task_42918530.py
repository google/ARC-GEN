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


def generate(width=None, height=None, colors=None, prows=None, pcols=None,
             pcolors=None, bcolors=None, bidxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the grid.
    prows: The rows of the pattern.
    pcols: The columns of the pattern.
    pcolors: The colors of the pattern.
    bcolors: The colors of the input boxes.
    bidxs: The indices of the input boxes.
  """

  if width is None:
    width, height = common.randint(2, 4), common.randint(2, 4)
    while True:
      colors = [common.random_color() for _ in range(width * height)]
      superset = list(set(colors))
      subset = common.sample(superset, common.randint(1, len(superset)))
      counts = [colors.count(color) for color in subset]
      if max(counts) > 1: break  # At least one color must appear twice or more.
    prows, pcols, pcolors, bcolors, bidxs = [], [], [], [], []
    for color in subset:
      pixels = []
      for r in range(3):
        for c in range(3):
          pixels.append((r, c))
      pixels = common.sample(pixels, common.randint(1, 5))
      for r, c in pixels:
        prows.append(r)
        pcols.append(c)
        pcolors.append(color)
      num_boxes = colors.count(color)
      bcolors.append(color)
      bidxs.append(common.randint(0, num_boxes - 1))

  grid, output = common.grids(6 * width + 1, 6 * height + 1)
  for row in range(height):
    for col in range(width):
      color = colors[row * width + col]
      common.hollow_rect(grid, 5, 5, 6 * row + 1, 6 * col + 1, color)
      common.hollow_rect(output, 5, 5, 6 * row + 1, 6 * col + 1, color)
      for prow, pcol, pcolor in zip(prows, pcols, pcolors):
        if color != pcolor: continue
        output[6 * row + 2 + prow][6 * col + 2 + pcol] = pcolor
  for bcolor, bidx in zip(bcolors, bidxs):
    count = 0
    for row in range(height):
      for col in range(width):
        color = colors[row * width + col]
        if color != bcolor: continue
        if count == bidx:
          for prow, pcol, pcolor in zip(prows, pcols, pcolors):
            if color != pcolor: continue
            grid[6 * row + 2 + prow][6 * col + 2 + pcol] = pcolor
        count += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=4, colors=[2, 6, 2, 8, 3, 8, 6, 2, 4, 1, 5, 2],
               prows=[0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 2, 2],
               pcols=[1, 0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 1, 1, 1, 1, 0, 2],
               pcolors=[2, 2, 2, 2, 8, 8, 8, 3, 3, 3, 6, 6, 4, 1, 1, 1, 1],
               bcolors=[2, 8, 3, 6, 4, 1], bidxs=[0, 0, 0, 1, 0, 0]),
      generate(width=3, height=3, colors=[2, 4, 8, 8, 3, 1, 2, 1, 2],
               prows=[0, 1, 1, 1, 1, 1, 2], pcols=[1, 0, 1, 1, 1, 2, 1],
               pcolors=[2, 2, 2, 8, 3, 3, 3], bcolors=[2, 8, 3],
               bidxs=[0, 0, 0]),
      generate(width=3, height=3, colors=[3, 3, 2, 2, 8, 1, 8, 2, 1],
               prows=[1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2],
               pcols=[1, 0, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1],
               pcolors=[3, 8, 8, 8, 1, 1, 1, 2, 2, 2, 2, 2],
               bcolors=[3, 8, 1, 2], bidxs=[1, 0, 0, 2]),
      generate(width=3, height=2, colors=[3, 8, 4, 4, 2, 7],
               prows=[0, 1, 1, 1, 2], pcols=[1, 0, 1, 2, 1],
               pcolors=[4, 4, 4, 4, 4], bcolors=[4], bidxs=[0]),
  ]
  test = [
      generate(width=4, height=4,
               colors=[1, 8, 3, 7, 6, 2, 1, 2, 8, 4, 3, 2, 2, 8, 2, 6],
               prows=[1, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 1, 0, 1, 1, 2],
               pcols=[0, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1],
               pcolors=[8, 8, 8, 3, 3, 3, 7, 7, 7, 6, 6, 6, 2, 2, 2, 2],
               bcolors=[8, 3, 7, 6, 2], bidxs=[0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
