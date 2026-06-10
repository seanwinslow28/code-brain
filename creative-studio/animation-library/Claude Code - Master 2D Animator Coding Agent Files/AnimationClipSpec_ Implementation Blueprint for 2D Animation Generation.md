Here is the implementation-ready specification for the AnimationClipSpec, designed for a 2D animation generation agent.

### 1\) JSON Schema: AnimationClipSpec

{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "AnimationClipSpec",  
  "description": "A structured blueprint for generating 2D animation sequences based on physics, style, and production constraints.",  
  "type": "object",  
  "required": \["fps", "duration\_frames", "action\_beats", "constraints"\],  
  "properties": {  
    "fps": {  
      "type": "integer",  
      "description": "Base playback rate. Standard is 24 for film, often 30 for video. Distinct from exposure rate (ones/twos).",  
      "default": 24,  
      "enum": \[1-3\]  
    },  
    "duration\_frames": {  
      "type": "integer",  
      "description": "Total length of the clip in frames. Enforces the 'Timing' (objective duration) of the shot."  
    },  
    "character\_rig\_assumptions": {  
      "type": "object",  
      "properties": {  
        "kinetic\_chain\_order": {  
          "type": "array",  
          "description": "Hierarchy for 'Successive Breaking of Joints'.",  
          "items": { "type": "string" },  
          "default": \["Hips", "Torso", "Shoulder", "Elbow", "Wrist"\]  
        },  
        "layer\_separation": {  
          "type": "boolean",  
          "description": "If true, treats Head/Mouth/Body as separate update layers (Cel Stacking).",  
          "default": false  
        },  
        "power\_center\_node": {  
          "type": "string",  
          "description": "The origin point of velocity/force (e.g., 'Chest', 'Hips')."  
        }  
      }  
    },  
    "shot\_context": {  
      "type": "object",  
      "properties": {  
        "camera\_move\_velocity": {  
          "type": "number",  
          "description": "If \> 0, forces exposure on 'Ones' to prevent strobing."  
        },  
        "framing": {  
          "type": "string",  
          "enum": \["close\_up", "medium", "wide"\],  
          "description": "Affects readability thresholds (hold durations)."  
        }  
      }  
    },  
    "style\_profile\_id": {  
      "type": "string",  
      "enum": \["full\_feature", "limited\_tv", "rubber\_hose", "anime\_modulation", "spider\_verse\_stepped"\],  
      "description": "Determines the physics engine and imperfection algorithms."  
    },  
    "constraints": {  
      "type": "object",  
      "properties": {  
        "exposure\_rate": {  
          "type": "integer",  
          "enum": \[4-7\],  
          "description": "1 \= Ones (24fps), 2 \= Twos (12fps). Controls 'texture' and budget."  
        },  
        "static\_ratio\_target": {  
          "type": "number",  
          "description": "Target percentage of screen pixels to remain static (e.g., 0.80 for Limited TV)."  
        },  
        "min\_hold\_frames": {  
          "type": "integer",  
          "description": "Minimum duration for a pose to ensure readability.",  
          "default": 6  
        }  
      }  
    },  
    "action\_beats": {  
      "type": "array",  
      "description": "Ordered list of key moments (Keyframes/Extremes) and their transition logic.",  
      "items": {  
        "type": "object",  
        "properties": {  
          "frame\_index": { "type": "integer" },  
          "pose\_type": {  
            "type": "string",  
            "enum": \["key", "breakdown", "anticipation", "overshoot", "moving\_hold"\]  
          },  
          "spacing\_curve": {  
            "type": "string",  
            "enum": \["linear", "ease\_in", "ease\_out", "odd\_rule\_gravity", "stepped"\]  
          },  
          "smear\_flag": {  
            "type": "boolean",  
            "description": "If true, applies geometry deformation or multiples for this frame."  
          }  
        },  
        "required": \["frame\_index", "pose\_type"\]  
      }  
    }  
  }  
}

### 2\) Field Specifications: Logic & Citations

#### A. fps (Base Frame Rate)

* **Purpose:** Establishes the timebase for the physics engine.  
* **Constraints:** Must align with the output medium (24 for film, 25 for PAL, 30 for NTSC).  
* **Citation:** "Animation is shot on 24 frames per second... digital video is often recorded at 30 fps." 8, 9\. "Timing is the objective quality of the motion, measured by the clock and the frame count." 10\.

#### B. constraints.exposure\_rate (Ones/Twos)

* **Purpose:** Defines the *texture* of motion and production cost.  
* **Logic:**  
* **Ones (1):** High fidelity, fast action, camera pans. "Use for fast or very smooth actions." 11\. "When the camera is panning... add in single inbetweens so it doesn't strobe." 12\.  
* **Twos (2):** Standard acting. "Twos work well for most actions... half as much work." 11, 13\.  
* **Threes (3):** Limited animation/Anime style. "Slightly jerky, stylized." 14\.  
* **Citation:** "On Ones \= 24 drawings per second... On Twos \= 12 drawings per second." 8, 15\.

#### C. character\_rig\_assumptions.layer\_separation (Cel Stacking)

