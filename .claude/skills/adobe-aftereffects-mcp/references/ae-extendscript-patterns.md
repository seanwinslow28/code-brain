# After Effects ExtendScript Pattern Reference

Read this when you need exact ExtendScript code patterns for `execute_extend_script` calls. The main SKILL.md provides the overview and animation intelligence; this file has the code recipes.

## Standard Script Template

Every script sent to `execute_extend_script` should follow this structure:

```javascript
app.beginUndoGroup("Action Description");
try {
  var proj = app.project;
  var comp = /* get or create comp */;

  // ... operation logic ...

  JSON.stringify({status: "success", data: /* result */});
} catch(e) {
  JSON.stringify({status: "error", message: e.toString()});
} finally {
  app.endUndoGroup();
}
```

## Project & Composition

### Create a New Composition
```javascript
var comp = app.project.items.addComp("Comp_Name", 1920, 1080, 1.0, 10, 30);
// Args: name, width, height, pixelAspect, duration(seconds), frameRate
```

### Find Composition by Name
```javascript
var comp = null;
for (var i = 1; i <= app.project.numItems; i++) {
  if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "Target_Comp") {
    comp = app.project.item(i);
    break;
  }
}
```

### Create Project Folder
```javascript
var folder = app.project.items.addFolder("Precomps");
// Move comp into folder:
comp.parentFolder = folder;
```

### Get Active Composition
```javascript
var comp = app.project.activeItem;
if (!(comp instanceof CompItem)) {
  JSON.stringify({status: "error", message: "No active composition"});
}
```

## Layer Creation

### Add Solid
```javascript
var solid = comp.layers.addSolid([1, 0, 0], "Red_BG", 1920, 1080, 1.0);
// Args: color[r,g,b] (0-1 range), name, width, height, pixelAspect
```

### Add Text Layer
```javascript
var textLayer = comp.layers.addText("Hello World");
var textProp = textLayer.property("Source Text");
var textDoc = textProp.value;
textDoc.fontSize = 72;
textDoc.fillColor = [1, 1, 1]; // white, 0-1 range
textDoc.font = "Arial-BoldMT";
textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
textProp.setValue(textDoc);
```

### Add Shape Layer
```javascript
var shapeLayer = comp.layers.addShape();
shapeLayer.name = "Circle";
var shapeGroup = shapeLayer.property("Contents").addProperty("ADBE Vector Group");
var ellipse = shapeGroup.property("Contents").addProperty("ADBE Vector Shape - Ellipse");
ellipse.property("Size").setValue([200, 200]);
var fill = shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Fill");
fill.property("Color").setValue([0, 0.5, 1]); // blue
```

### Add Null Object
```javascript
var nullLayer = comp.layers.addNull();
nullLayer.name = "Controller";
```

### Import and Add Footage
```javascript
var importOpts = new ImportOptions(new File("/path/to/video.mp4"));
var footage = app.project.importFile(importOpts);
var layer = comp.layers.add(footage);
```

## Property Access

### Transform Properties (Match Names)
```javascript
var transform = layer.property("ADBE Transform Group");
var position = transform.property("ADBE Position");       // [x, y] or [x, y, z]
var scale = transform.property("ADBE Scale");              // [x%, y%] or [x%, y%, z%]
var rotation = transform.property("ADBE Rotate Z");        // degrees
var opacity = transform.property("ADBE Opacity");          // 0-100
var anchorPoint = transform.property("ADBE Anchor Point"); // [x, y]
```

### Common Match Names
| Display Name | Match Name |
|-------------|-----------|
| Transform | ADBE Transform Group |
| Position | ADBE Position |
| Scale | ADBE Scale |
| Rotation | ADBE Rotate Z |
| Opacity | ADBE Opacity |
| Anchor Point | ADBE Anchor Point |
| Effects | ADBE Effect Parade |

