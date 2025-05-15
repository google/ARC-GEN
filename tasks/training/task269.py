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


def generate(rows=None, cols=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: digits representing the colors to be used
    size: the width and height of the (square) input grid
  """
  if rows is None:
    pixels = common.all_pixels(size, size)
    pixels = common.sample(pixels, common.randint(1, 9))
    rows, cols = zip(*pixels)
    colors = common.random_colors(len(pixels))

  grid, output = common.grid_enhance(size, len(colors), rows, cols,
                                     range(len(colors)), colors, common.black())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1], cols=[0, 2], colors=[2, 7]),
      generate(rows=[0, 1, 2], cols=[1, 2, 0], colors=[4, 8, 6]),
      generate(rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 2, 1],
               colors=[6, 9, 3, 2, 7]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[0, 1, 2, 0], colors=[1, 9, 6, 8]),
  ]
  return {"train": train, "test": test}
