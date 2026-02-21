Here is the implementation-ready schema for timing and spacing primitives, derived strictly from the provided source text.

### 1\) JSON Schema: Animation Primitives

{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "AnimationPrimitives",  
  "description": "Atomic timing and spacing logic for a 2D animation coding agent.",  
  "definitions": {  
    "TimingBeat": {  
      "type": "object",  
      "description": "The temporal duration of a specific action state.",  
      "properties": {  
        "action\_type": {  
          "type": "string",  
          "enum": \["fast\_reaction", "normal\_gesture", "heavy\_effort", "contemplative"\],  
          "description": "Determines the baseline frame count range."  
        },  
        "duration\_frames": {  
          "type": "integer",  
          "description": "Absolute duration in frames (at 24fps).",  
          "minimum": 2  
        }  
      },  
      "required": \["action\_type", "duration\_frames"\]  
    },  
    "Hold": {  
      "type": "object",  
      "description": "A static or semi-static pose maintained for readability.",  
      "properties": {  
        "duration\_frames": {  
          "type": "integer",  
          "minimum": 3,  
          "description": "Must meet 3-frame readability floor."  
        },  
        "type": {  
          "type": "string",  
          "enum": \["dead\_hold", "moving\_hold"\],  
          "description": "'Dead' is perfectly static; 'Moving' includes subtle drift/traceback."  
        },  
        "drift\_amplitude": {  
          "type": "number",  
          "description": "Pixel or degree variance allowed during a moving hold to keep character 'alive'."  
        }  
      }  
    },  
    "EaseCurve": {  
      "type": "object",  
      "description": "The mathematical function governing spacing between keyframes.",  
      "properties": {  
        "curve\_type": {  
          "type": "string",  
          "enum": \["linear", "step", "bezier\_cubic", "gravity\_odd\_rule"\]  
        },  
        "bezier\_control\_points": {  
          "type": "array",  
          "items": { "type": "number" },  
          "minItems": 4,  
          "maxItems": 4,  
          "description": "\[x1, y1, x2, y2\] coordinates for the graph editor."  
        },  
        "chart\_strategy": {  
          "type": "string",  
          "enum": \["halves", "thirds", "favors"\],  
          "description": "Traditional breakdown strategy for placing in-betweens."  
        }  
      }  
    },  
    "Overshoot": {  
      "type": "object",  
      "description": "Moving past the target value before returning, to indicate mass/velocity.",  
      "properties": {  
        "target\_value": { "type": "number" },  
        "peak\_value": {   
          "type": "number",  
          "description": "The maximum value reached past the target (Extreme)."  
        },  
        "return\_frames": {  
          "type": "integer",  
          "description": "Frames required to return from Peak to Target."  
        }  
      }  
    },  
    "Settle": {  
      "type": "object",  
      "description": "The deceleration phase into a final pose.",  
      "properties": {  
        "duration\_frames": { "type": "integer" },  
        "cushion\_type": {  
          "type": "string",  
          "enum": \["ease\_out", "dampened\_oscillation"\],  
          "description": "Standard slow-out or a spring-like wobble."  
        }  
      }  
    },  
    "FollowThrough": {  
      "type": "object",  
      "description": "The lag of secondary parts (hair, cloth, child joints) behind the main driver.",  
      "properties": {  
        "parent\_joint": { "type": "string" },  
        "child\_joint": { "type": "string" },  
        "frame\_offset": {  
          "type": "integer",  
          "description": "Delay in frames for the child joint to replicate the parent's motion curve."  
        },  
        "drag\_magnitude": { "type": "number" }  
      }  
    },  
    "ArcConstraint": {  
      "type": "object",  
      "description": "Geometric path constraint ensuring organic movement.",  
      "properties": {  
        "apex\_frame\_index": {   
            "type": "integer",  
            "description": "The frame number where the arc reaches its peak."  
        },  
        "breakdown\_rule": {  
          "type": "string",  
          "enum": \["fourth\_down\_at\_half\_time", "geometric\_center"\],  
          "description": "Algorithm for placing the passing position."  
        }  
      }  
    }  
  }  
}

### 2\) Parameter Defaults & Ranges