### Access Effects
```javascript
var effects = layer.property("ADBE Effect Parade");
// Add effect by match name:
var blur = effects.addProperty("ADBE Gaussian Blur 2");
blur.property("Blurriness").setValue(10);
```

## Keyframing

### Set Keyframes
```javascript
var pos = layer.property("ADBE Transform Group").property("ADBE Position");
pos.setValueAtTime(0, [960, 800]);    // time in seconds, value
pos.setValueAtTime(1, [960, 540]);    // arrives at center at 1s
```

### Apply Easing
```javascript
var pos = layer.property("ADBE Transform Group").property("ADBE Position");
// After setting keyframes:
var easeIn = new KeyframeEase(0, 75);    // speed, influence (0-100)
var easeOut = new KeyframeEase(0, 75);

// For 2D position (array of 2 dimensions):
pos.setTemporalEaseAtKey(1, [easeIn, easeIn], [easeOut, easeOut]);   // key index 1
pos.setTemporalEaseAtKey(2, [easeIn, easeIn], [easeOut, easeOut]);   // key index 2
```

### Easy Ease Shortcut
```javascript
// Apply to all keyframes on a property:
for (var k = 1; k <= prop.numKeys; k++) {
  var dims = prop.value instanceof Array ? prop.value.length : 1;
  var easeArr = [];
  for (var d = 0; d < dims; d++) {
    easeArr.push(new KeyframeEase(0, 33));
  }
  prop.setTemporalEaseAtKey(k, easeArr, easeArr);
}
```

### Overshoot Pattern (Scale)
```javascript
var scale = layer.property("ADBE Transform Group").property("ADBE Scale");
scale.setValueAtTime(0, [0, 0]);       // start invisible
scale.setValueAtTime(0.5, [110, 110]); // overshoot
scale.setValueAtTime(0.7, [100, 100]); // settle
// Apply easing to all 3 keyframes
```

### Query Keyframe Data
```javascript
var numKeys = prop.numKeys;
var keys = [];
for (var k = 1; k <= numKeys; k++) {
  keys.push({
    index: k,
    time: prop.keyTime(k),
    value: prop.keyValue(k),
    interpolation: prop.keyOutInterpolationType(k).toString()
  });
}
JSON.stringify({keyframes: keys});
```

## Expressions

### Apply Expression
```javascript
var pos = layer.property("ADBE Transform Group").property("ADBE Position");
pos.expression = "wiggle(2, 50)";
// Check for errors:
if (pos.expressionError !== "") {
  JSON.stringify({status: "error", expressionError: pos.expressionError});
}
```

### Common Expressions
```javascript
// Wiggle (oscillations per second, amplitude in pixels)
"wiggle(2, 50)"

// Loop keyframes
"loopOut('cycle')"
"loopOut('pingpong')"
"loopIn('cycle')"

// Time-based
"time * 100"                    // linear motion
"Math.sin(time * 2) * 50"      // sine wave

// Value linking (slider control)
"thisComp.layer('Control').effect('Slider Control')('Slider')"

// Inertial bounce (after keyframes)
"n = 0; if (numKeys > 0) { n = nearestKey(time).index; if (key(n).time > time) n--; } if (n == 0) { value; } else { t = time - key(n).time; amp = velocityAtTime(key(n).time - thisComp.frameDuration/10); freq = 4; decay = 6; value + amp * (Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t)); }"

// Auto-resize background behind text
"src = thisComp.layer('Text Layer'); pad = 20; rect = src.sourceRectAtTime(time, false); [rect.width + pad*2, rect.height + pad*2]"
```

## MOGRTs (Motion Graphics Templates)

### Add Property to Essential Graphics Panel
```javascript
var prop = layer.property("Source Text");
prop.addToMotionGraphicsTemplate(comp);
// Also works for sliders, colors, checkboxes
```

### Set Template Name
```javascript
comp.motionGraphicsTemplateName = "Lower_Third_v01";
```

