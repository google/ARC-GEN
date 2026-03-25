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


def generate(size=None, lengths=None, brows=None, bcols=None, colors=None,
             groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    lengths: The lengths of the shapes.
    brows: The rows of the shapes.
    bcols: The columns of the shapes.
    colors: The colors of the shapes.
    groups: The groups of the colors.
  """

  if size is None:
    size = common.randint(5, 12)
    num_boxes = size // 5
    while True:
      lengths = [common.randint(1, min(5, size // 2)) for _ in range(num_boxes)]
      brows = [common.randint(0, size - length) for length in lengths]
      if not common.overlaps_1d(brows, lengths, 2): break
    bcols = [common.randint(0, size - 2 * length) for length in lengths]
    colors, groups = [], []
    for group, length in enumerate(lengths):
      pixels = common.diagonally_connected_sprite(length, length, length)
      for row in range(length):
        for col in range(length):
          colors.append(1 if (row, col) in pixels else 0)
          groups.append(group)

  grid, output = common.grids(size, size)
  for i, (length, brow, bcol) in enumerate(zip(lengths, brows, bcols)):
    hues = [int(c) for c, g in zip(colors, groups) if int(g) == i]
    for row in range(length):
      for col in range(length):
        grid[brow + row][bcol + col] = 8 * hues[row * length + col]
        output[brow + row][bcol + col + length] = 8 * hues[row * length + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, lengths=[2], brows=[1], bcols=[0], colors="1111",
               groups="0000"),
      generate(size=10, lengths=[3, 1], brows=[1, 6], bcols=[1, 1],
               colors="1111011111", groups="0000000001"),
      generate(size=12, lengths=[4, 2], brows=[1, 8], bcols=[1, 4],
               colors="11111100001111111111", groups="00000000000000001111"),
  ]
  test = [
      generate(size=12, lengths=[5, 2], brows=[1, 8], bcols=[1, 4],
               colors="10101101010101001010101010111",
               groups="00000000000000000000000001111"),
  ]
  return {"train": train, "test": test}
