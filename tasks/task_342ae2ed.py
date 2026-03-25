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


def generate(brows=None, bcols=None, sizes=None, lengths=None, colors=None,
             angles=None, dim=16):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows where the boxes start.
    bcols: The columns where the boxes start.
    sizes: The sizes of the boxes.
    lengths: The lengths of the lines.
    colors: The colors of the boxes.
    angles: The angles of the lines.
    dim: The dimension of the grid.
  """

  def draw():
    if len(set(sizes)) == 1: return None, None  # Require 1+ of each size.
    if len(set(angles)) == 1: return None, None  # Require 1+ of each angle.
    grid, output = common.grids(dim, dim, 7)
    for brow, bcol, size, length, color, angle in zip(brows, bcols, sizes,
                                                      lengths, colors, angles):
      r, c = brow, bcol
      for row in range(size):
        for col in range(size):
          if r + row < 0 or c + col < 0 or r + row >= dim or c + col >= dim:
            return None, None
          if output[r + row][c + col] != 7: return None, None
          output[r + row][c + col] = grid[r + row][c + col] = color
      r += size
      c += size if angle == 1 else -1
      for _ in range(length):
        if r < 0 or c < 0 or r >= dim or c >= dim: return None, None
        if output[r][c] != 7: return None, None
        output[r][c] = color
        r += 1
        c += angle
      if angle == -1: c -= size - 1
      for row in range(size):
        for col in range(size):
          if r + row < 0 or c + col < 0 or r + row >= dim or c + col >= dim:
            return None, None
          if output[r + row][c + col] != 7: return None, None
          output[r + row][c + col] = grid[r + row][c + col] = color
    return grid, output

  if brows is None:
    lines = common.randint(3, 5)
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], lines)
    while True:
      sizes = [common.randint(2, 3) for _ in range(lines)]
      lengths = [common.randint(2, 6) for _ in range(lines)]
      brows = [common.randint(0, dim - 2 * size - length) for size, length in zip(sizes, lengths)]
      bcols = [common.randint(0, dim - size) for size in sizes]
      angles = [2 * common.randint(0, 1) - 1 for _ in range(lines)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[0, 1, 6, 6], bcols=[4, 13, 2, 14], sizes=[2, 3, 3, 2],
               lengths=[2, 3, 4, 6], colors=[9, 3, 1, 4],
               angles=[1, -1, 1, -1]),
      generate(brows=[2, 2, 9], bcols=[2, 12, 1], sizes=[3, 2, 2],
               lengths=[6, 5, 3], colors=[8, 4, 9], angles=[1, -1, 1]),
      generate(brows=[0, 1, 6, 7], bcols=[0, 8, 14, 7], sizes=[2, 3, 2, 2],
               lengths=[2, 3, 5, 3], colors=[0, 9, 5, 3],
               angles=[1, -1, -1, 1]),
  ]
  test = [
      generate(brows=[0, 3, 5, 6, 10], bcols=[9, 10, 2, 8, 13],
               sizes=[2, 2, 2, 3, 2], lengths=[2, 2, 4, 4, 2],
               colors=[4, 1, 6, 8, 3], angles=[-1, 1, 1, -1, -1]),
  ]
  return {"train": train, "test": test}
