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


def generate(width=None, height=None, prows=None, pcols=None, pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    pcolors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height, 7)
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      output[prow][pcol] = grid[prow][pcol] = pcolor
    idx = 0
    vuniq = len(set(pcols)) == len(pcols)
    huniq = len(set(prows)) == len(prows)
    if vuniq == huniq: return None, None
    if huniq:
      for row in range(height):
        for col in range(width):
          if output[row][col] == 7: continue
          output[row][col] = [2, 8, 5][idx % 3]
          idx += 1
    if vuniq:
      for col in range(width):
        for row in range(height):
          if output[row][col] == 7: continue
          output[row][col] = [2, 8, 5][idx % 3]
          idx += 1
    return grid, output

  if width is None:
    width, height = common.randint(5, 12), common.randint(5, 12)
    vuniq = common.randint(0, 1)
    num_pixels = common.randint(width * height // 10, width * height // 6)
    num_pixels = min(num_pixels, height if vuniq else width)
    pcolors = common.choices([0, 1, 2, 3, 4, 5, 6, 8, 9], num_pixels)
    while True:
      if vuniq:
        prows = common.sample(range(height), num_pixels)
        pcols = [common.randint(0, width - 1) for _ in range(num_pixels)]
      else:
        prows = [common.randint(0, height - 1) for _ in range(num_pixels)]
        pcols = common.sample(range(width), num_pixels)
      if common.overlaps(prows, pcols, [1] * num_pixels, [1] * num_pixels, 1):
        continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=6, prows=[0, 1, 2, 3, 4, 5],
               pcols=[2, 4, 7, 2, 4, 2], pcolors=[9, 6, 4, 9, 6, 9]),
      generate(width=8, height=8, prows=[0, 1, 3, 4, 5, 6, 7],
               pcols=[0, 5, 2, 4, 6, 4, 2], pcolors=[6, 9, 6, 9, 1, 6, 1]),
      generate(width=10, height=6, prows=[1, 2, 2, 2, 2, 4, 4, 4, 4],
               pcols=[0, 2, 5, 7, 9, 1, 4, 6, 8],
               pcolors=[9, 6, 9, 1, 1, 1, 9, 9, 6]),
  ]
  test = [
      generate(width=12, height=9, prows=[1, 1, 2, 3, 5, 5, 6, 8, 8, 8],
               pcols=[0, 8, 2, 9, 5, 10, 1, 3, 7, 11],
               pcolors=[6, 4, 2, 2, 2, 0, 4, 6, 0, 6]),
  ]
  return {"train": train, "test": test}
