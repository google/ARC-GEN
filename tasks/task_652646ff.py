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


def generate(size=None, bgcolor=None, brows=None, bcols=None, bcolors=None,
             prows=None, pcols=None, pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    bgcolor: The background color.
    brows: The row indices of the blobs.
    bcols: The column indices of the blobs.
    bcolors: The colors of the blobs.
    prows: The row indices of the pixels.
    pcols: The column indices of the pixels.
    pcolors: The colors of the pixels.
  """

  def draw():
    if common.overlaps(brows, bcols, [1] * len(brows), [1] * len(bcols)):
      return None, None
    grid = common.grid(size, size, bgcolor)
    output = common.grid(6, 6 * len(bcolors), bgcolor)
    drs = [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0]
    dcs = [3, 4, 5, 5, 4, 3, 2, 1, 0, 0, 1, 2]
    for i, (brow, bcol, bcolor) in enumerate(reversed(list(zip(brows, bcols, bcolors)))):
      for dr, dc in zip(drs, dcs):
        common.draw(grid, brow + dr, bcol + dc, bcolor)
        output[(len(bcolors) - i - 1) * 6 + dr][dc] = bcolor
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      grid[prow][pcol] = pcolor
    # Check that each blob is (a) covered by the one above it, and (b) shows at
    # least 8 pixels.
    for i in range(1, len(bcolors)):
      covered = False
      num_showing = 0
      for dr, dc in zip(drs, dcs):
        color = common.get_pixel(grid, brows[i] + dr, bcols[i] + dc)
        if color == bcolors[i - 1]: covered = True
        if color == bcolors[i]: num_showing += 1
      if not covered or num_showing < 8: return None, None
    return grid, output

  if size is None:
    size = common.randint(10, 20)
    num_blobs = common.randint(2, 3)
    if size > 15: num_blobs += 1
    num_pixels = common.randint(3, 7)
    colors = common.shuffle(list(range(10)))
    bgcolor = colors.pop()
    bcolors = [colors.pop() for _ in range(num_blobs)]
    pixel_colors = [colors.pop() for _ in range(2)]
    while True:
      brows = [common.randint(-1, size - 5) for _ in range(num_blobs)]
      bcols = [common.randint(-1, size - 5) for _ in range(num_blobs)]
      prows = [common.randint(0, size - 1) for _ in range(num_pixels)]
      pcols = [common.randint(0, size - 1) for _ in range(num_pixels)]
      pcolors = common.choices(pixel_colors, num_pixels)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, bgcolor=2, brows=[7, 7, 8], bcols=[1, 6, 10],
               bcolors=[4, 8, 3], prows=[2, 2, 9, 10, 10, 16, 19],
               pcols=[3, 17, 7, 3, 13, 10, 0], pcolors=[5, 5, 5, 9, 9, 5, 5]),
      generate(size=10, bgcolor=3, brows=[1, 2, 4], bcols=[1, 2, 0],
               bcolors=[4, 8, 1], prows=[1, 7, 9], pcols=[0, 2, 6],
               pcolors=[5, 5, 5]),
      generate(size=13, bgcolor=4, brows=[8, 5, 2], bcols=[6, 3, 0],
               bcolors=[3, 8, 2], prows=[0, 1, 4, 5, 10, 11, 11],
               pcols=[5, 11, 3, 9, 1, 2, 9], pcolors=[5, 7, 7, 5, 5, 7, 5]),
      generate(size=10, bgcolor=8, brows=[2, 2], bcols=[1, 4], bcolors=[4, 3],
               prows=[0, 4, 8, 9], pcols=[8, 2, 1, 7], pcolors=[5, 2, 5, 2]),
  ]
  test = [
      generate(size=17, bgcolor=1, brows=[3, 6, 8, 7], bcols=[5, 8, 4, 5],
               bcolors=[8, 4, 3, 7], prows=[1, 2, 8, 11, 15, 16],
               pcols=[14, 2, 3, 16, 11, 0],
               pcolors=[0, 0, 5, 5, 0, 5]),
  ]
  return {"train": train, "test": test}
