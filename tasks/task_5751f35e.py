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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(size, size)
    half = size // 2
    radii = [0] * half
    for i, color in enumerate(colors):
      row, col = i // size, i % size
      grid[row][col] = color
      r = (half - 1 - row) if row < half else (row - half)
      c = (half - 1 - col) if col < half else (col - half)
      if color: radii[max(r, c)] = color
    for row in range(size):
      for col in range(size):
        r = (half - 1 - row) if row < half else (row - half)
        c = (half - 1 - col) if col < half else (col - half)
        output[row][col] = radii[max(r, c)]
    return grid, output, radii

  if size is None:
    num_colors = 3
    while True:
      lengths = [common.randint(1, 3) for _ in range(num_colors)]
      size = 2 * sum(lengths)
      if size < 8 or size > 12: continue
      half = size // 2
      colors = common.sample(list(range(10)), num_colors)
      radii = []
      for color, length in zip(colors, lengths):
        for _ in range(length):
          radii.append(color)
      slate = common.grid(size, size)
      for row in range(size):
        for col in range(size):
          r = (half - 1 - row) if row < half else (row - half)
          c = (half - 1 - col) if col < half else (col - half)
          slate[row][col] = radii[max(r, c)]
      for r, c in common.random_pixels(size, size):
        slate[r][c] = 0
      colors = common.flatten(slate)
      _, _, the_radii = draw()
      if the_radii == radii: break  # Ensure all colors were correctly inferred.

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, colors=[3, 0, 3, 0, 0, 3, 3, 3, 0, 3,
                                0, 2, 2, 2, 0, 0, 2, 0, 2, 0,
                                0, 2, 2, 0, 0, 0, 0, 2, 0, 0,
                                0, 2, 0, 8, 0, 8, 8, 0, 2, 0,
                                3, 2, 2, 0, 8, 8, 0, 2, 2, 0,
                                3, 0, 0, 8, 0, 8, 0, 2, 0, 0,
                                0, 0, 2, 8, 0, 8, 8, 2, 2, 0,
                                0, 2, 2, 0, 2, 2, 2, 2, 2, 0,
                                0, 0, 2, 2, 2, 0, 2, 0, 2, 3,
                                3, 3, 3, 0, 3, 3, 3, 3, 0, 3]),
      generate(size=10, colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 8, 8, 0, 8, 8, 8, 8, 8, 0,
                                0, 8, 2, 0, 0, 0, 2, 2, 0, 0,
                                0, 0, 0, 2, 0, 0, 2, 0, 8, 0,
                                0, 8, 0, 2, 2, 0, 0, 0, 0, 0,
                                0, 8, 2, 0, 0, 0, 2, 0, 8, 0,
                                0, 8, 0, 2, 0, 0, 0, 0, 0, 0,
                                0, 8, 0, 0, 0, 0, 0, 0, 8, 0,
                                0, 0, 8, 8, 8, 0, 8, 8, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(size=12, colors=[4, 0, 0, 0, 0, 4, 0, 4, 4, 0, 4, 0,
                                0, 4, 0, 0, 0, 0, 4, 4, 0, 4, 4, 4,
                                4, 4, 0, 3, 3, 0, 3, 3, 3, 3, 0, 0,
                                4, 0, 3, 0, 3, 0, 3, 0, 3, 0, 4, 4,
                                0, 4, 3, 3, 0, 1, 1, 0, 3, 3, 0, 4,
                                0, 4, 0, 3, 1, 0, 1, 0, 0, 3, 4, 0,
                                0, 0, 3, 3, 1, 1, 1, 1, 0, 3, 0, 4,
                                0, 4, 3, 0, 0, 1, 0, 1, 3, 3, 0, 4,
                                4, 4, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0,
                                0, 0, 3, 0, 3, 3, 0, 0, 3, 3, 4, 4,
                                4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 4, 0,
                                4, 0, 4, 4, 0, 4, 0, 0, 4, 4, 0, 4]),
  ]
  return {"train": train, "test": test}