**TimingBeat (Duration at 24fps)**

* **Fast Reaction:** 2–4 frames.  
* *Rationale:* Used for surprise, impact, or shock 1\.  
* **Normal Gesture:** 8–12 frames.  
* *Rationale:* Standard for casual conversation/human movement 1\.  
* **Heavy Effort:** 16–24 frames.  
* *Rationale:* Suggests mass, fatigue, or deliberation 1\.  
* **Golden Key Hold:** 6–12 frames.  
* *Rationale:* Required duration for an audience to read a main attitude pose 2\.  
* **Readability Floor:** Minimum 3 frames.  
* *Rationale:* Any hold shorter than this may not register to the human brain 3, 4\.

**Spacing & Easing**

* **Gravity Acceleration:** 1:3:5:7 ratio.  
* *Rationale:* The "Odd Rule." Displacement increases by odd numbers from the apex 5\.  
* **Standard Breakdown (Arc):** "Fourth Down at Half Time."  
* *Rationale:* At 50% of the duration, the object should be 25% down from the apex vertically (3/4 of total height) 6, 7\.

**Offset (Follow Through)**

* **Joint Offset:** 1–3 frames.  
* *Rationale:* Child joints (elbows/wrists) should lag behind parent joints (shoulders) to avoid robotic motion 8, 3\.  
* **Viseme/Face Lag:** 8–12 frames (approx).  
* *Rationale:* The face may lead the body, or the head may turn leaving the face pointing at the camera for 8-12 frames before whipping to catch up 9\.

### 3\) Primitives: Filled Examples

#### A. TimingBeat: The "Shock" Reaction

* **Context:** A character touches a hot stove.  
* **Data:**  
* {  
*   "primitive": "TimingBeat",  
*   "action\_type": "fast\_reaction",  
*   "duration\_frames": 3  
* }  
* **Citation:** "Fast Reaction: 2-4 frames... Surprise, impact, or sudden shock." 1\.

#### B. Hold: The "Thinking" Pause

* **Context:** A character pauses to consider an option.  
* **Data:**  
* {  
*   "primitive": "Hold",  
*   "duration\_frames": 12,  
*   "type": "moving\_hold",  
*   "drift\_amplitude": 0.02  
* }  
* **Citation:** "My main circled 'Golden' keys... usually giving them a value of between 6 to 12 frames... Moving hold... adding subtle drag... extending the duration." 2, 10\.

#### C. EaseCurve: The Falling Anvil

* **Context:** An object dropping from a dead stop (apex).  
* **Data:**  
* {  
*   "primitive": "EaseCurve",  
*   "curve\_type": "gravity\_odd\_rule",  
*   "chart\_strategy": "slow\_out"  
* }  
* **Citation:** "For a falling object, the spacings follow a simple pattern... the 'Odd Rule'... ratios 1:3:5:7." 5\.

#### D. Overshoot: The Head Stop

* **Context:** A character's body stops moving, but the head continues briefly.  
* **Data:**  
* {  
*   "primitive": "Overshoot",  
*   "target\_value": 0.0,  
*   "peak\_value": 5.0,  
*   "return\_frames": 4  
* }  
* **Citation:** "The head will go slightly beyond its final resting-place and then come back to a stop... Extremities of the body go beyond." 11\.

#### E. FollowThrough: The Arm Drag

* **Context:** Shoulders rotate, dragging the arm.  
* **Data:**  
* {  
*   "primitive": "FollowThrough",  
*   "parent\_joint": "shoulder",  
*   "child\_joint": "elbow",  
*   "frame\_offset": 2  
* }  
* **Citation:** "Make one of the arms slightly later than the other... offset the arm swing." 8, 12\.

#### F. ArcConstraint: The Bouncing Ball

* **Context:** Calculating the position of a ball at the halfway point of a bounce.  
* **Data:**  
* {  
*   "primitive": "ArcConstraint",  
*   "apex\_frame\_index": 12,  
*   "breakdown\_rule": "fourth\_down\_at\_half\_time"  
* }  
* **Citation:** "Fourth Down at Half Time... at the half-time key... the ball is one foot (a fourth down) below the apex." 6, 13\.

