# Ground Truth Annotation Protocol — SP19

## 1. Objective

Create an independently annotated reference dataset for evaluating ZoneTrace event detection accuracy.

## 2. Reference Video

- Video: `intersection_v2.mp4`
- Resolution: 1280 × 720
- FPS: 24
- Total frames: 240
- Reference run: `run_22d86d30ea024aa59f30cefb230bdfcd`
- Zone configuration: Use the polygon snapshot saved in the reference run manifest.

The input video and zone configuration must match the reference manifest before annotation begins.

## 3. Event Definitions

**ZONE_ENTRY:** The first frame in which an object's bottom-center reference point is inside or on the controlled-zone boundary after being outside.

**ZONE_EXIT:** The first frame in which the reference point is outside the polygon after being inside.

**LOITERING:** The first frame at which an object has continuously occupied the zone for at least 3.0 seconds (72 frames at 24 FPS). Movement inside the zone does not reset the duration.

## 4. Annotation Rules

- Use 1-based frame numbering, matching stored ZoneTrace events.
- Assign manually maintained object identifiers, such as `obj_001`.
- Use the original video with the reference polygon overlay, without model predictions influencing the annotation.
- Label the physical event frame, not the model's delayed confirmation frame.
- Do not label initial presence inside a zone as a new entry.
- Do not interpret temporary disappearance or loss of tracking as an exit.
- Mark occluded, ambiguous, or unobservable events as uncertain rather than guessing.
- Exclude uncertain events from scoring until they have been reviewed.
- Record only `ZONE_ENTRY`, `ZONE_EXIT`, and `LOITERING` for this evaluation.

## 5. Evaluation Policy

- Initial event matching tolerance: ±3 frames.
- Events must match by type and time.
- Object-aware identity matching will be implemented in SP20.
- A single reference event must not be matched to multiple predictions.
- Precision, recall, and F1 will be reported in SP21.

## 6. Limitations

Visual object boundaries and ground-contact points may be ambiguous during occlusion or overlap.

Events whose true onset occurs before the video begins cannot always be independently established.

Annotations will be reviewed before being treated as the evaluation reference.
