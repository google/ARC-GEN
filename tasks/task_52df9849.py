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


def generate(wides=None, talls=None, rows=None, cols=None, colors=None,
             orders=None, shapes=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: widths of the boxes.
    talls: talls of the boxes.
    rows: rows of the boxes.
    cols: columns of the boxes.
    colors: colors of the boxes.
    orders: order of the boxes.
    shapes: shapes of the boxes.
  """

  def draw():
    grid, output = common.grids(16, 16, 7)
    # Draw the shapes without checking anything.
    for order in [0, 1]:
      for t, w, r, c, l, o, s in zip(talls, wides, rows, cols, colors, orders, shapes):
        layer = grid if o == order else output
        if s == 0: common.rect(layer, w, t, r, c, l)
        if s == 1: common.backslash(layer, w, r, c, l)
        if s == 2: common.slash(layer, w, r, c, l)
    # Check #1: every color must be visible in both grids.
    flattened_grid = common.flatten(grid)
    flattened_output = common.flatten(output)
    for color in colors:
      if color not in flattened_grid or color not in flattened_output:
        return None, None
    # Check #2: every color must be partially obscured by another color.
    obscured = set()
    for t, w, r, c, l, o, s in zip(talls, wides, rows, cols, colors, orders, shapes):
      layer = output if o else grid
      if s == 0 and common.rect_obscured(layer, w, t, r, c, l): obscured.add(l)
      if s == 1 and common.backslash_obscured(layer, w, r, c, l): obscured.add(l)
      if s == 2 and common.slash_obscured(layer, w, r, c, l): obscured.add(l)
    if len(obscured) != len(set(colors)): return None, None
    # Check #3: for every object, over half of all corners must be visible.
    for t, w, r, c, l, o, s in zip(talls, wides, rows, cols, colors, orders, shapes):
      if o: continue  # We're only worried about objects hidden in *input* background.
      layer = output if o else grid
      if s == 0 and not common.rect_visible(layer, w, t, r, c, l): return None, None
      if s == 1 and not common.backslash_visible(layer, w, r, c, l): return None, None
      if s == 2 and not common.slash_visible(layer, w, r, c, l): return None, None
    return grid, output

  if wides is None:
    num_boxes = [common.randint(1, 3), common.randint(1, 3)]
    while True:
      # These are the "pre-shaved" lists.
      pwides, ptalls, prows, pcols, pcolors, porders, pshapes = [], [], [], [], [], [], []
      good = True
      for o in [0, 1]:
        ws = [common.randint(1, 16) for _ in range(num_boxes[o])]
        ts = [common.randint(1, 16) for _ in range(num_boxes[o])]
        rs = [common.randint(0, 16 - tall) for tall in ts]
        cs = [common.randint(0, 16 - wide) for wide in ws]
        available = [c for c in [0, 1, 2, 3, 4, 5, 6, 8, 9] if c not in pcolors]
        ls = common.sample(available, num_boxes[o])
        os = [o] * len(ws)
        ss = [0 if w != t else common.randint(1, 2) for w, t in zip(ws, ts)]
        if common.overlaps(rs, cs, ws, ts, 1): good = False
        pwides.extend(ws)
        ptalls.extend(ts)
        prows.extend(rs)
        pcols.extend(cs)
        pcolors.extend(ls)
        porders.extend(os)
        pshapes.extend(ss)
      if not good: continue
      # Now, shave down some of the rectangles.
      wides, talls, rows, cols, colors, orders, shapes = [], [], [], [], [], [], []
      for w, t, r, c, l, o, s in zip(pwides, ptalls, prows, pcols, pcolors, porders, pshapes):
        if s != 0 or common.randint(0, 4) > 0:
          wides.append(w)
          talls.append(t)
          rows.append(r)
          cols.append(c)
          colors.append(l)
          orders.append(o)
          shapes.append(s)
          continue
        swides, stalls, srows, scols = common.shave(w, t, r, c)
        wides.extend(swides)
        talls.extend(stalls)
        rows.extend(srows)
        cols.extend(scols)
        colors.extend([l] * len(swides))
        orders.extend([o] * len(swides))
        shapes.extend([s] * len(swides))
      grid, output = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[4, 5], talls=[6, 7], rows=[4, 6], cols=[7, 4],
               colors=[4, 1], orders=[0, 1], shapes=[0, 0]),
      generate(wides=[1, 10], talls=[11, 1], rows=[2, 7], cols=[5, 2],
               colors=[5, 9], orders=[1, 0], shapes=[0, 0]),
  ]
  test = [
      generate(wides=[2, 2, 4, 14, 16], talls=[12, 12, 12, 2, 3],
               rows=[2, 2, 2, 4, 9], cols=[2, 6, 10, 1, 0],
               colors=[5, 8, 6, 9, 1], orders=[1, 1, 1, 0, 0],
               shapes=[0, 0, 0, 0, 0]),
      generate(wides=[15, 11, 10, 8, 7, 5, 4, 2, 1, 3],
               talls=[15, 1, 1, 1, 1, 1, 1, 1, 1, 5],
               rows=[1, 10, 9, 8, 7, 6, 5, 4, 3, 4],
               cols=[0, 4, 5, 6, 7, 8, 9, 10, 11, 13],
               colors=[3, 8, 8, 8, 8, 8, 8, 8, 8, 2],
               orders=[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               shapes=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
