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


def generate(width=None, height=None, size=None, brows=None, bcols=None,
             cdirs=None, colors=None, extra_rows=None, extra_cols=None,
             extra_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    size: The size of the output grid.
    brows: The rows of the lines.
    bcols: The columns of the lines.
    cdirs: The directions of the lines.
    colors: The colors of the lines.
    extra_rows: The rows of the extra pixels (to handle a broken case).
    extra_cols: The columns of the extra lines (to handle a broken case).
    extra_colors: The colors of the extra lines (to handle a broken case).
  """

  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    size = common.randint(5, 8)
    colors = common.random_colors((size + 1) // 2)
    cdirs = [common.randint(0, 1) for _ in range((size + 1) // 2)]
    while True:
      wides = [1 if cdir else (size - i * 2) for i, cdir in enumerate(cdirs)]
      talls = [(size - i * 2) if cdir else 1 for i, cdir in enumerate(cdirs)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break

  grid, output = common.grid(width, height), common.grid(size, size)
  for i, length in enumerate(range(size, 0, -2)):
    common.rect(output, length, length, i, i, colors[i])
    for j in range(length):
      row = (brows[i] + j) if cdirs[i] else brows[i]
      col = bcols[i] if cdirs[i] else (bcols[i] + j)
      grid[row][col] = colors[i]
  if extra_rows is not None:
    for row, col, color in zip(extra_rows, extra_cols, extra_colors):
      grid[row][col] = color  # Broken / ambiguous case.
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=21, size=6, brows=[2, 3, 8], bcols=[13, 4, 8],
               cdirs=[1, 1, 1], colors=[1, 3, 6]),
      generate(width=29, height=23, size=5, brows=[4, 12, 9], bcols=[3, 8, 15],
               cdirs=[0, 0, 0], colors=[2, 3, 8], extra_rows=[12],
               extra_cols=[11], extra_colors=[3]),
      generate(width=20, height=24, size=8, brows=[0, 15, 9, 8],
               bcols=[14, 7, 9, 4], cdirs=[1, 0, 1, 0], colors=[8, 3, 4, 7]),
  ]
  test = [
      generate(width=23, height=21, size=7, brows=[12, 11, 6, 4],
               bcols=[10, 2, 10, 6], cdirs=[1, 0, 1, 0], colors=[8, 6, 7, 3]),
  ]
  return {"train": train, "test": test}