### Auto-Sizing Background Pattern
Apply this expression to a background shape's Size property:
```javascript
"src = thisComp.layer('Title Text'); pad = [40, 20]; rect = src.sourceRectAtTime(time, false); [rect.width + pad[0], rect.height + pad[1]]"
```

## Project Query (Read-Only)

### List All Comps
```javascript
var comps = [];
for (var i = 1; i <= app.project.numItems; i++) {
  var item = app.project.item(i);
  if (item instanceof CompItem) {
    comps.push({
      name: item.name,
      id: item.id,
      width: item.width,
      height: item.height,
      duration: item.duration,
      fps: item.frameRate,
      numLayers: item.numLayers
    });
  }
}
JSON.stringify({comps: comps});
```

### List Layers in Comp
```javascript
var layers = [];
for (var i = 1; i <= comp.numLayers; i++) {
  var lyr = comp.layer(i);
  layers.push({
    index: i,
    name: lyr.name,
    type: lyr instanceof TextLayer ? "text" :
          lyr instanceof ShapeLayer ? "shape" :
          lyr instanceof CameraLayer ? "camera" :
          lyr instanceof LightLayer ? "light" : "av",
    enabled: lyr.enabled,
    inPoint: lyr.inPoint,
    outPoint: lyr.outPoint,
    hasVideo: lyr.hasVideo,
    hasAudio: lyr.hasAudio
  });
}
JSON.stringify({layers: layers});
```

### Find Expression Errors
```javascript
var errors = [];
for (var i = 1; i <= comp.numLayers; i++) {
  var lyr = comp.layer(i);
  // Check transform properties
  var props = ["Position", "Scale", "Rotation", "Opacity"];
  for (var p = 0; p < props.length; p++) {
    try {
      var prop = lyr.property("ADBE Transform Group").property(props[p]);
      if (prop.expressionEnabled && prop.expressionError !== "") {
        errors.push({layer: lyr.name, property: props[p], error: prop.expressionError});
      }
    } catch(e) {}
  }
}
JSON.stringify({expressionErrors: errors});
```

### Check Interpolation Types (Linear Detection)
```javascript
var linearKeys = [];
for (var i = 1; i <= comp.numLayers; i++) {
  var lyr = comp.layer(i);
  var pos = lyr.property("ADBE Transform Group").property("ADBE Position");
  for (var k = 1; k <= pos.numKeys; k++) {
    if (pos.keyOutInterpolationType(k) == KeyframeInterpolationType.LINEAR) {
      linearKeys.push({layer: lyr.name, keyIndex: k, time: pos.keyTime(k)});
    }
  }
}
JSON.stringify({linearKeyframes: linearKeys});
```

## Render Queue

### Add to Render Queue
```javascript
var rqItem = app.project.renderQueue.items.add(comp);
// Set output module (use existing template):
rqItem.outputModule(1).applyTemplate("H.264 - Match Render Settings - 15 Mbps");
// Set output path:
rqItem.outputModule(1).file = new File("/path/to/output.mp4");
```

**Note:** Do NOT call `app.project.renderQueue.render()` from script — it blocks AE UI until complete. Instead, queue items and instruct user to start render, or use `aerender` command-line tool for batch rendering.

## Batch Operation Safety

```javascript
// Suppress dialogs for batch operations:
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;

// Restore after:
app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
```

## Known Gotchas

- **1-based everything**: `item(1)`, `layer(1)`, `key(1)` — index 0 throws errors
- **Color values 0-1**: RGB values are 0.0 to 1.0, not 0-255
- **No keyframe objects**: Access via `prop.keyValue(index)`, `prop.keyTime(index)`
- **Property dimensions**: Position is `[x,y]` or `[x,y,z]`. Ease arrays must match dimension count.
- **Script string escaping**: Quotes inside `script_string` must be escaped or use alternating quote types
- **Object invalidation**: After deleting items, re-fetch collection references
