Here is the **Structured Critique Format (SCF)** designed for the Animation Agent to evaluate generated poses. It is formatted as a JSON schema for machine processing, followed by the logic parameters for each field.

### 1\. The Critique Object Schema (JSON)

{  
  "pose\_id": "shot\_04\_frame\_12",  
  "evaluation\_timestamp": "2023-10-27T10:00:00Z",  
  "critique\_data": {  
    "silhouette\_score": {  
      "value": 0.0 to 1.0,  
      "status": "PASS/FAIL",  
      "rationale": "String",  
      "occlusion\_ratio": "Float"  
    },  
    "line\_of\_action": {  
      "type": "C-Curve" | "S-Curve" | "Broken/Z",  
      "strength": "Strong" | "Weak",  
      "notes": "String"  
    },  
    "tangents": {  
      "detected\_count": "Integer",  
      "locations": \["Vector2", "Vector2"\],  
      "severity": "High" | "Low",  
      "warnings": "String"  
    },  
    "staging\_clarity": {  
      "facial\_visibility": "Boolean",  
      "focus\_point": "Vector2",  
      "notes": "String"  
    },  
    "fix\_strategy": {  
      "priority\_action": "String",  
      "secondary\_adjustments": \["String", "String"\]  
    }  
  }  
}

### 2\. Field Logic & Validation Criteria

#### A. Silhouette Score Rationale

* **Mental Model:** The "Squint Test." Can the pose be read instantly if filled with solid black? The agent calculates the ratio of negative space to positive mass.  
* **Logic/Metric:**  
* **Binary Conversion:** Convert character mesh to a binary mask (Black/White).  
* **Occlusion Check:** Calculate Visible\_Surface\_Area of limbs vs. Torso.  
* **Fail Condition:** If limbs occlude $\>30\\%$ of the torso (creating a "blob"), the score drops below 0.5.  
* **Agent Output Example:** *"FAIL (Score: 0.4). Left arm is merged with torso mass. Negative space windows are closed."*  
* **Sources:**  
* "Check Visible\_Surface\_Area to ensure limbs are not occluding the torso." 1, 2\.  
* "Avoid 'blobs,' where limbs overlap the torso... create 'windows' of negative space." 3\.  
* "The human eye sees the outline of a shape first... action clearly seen from a character’s silhouette." 4\.

#### B. Line-of-Action Notes

* **Mental Model:** The "Invisible Spine." A single fluid stroke must connect the head to the weight-bearing foot.  
* **Logic/Metric:**  
* **Vector Fit:** Attempt to fit a Bézier curve through Head\_Centroid $\\rightarrow$ Spine $\\rightarrow$ Heel.  
* **Classification:** Identify as **C-Curve** (simple/force), **S-Curve** (grace/complex), or **Broken** (jagged/Z-shape).  
* **Thrust Check:** Does the curve align with the intended force vector?  
* **Agent Output Example:** *"Type: Broken. Spine creates a 'Z' shape against the leg. Energy flow is interrupted at the hips."*  
* **Sources:**  
* "Can a single C or S curve be drawn... If the line is broken or zigzagged, the pose is weak." 5\.  
* "Line of action is an imaginary curve... connecting every stage of an action." 6, 7\.  
* "Avoid 'broken' or disjointed posing." 8\.

#### C. Tangent Warnings

* **Mental Model:** "Depth Destruction." When two lines touch but do not overlap, the brain perceives them as being on the same plane, flattening the image.  
* **Logic/Metric:**  
* **Intersection Detect:** Identify T-junctions or shared vertices between distinct objects (e.g., Hand outline touches Shoulder outline).  
* **Depth Check:** Are the objects separated in Z-depth but touching in Screen-Space (X/Y)?  
* **Agent Output Example:** *"WARNING: 2 Tangents detected. Wrist contour touches Knee contour at x,y. Flattens depth perception."*  
* **Sources:**  
* "Identify vertices where two distinct object outlines touch at a single point." 8\.  
* "Tangents... make your drawing appear more flat (think of a picture from a church window)." 9, 10\.  
* "Avoid tangents in your pose." 11\.

#### D. Staging Clarity Notes

* **Mental Model:** "One Idea Per Shot." Direct the viewer's eye to the focal point (usually the face or the action).  
* **Logic/Metric:**  
* **Facial Triangle:** Perform a raycast from Camera $\\rightarrow$ Face. Is it obstructed by a hand or prop?  
* **Rule of Thirds:** Is the focal point (eyes/action) located near a grid intersection?  
* **Twinning (Symmetry):** Check if Left/Right limbs have identical values (Dead Robot).  
* **Agent Output Example:** *"Clarity: LOW. Hand prop obscures the mouth during dialogue. Left and Right arms are Twinned (symmetric)."*  
* **Sources:**  
* "Trace ray from Camera \-\> Face. Fail if Hand/Prop intersects ray." 8\.  
* "Clear the 'facial triangle'." 8\.  
* "Avoid 'twinning' (symmetry)... creates a rather boring and unappealing pose." 12, 13\.  
* "One main action at a time... additional actions be complementary." 14\.

#### E. Fix Suggestions

* **Mental Model:** Actionable, code-ready adjustments to resolve the flags.  
* **Logic/Metric:**  
* **Silhouette Fix:** "Move actions to the exterior silhouette."  
* **Twinning Fix:** "Offset one limb by 2–4 frames or change angle."  
* **Tangent Fix:** "Overlap clearly or separate."  
* **Agent Output Example:**  
* *Rotate Right\_Shoulder \+15deg to open silhouette.*  
* *Offset Left\_Arm timing by \-2 frames to break symmetry.*  
* *Clear prop from facial view axis.*  
* **Sources:**  
* "Move actions to the exterior silhouette." 8, 3\.  
* "Offset one side by 2-4 frames or change the angle." 5\.  
* "Overlap the lines clearly (depth) or separate them (space)." 8\.

