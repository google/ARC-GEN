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


def generate(rows=None, cols=None, idxs=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: digits representing indices into the colors list
    colors: digits representing the colors to be used
    size: the width and height of the (square) input grid
  """
  if rows is None:
    pixels = common.all_pixels(size, size)
    pixels = common.sample(pixels, common.randint(3, 5))
    rows, cols = zip(*pixels)
    colors = common.random_colors(common.randint(1, len(pixels)))
    idxs = list(range(len(colors)))  # Make sure we have one of each color
    while len(idxs) < len(pixels):
      idxs.append(common.randint(0, len(colors) - 1))
    common.shuffle(idxs)

  grid, output = common.grid_enhance(size, len(colors), rows, cols, idxs,
                                     colors, common.black())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2], idxs=[0, 1, 0, 0],
               colors=[6, 7]),
      generate(rows=[0, 0, 1, 2], cols=[0, 2, 1, 1], idxs=[0, 1, 1, 0],
               colors=[1, 4]),
      generate(rows=[0, 0, 1, 1], cols=[0, 1, 1, 2], idxs=[0, 1, 2, 0],
               colors=[3, 2, 7]),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 1, 2, 0, 1], idxs=[0, 1, 1, 2, 0],
               colors=[8, 6, 9]),
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 1, 2], idxs=[0, 1, 2, 2, 3],
               colors=[4, 3, 2, 8]),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 1, 2, 0, 1], idxs=[0, 1, 2, 3, 3],
               colors=[1, 8, 7, 9]),
  ]
  return {"train": train, "test": test}