* **Purpose:** Enables "Planned Animation" optimization for TV budgets.  
* **Logic:** If true, the agent must separate the Static\_Body from Active\_Mouth or Active\_Eyes.  
* **Citation:** "Limited animation is based on dividing a character into as many as four cel levels... body on level 1 and the mouth on top of this on level 2." 16\. "80% static poses / 20% movement ratio." 17, 18\.

#### D. action\_beats.spacing\_curve

* **Purpose:** Defines the rhythm (spacing) between keyframes.  
* **Options:**  
* **odd\_rule\_gravity**: Used for falling objects. Spacing increases by odd numbers (1, 3, 5, 7). "I call this pattern the 'Odd Rule'... spacings from the apex go as 1, 3, 5, 7." 19, 20\.  
* **ease\_in / ease\_out**: For organic movement. "Slow in and slow out... gradually accelerating an object." 21\.  
* **Citation:** "Spacing is the subjective rhythm... distinct from Timing." 22\.

#### E. action\_beats.smear\_flag

* **Purpose:** Prevents strobing during high-velocity transits.  
* **Trigger Logic:** IF velocity \> object\_width, THEN smear\_flag \= true.  
* **Constraint:** Duration must be exactly **1 frame**. "If a smear lasts too long... it acts as a static detail rather than a burst of speed." 23\.  
* **Citation:** "When the action is too fast... the object seems to disappear strobing... bridge the gap." 24, 25\.

#### F. constraints.min\_hold\_frames

* **Purpose:** Ensures readability of poses.  
* **Constraint:** Minimum 6-12 frames for a "Golden Key" to register.  
* **Citation:** "My main circled 'Golden' keys... usually giving them a value of between 6 to 12 frames." 26\. "An action must hold for a minimum duration to be registered by the human brain." 27\.

### 3\) Filled Example Objects

#### Example 1: The "Smear Punch" (High Velocity / Feature Style)

* **Scenario:** A character throws a fast punch. High fidelity, physics-driven.  
* **Citation Basis:** "Fast Action (Reaction): 2–4 frames" 28\. "Smear duration \= 1 frame" 23\. "Ease-in/Ease-out" 29\.

{  
  "fps": 24,  
  "duration\_frames": 16,  
  "style\_profile\_id": "full\_feature",  
  "character\_rig\_assumptions": {  
    "kinetic\_chain\_order": \["Torso", "Shoulder", "Elbow", "Wrist"\],  
    "power\_center\_node": "Shoulder"  
  },  
  "constraints": {  
    "exposure\_rate": 1,   
    "min\_hold\_frames": 6  
  },  
  "action\_beats": \[  
    {  
      "frame\_index": 1,  
      "pose\_type": "anticipation",  
      "spacing\_curve": "ease\_out",  
      "description": "Arm pulls back (opposite direction of punch) \[30\]."  
    },  
    {  
      "frame\_index": 8,  
      "pose\_type": "key",  
      "spacing\_curve": "ease\_in",  
      "description": "Maximum anticipation hold."  
    },  
    {  
      "frame\_index": 9,  
      "pose\_type": "breakdown",  
      "spacing\_curve": "linear",  
      "smear\_flag": true,  
      "description": "The Punch Transit. Elongated geometry stretching from start to end position. Duration 1 frame \[23, 24\]."  
    },  
    {  
      "frame\_index": 10,  
      "pose\_type": "overshoot",  
      "spacing\_curve": "ease\_out",  
      "description": "Fist travels past target before settling \[31\]."  
    },  
    {  
      "frame\_index": 16,  
      "pose\_type": "key",  
      "spacing\_curve": "linear",  
      "description": "Final contact pose held."  
    }  
  \]  
}

#### Example 2: "Limited TV" Dialogue (Budget Optimization)

* **Scenario:** A character speaking a line. Low budget, audio-driven.  
* **Citation Basis:** "80% static / 20% moving" 18\. "Cel Stacking" 16\. "Animatic on Twos" 14\.

{  
  "fps": 24,  
  "duration\_frames": 48,  
  "style\_profile\_id": "limited\_tv",  
  "character\_rig\_assumptions": {  
    "layer\_separation": true,  
    "power\_center\_node": "Head"  
  },  
  "shot\_context": {  
    "framing": "medium",  
    "camera\_move\_velocity": 0  
  },  
  "constraints": {  
    "exposure\_rate": 2,  
    "static\_ratio\_target": 0.80,  
    "min\_hold\_frames": 12  
  },  
  "action\_beats": \[  
    {  
      "frame\_index": 1,  
      "pose\_type": "key",  
      "spacing\_curve": "stepped",  
      "description": "Body Pose A (Held). Only Mouth layer updates \[16\]."  
    },  
    {  
      "frame\_index": 24,  
      "pose\_type": "moving\_hold",  
      "spacing\_curve": "linear",  
      "description": "Subtle drift or 'traceback' on the head to keep character alive during pause \[32, 33\]."  
    },  
    {  
      "frame\_index": 36,  
      "pose\_type": "key",  
      "spacing\_curve": "stepped",  
      "description": "Body Pose B (New attitude for second half of sentence). Hard cut/pop to new pose \[34\]."  
    }  
  \]  
}  
