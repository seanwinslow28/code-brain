# Illustrator ExtendScript Pattern Reference

Read this when you need exact ExtendScript code patterns for `execute_extend_script` calls. The main SKILL.md provides the overview and workflow patterns; this file has the code recipes.

## Standard Script Template

Every script sent to `execute_extend_script` should follow this structure:

```javascript
try {
  var doc = app.activeDocument;
  app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;

  // ... operation logic ...

  JSON.stringify({status: "success", data: /* result */});
} catch(e) {
  JSON.stringify({status: "error", message: e.toString()});
}
```

**Note:** Unlike After Effects, Illustrator does not have `beginUndoGroup` / `endUndoGroup`. Each script execution is treated as one undoable action automatically.

## Document Management

### Create New Document
```javascript
var preset = new DocumentPreset();
preset.width = 256;   // points (72pt = 1 inch)
preset.height = 192;
preset.colorMode = DocumentColorSpace.RGB;
preset.units = RulerUnits.Pixels;
var doc = app.documents.addDocument("", preset);
doc.name = "SpriteSheet_v01";
```

### Get Active Document Info
```javascript
var doc = app.activeDocument;
JSON.stringify({
  name: doc.name,
  width: doc.width,
  height: doc.height,
  colorSpace: doc.documentColorSpace.toString(),
  numLayers: doc.layers.length,
  numArtboards: doc.artboards.length,
  rulerUnits: doc.rulerUnits.toString()
});
```

### Suppress Dialogs (Batch Operations)
```javascript
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
// ... batch operations ...
app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
```

## Shapes & Paths

### Rectangle
```javascript
// IMPORTANT: Argument order is (top, left, width, height) — NOT (x, y, w, h)
// top = Y position, left = X position
// Negative Y moves DOWN on canvas
var rect = doc.pathItems.rectangle(0, 0, 100, 100);
// Creates 100x100 square at artboard origin (top-left)
rect.name = "Background";
```

### Rectangle at Grid Position
```javascript
// For sprite grid: cell at column 2, row 1 (0-indexed), 64px cells
var col = 2; var row = 1; var cellSize = 64;
var x = col * cellSize;
var y = -(row * cellSize); // negative Y = down
var rect = doc.pathItems.rectangle(y, x, cellSize, cellSize);
```

### Ellipse
```javascript
var circle = doc.pathItems.ellipse(0, 0, 50, 50);
// Args: top, left, width, height
circle.name = "Dot";
```

### Polygon
```javascript
var hex = doc.pathItems.polygon(128, -64, 30, 6);
// Args: centerX, centerY, radius, sides
hex.name = "Hexagon";
```

### Custom Path
```javascript
var path = doc.pathItems.add();
path.setEntirePath([[0, 0], [100, 0], [50, -86.6]]);
// Array of [x, y] coordinate pairs — creates a triangle
path.closed = true;
path.name = "Triangle";
```

### Rounded Rectangle
```javascript
var rrect = doc.pathItems.roundedRectangle(0, 0, 200, 100, 10, 10);
// Args: top, left, width, height, horizontalRadius, verticalRadius
rrect.name = "Button_BG";
```

## Colors

### RGB Color (for RGB documents)
```javascript
var red = new RGBColor();
red.red = 255;
red.green = 0;
red.blue = 0;

var path = doc.pathItems.rectangle(0, 0, 100, 100);
path.fillColor = red;
path.filled = true;      // Must explicitly enable fill
path.stroked = false;     // Disable stroke if not needed
```

### Hex to RGB Helper
```javascript
function hexToRGB(hex) {
  hex = hex.replace("#", "");
  var c = new RGBColor();
  c.red = parseInt(hex.substring(0, 2), 16);
  c.green = parseInt(hex.substring(2, 4), 16);
  c.blue = parseInt(hex.substring(4, 6), 16);
  return c;
}
var brandColor = hexToRGB("#4A90D9");
```

### No Fill / No Stroke
```javascript
path.filled = false;
path.stroked = true;
path.strokeWidth = 2;
path.strokeColor = new RGBColor(); // defaults to black
```

### CMYK Color (for CMYK documents)
```javascript
var cyan = new CMYKColor();
cyan.cyan = 100;
cyan.magenta = 0;
cyan.yellow = 0;
cyan.black = 0;
path.fillColor = cyan;
```

