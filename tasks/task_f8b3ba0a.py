# Copyright 2025 Google LLC
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


def generate(width=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(3, 5), common.randint(6, 7)
    color_list = common.random_colors(4)
    counts = common.sample(range(1, 5), 3)
    bitmap = common.grid(width, height, color_list[0])
    for idx, count in enumerate(counts):
      for _ in range(count):
        while True:
          r, c = common.randint(0, height - 1), common.randint(0, width - 1)
          if bitmap[r][c] != color_list[0]: continue
          bitmap[r][c] = color_list[idx + 1]
          break
    colors = []
    for row in bitmap:
      colors.extend(row)

  height = len(colors) // width
  grid = common.grid(3 * width + 1, 2 * height + 1)
  for r in range(height):
    for c in range(width):
      for dc in range(2):
        grid[2 * r + 1][3 * c + dc + 1] = colors[r * width + c]
  counts_to_colors = {colors.count(x): x for x in colors}
  counts = sorted(counts_to_colors.keys(), reverse=True)
  output = common.grid(1, len(set(colors)) - 1)
  for r, count in enumerate(counts):
    if not r: continue
    output[r - 1][0] = counts_to_colors[count]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4,
               colors=[3, 1, 1, 1, 1, 1, 4, 4, 1, 4, 1, 1, 2, 1, 1, 1, 1, 2, 1,
                       1, 1, 1, 1, 1]),
      generate(width=5,
               colors=[6, 8, 8, 8, 8, 8, 8, 2, 6, 8, 1, 8, 1, 8, 8, 8, 1, 8, 8,
                       8, 8, 8, 6, 8, 6, 8, 8, 8, 8, 8]),
      generate(width=3,
               colors=[3, 3, 3, 1, 3, 3, 3, 8, 3, 3, 8, 3, 3, 2, 2, 2, 3, 3]),
      generate(width=4,
               colors=[1, 1, 8, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 8, 1, 1, 8, 1,
                       4, 1, 8, 1, 1]),
  ]
  test = [
      generate(width=4,
               colors=[2, 4, 2, 2, 1, 2, 4, 2, 8, 2, 2, 8, 2, 2, 1, 2, 4, 2, 2,
                       2, 2, 1, 2, 4, 2, 2, 4, 2]),
  ]
  return {"train": train, "test": test}