### Check Document Color Space Before Applying
```javascript
if (doc.documentColorSpace == DocumentColorSpace.RGB) {
  var color = new RGBColor();
  color.red = 255; color.green = 128; color.blue = 0;
} else {
  var color = new CMYKColor();
  color.cyan = 0; color.magenta = 50; color.yellow = 100; color.black = 0;
}
path.fillColor = color;
```

## Transformations

### Position (Move)
```javascript
// item.position = [x, y]
myItem.position = [100, -50]; // 100pt right, 50pt down from origin
```

### Resize
```javascript
// resize(scaleX%, scaleY%)
myItem.resize(150.0, 150.0); // Scale to 150%
```

### Rotate
```javascript
// rotate(angle) — positive = counterclockwise
myItem.rotate(45);
```

### Translate
```javascript
// translate(deltaX, deltaY)
myItem.translate(50, -30); // Move 50pt right, 30pt down
```

### Matrix Transformations (Complex)
```javascript
var scaleMatrix = app.getScaleMatrix(200, 200);    // 2x scale
var rotMatrix = app.getRotationMatrix(45);          // 45 degrees
var combined = app.concatenateMatrix(scaleMatrix, rotMatrix);
myItem.transform(combined);
```

## Grouping & Organization

### Create Group and Move Items Into It
```javascript
var group = doc.groupItems.add();
group.name = "Sprite_01";
// Move existing items into group:
myPath.moveToBeginning(group);
myCircle.moveToBeginning(group);
```

### Group Selected Items
```javascript
// Alternative: use menu command
app.executeMenuCommand("group");
```

### Layer Management
```javascript
// Create new layer
var newLayer = doc.layers.add();
newLayer.name = "Sprites";

// Move item to layer
myGroup.move(newLayer, ElementPlacement.PLACEATBEGINNING);

// Lock/unlock layer
newLayer.locked = false;

// Hide/show layer
newLayer.visible = true;
```

## Artboard Management

### Add Artboard
```javascript
// rect = [left, top, right, bottom] in points
var rect = [0, 0, 256, -192]; // 256x192 artboard
var abIndex = doc.artboards.add(rect);
doc.artboards[abIndex].name = "SpriteSheet";
```

### Iterate Artboards
```javascript
var abs = [];
for (var i = 0; i < doc.artboards.length; i++) {
  var ab = doc.artboards[i];
  var rect = ab.artboardRect; // [left, top, right, bottom]
  abs.push({
    index: i,
    name: ab.name,
    width: rect[2] - rect[0],
    height: rect[1] - rect[3], // top - bottom (remember Y-axis)
    position: [rect[0], rect[1]]
  });
}
JSON.stringify({artboards: abs});
```

### Set Active Artboard
```javascript
doc.artboards.setActiveArtboardIndex(0);
```

## Text

### Point Text
```javascript
var textFrame = doc.textFrames.pointText([100, -50]);
// Args: anchor point [x, y]
textFrame.contents = "Front View";
textFrame.textRange.characterAttributes.size = 14;
var blackColor = new RGBColor();
blackColor.red = 0; blackColor.green = 0; blackColor.blue = 0;
textFrame.textRange.characterAttributes.fillColor = blackColor;
```

### Area Text
```javascript
var textRect = doc.pathItems.rectangle(-10, 10, 200, 100);
var areaText = doc.textFrames.areaText(textRect);
areaText.contents = "This text wraps within the rectangle bounds.";
```

## SVG Export

### Export SVG with Optimization
```javascript
var doc = app.activeDocument;
var svgFile = new File("/path/to/output.svg");
var opts = new ExportOptionsSVG();
opts.cssProperties = SVGCSSPropertyLocation.PRESENTATIONATTRIBUTES; // Best for CSS animation
opts.fontType = SVGFontType.OUTLINEFONT;           // Convert text to paths
opts.coordinatePrecision = 3;                       // Balance size vs precision
opts.embedRasterImages = false;                     // Keep SVG light
opts.DTD = SVGDTDVersion.SVG1_1;                   // Standard SVG 1.1
opts.documentEncoding = SVGDocumentEncoding.UTF8;
opts.compressed = false;                            // Human-readable
doc.exportFile(svgFile, ExportType.SVG, opts);
```

### Export SVG (Compact / Production)
```javascript
var opts = new ExportOptionsSVG();
opts.cssProperties = SVGCSSPropertyLocation.STYLEELEMENTS; // Single <style> block
opts.fontType = SVGFontType.OUTLINEFONT;
opts.coordinatePrecision = 1;     // Minimal precision for small file size
opts.compressed = true;           // SVGZ format
opts.embedRasterImages = true;    // Self-contained
```

## PNG Export via ExtendScript

### Export PNG24
```javascript
var opts = new ExportOptionsPNG24();
opts.transparency = true;
opts.artBoardClipping = true;
opts.antiAliasing = true;         // false for pixel art
opts.horizontalScale = 400;       // 4x scale
opts.verticalScale = 400;
var pngFile = new File("/path/to/output.png");
doc.exportFile(pngFile, ExportType.PNG24, opts);
```

## Iteration Patterns

### Iterate All PageItems
```javascript
var items = [];
for (var i = 0; i < doc.pageItems.length; i++) {
  var item = doc.pageItems[i];
  items.push({
    name: item.name,
    type: item.typename,  // "PathItem", "GroupItem", "TextFrame", etc.
    position: item.position,
    width: item.width,
    height: item.height,
    visible: !item.hidden
  });
}
JSON.stringify({pageItems: items});
```

### Find Items by Name
```javascript
var found = [];
for (var i = 0; i < doc.pageItems.length; i++) {
  if (doc.pageItems[i].name.indexOf("Sprite") === 0) {
    found.push({index: i, name: doc.pageItems[i].name});
  }
}
JSON.stringify({matches: found});
```

### Clean Up Hidden Items
```javascript
var removed = 0;
for (var i = doc.pageItems.length - 1; i >= 0; i--) {
  if (doc.pageItems[i].hidden) {
    doc.pageItems[i].remove();
    removed++;
  }
}
// IMPORTANT: Iterate backwards when removing items
JSON.stringify({removed: removed});
```

### Remove Empty Text Frames
```javascript
var removed = 0;
for (var i = doc.textFrames.length - 1; i >= 0; i--) {
  if (doc.textFrames[i].contents === "") {
    doc.textFrames[i].remove();
    removed++;
  }
}
JSON.stringify({emptyTextFramesRemoved: removed});
```

## Alignment

### Align to Artboard Center
```javascript
var ab = doc.artboards[doc.artboards.getActiveArtboardIndex()];
var abRect = ab.artboardRect; // [left, top, right, bottom]
var abCenterX = (abRect[0] + abRect[2]) / 2;
var abCenterY = (abRect[1] + abRect[3]) / 2;

var item = doc.selection[0]; // or any pageItem
var itemCenterX = item.position[0] + item.width / 2;
var itemCenterY = item.position[1] - item.height / 2;

item.translate(abCenterX - itemCenterX, abCenterY - itemCenterY);
```

## Sprite Grid Assembly (Complete Pattern)

```javascript
var doc = app.activeDocument;
app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;

var cols = 4;
var rows = 3;
var cellW = 64;
var cellH = 64;
var sprites = [];

for (var r = 0; r < rows; r++) {
  for (var c = 0; c < cols; c++) {
    var idx = r * cols + c + 1;
    var x = c * cellW;
    var y = -(r * cellH); // negative Y = down

    var group = doc.groupItems.add();
    group.name = "Sprite_" + (idx < 10 ? "0" : "") + idx;

    // Create placeholder cell (replace with actual sprite content)
    var cell = doc.pathItems.rectangle(y, x, cellW, cellH);
    cell.filled = false;
    cell.stroked = true;
    cell.strokeWidth = 0.5;
    cell.moveToBeginning(group);

    sprites.push({name: group.name, col: c, row: r, x: x, y: y});
  }
}
JSON.stringify({status: "success", sprites: sprites, grid: cols + "x" + rows});
```

## Known Gotchas

- **Rectangle arg order**: `rectangle(top, left, width, height)` — Y before X
- **Negative Y = down**: Moving down the canvas requires negative Y values
- **0-based layers**: Unlike AE (1-based), Illustrator layers are 0-indexed: `doc.layers[0]`
- **`filled = true` required**: Setting `fillColor` alone doesn't enable fill — must also set `filled = true`
- **Backwards iteration for removal**: When removing items from collections, iterate from `length-1` down to 0
- **Group workflow**: Create group first, then `moveToBeginning(group)` — cannot pass items at creation time
- **Color space mismatch**: Always check `doc.documentColorSpace` before creating `RGBColor` or `CMYKColor`
- **No undo groups**: Unlike AE, no explicit undo grouping — each script run is one undo step
