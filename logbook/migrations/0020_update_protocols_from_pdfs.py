"""
Update FAST and Lung Ultrasound protocols with PDF-accurate content;
add AAA and OB POCUS protocols using the same heading structure.
"""
from django.db import migrations


# ---------------------------------------------------------------------------
# FAST (Abdominal) — from FAST.pdf
# ---------------------------------------------------------------------------
FAST_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid var(--medical-primary);">
  <div class="card-header" style="background-color: var(--medical-primary); color: white;">
    <h4 class="mb-0"><i class="fas fa-search me-2"></i>Focused Assessment with Sonography in Trauma (Abdominal FAST)</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Rapid bedside assessment for free intraperitoneal fluid in trauma patients. A negative scan only rules out significant hemoperitoneum (&gt;250 ml) at one specific moment in time.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Curvilinear</li>
          <li class="mb-2"><strong>Preset:</strong> Abdominal / FAST</li>
          <li class="mb-2"><strong>Depth:</strong> 20 cm or machine max</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Gain:</strong> Mid-range</li>
          <li class="mb-2"><strong>Orientation:</strong> Longitudinal, indicator cephalad (upper quadrants)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">Upper Quadrants — External landmark: mid to posterior axillary line at level of xiphoid | Internal landmark: kidney</p>
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-ruq1"><label class="form-check-label" for="fast-ruq1">RUQ — sweep hepatorenal interface</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-ruq2"><label class="form-check-label" for="fast-ruq2">RUQ — caudal tip of liver <span class="badge bg-primary ms-1">Most sensitive site</span></label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-luq1"><label class="form-check-label" for="fast-luq1">LUQ — sweep splenorenal interface</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-luq2"><label class="form-check-label" for="fast-luq2">LUQ — slide cephalad to subdiaphragmatic space <span class="badge bg-primary ms-1">Most likely LUQ site</span></label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-pelvis1"><label class="form-check-label" for="fast-pelvis1">Pelvis (longitudinal) — rectovesical pouch (M) / rectouterine pouch (F)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-pelvis2"><label class="form-check-label" for="fast-pelvis2">Pelvis (transverse) — sweep from seminal vesicles (M) / vaginal stripe (F)</label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-lightbulb me-2"></i><strong>Tip:</strong> The kidney does not define the interface — the solid organ does (including the caudal tip). Slide posteriorly/anteriorly to find the best window.
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i>No anechoic free fluid at the caudal tip of the liver (hepatorenal interface)</li>
      <li><i class="fas fa-check text-success me-2"></i>No free fluid in the subdiaphragmatic space (LUQ)</li>
      <li><i class="fas fa-check text-success me-2"></i>No free fluid in the rectovesical or rectouterine pouch (pelvis)</li>
      <li><i class="fas fa-check text-success me-2"></i>Kidney clearly visualized as internal landmark in both upper quadrant views</li>
      <li><i class="fas fa-check text-success me-2"></i>Bladder visualized as internal landmark for pelvic views</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Anechoic stripe at caudal tip of liver (hemoperitoneum)</li>
          <li>Free fluid in subdiaphragmatic space (LUQ)</li>
          <li>Free fluid posterior to bladder in pelvis</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Ascites, urine, dialysate, or intraluminal bowel fluid (mimics)</li>
          <li>Stomach wall mistaken for diaphragm (LUQ)</li>
          <li>Seminal vesicles (bow-tie) or prostate mistaken for free fluid (pelvis)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">Image Interpretation</p>
    <ul>
      <li>Mistaking perinephric fat, blood vessels, gallbladder, or stomach contents for free fluid</li>
      <li>Mistaking other fluids for blood — ascites, urine, dialysate, intraluminal bowel fluid</li>
      <li>Attempting to interpret an interface obscured by a persistent rib shadow</li>
      <li>Misidentifying seminal vesicles (bow-tie appearance) or prostate as pelvic free fluid</li>
    </ul>
    <p class="mb-2 fw-bold">Clinical Integration</p>
    <ul class="mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Assuming absence of free fluid rules out solid organ, hollow viscus, or vascular injury</li>
      <li><i class="fas fa-times text-warning me-2"></i>Only rules out significant hemoperitoneum (&gt;250 ml) in one specific moment in time</li>
      <li><i class="fas fa-times text-warning me-2"></i>Not repeating the scan in high-risk trauma patients</li>
      <li><i class="fas fa-times text-warning me-2"></i>Assuming all free fluid is blood — free fluid is not always hemoperitoneum</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Abdominal FAST performed, curvilinear probe, abdominal/FAST preset, depth 20cm.<br>
      RUQ: No free fluid at hepatorenal interface or caudal tip of liver.<br>
      LUQ: No free fluid at splenorenal interface or subdiaphragmatic space.<br>
      Pelvis: No free fluid in rectovesical/rectouterine pouch.<br>
      <strong>Impression: Negative abdominal FAST. Significant hemoperitoneum (&gt;250 ml) excluded at time of scan.</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">Quiz 8 — Abdominal FAST Exam</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-tasks me-2"></i><strong>Skills Checklist:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/scans/">Log FAST Scans</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""

# ---------------------------------------------------------------------------
# Pneumothorax / Lung Ultrasound — from Pneumothorax.pdf
# ---------------------------------------------------------------------------
LUNG_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid var(--medical-secondary);">
  <div class="card-header" style="background-color: var(--medical-secondary); color: white;">
    <h4 class="mb-0"><i class="fas fa-lungs me-2"></i>Pneumothorax POCUS</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Systematic evaluation of the pleural line for pneumothorax. Assess lung sliding, comet tails, lung pulse, and lung point in 3 pleural spaces per side.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Curvilinear or Linear <span class="badge bg-secondary ms-1">Linear = best image quality</span></li>
          <li class="mb-2"><strong>Preset:</strong> Lung / Abdomen</li>
          <li class="mb-2"><strong>Depth:</strong> 10 cm, then center pleural line</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Position:</strong> Supine</li>
          <li class="mb-2"><strong>Orientation:</strong> Longitudinal</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">External landmark: most anterior part of lung in mid-clavicular line (supine patient) | Internal landmark: ribs/rib shadows | AOI: pleural line (0.5–1.5 cm far-field of ribs)</p>
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-step1"><label class="form-check-label" for="ptx-step1">Place probe longitudinally at most anterior hemithorax (~ICS 4–5)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-step2"><label class="form-check-label" for="ptx-step2">Identify ribs/shadows (internal landmark)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-step3"><label class="form-check-label" for="ptx-step3">Identify echogenic pleural line — sweep to optimize crispness</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-step4"><label class="form-check-label" for="ptx-step4">Evaluate for lung sliding, lung pulse, comet tails in 3 pleural spaces</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-step5"><label class="form-check-label" for="ptx-step5">If all absent ≥3 resp cycles + stable: identify lung point (ant → mid → post axillary)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ptx-mmode"><label class="form-check-label" for="ptx-mmode"><em>Optional: M-mode — seashore sign (normal) vs barcode sign (PTX)</em></label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-info-circle me-2"></i><strong>Lung point search:</strong> Start at anterior axillary line → slide to mid axillary → slide to posterior axillary, stopping when lung sliding or comet tails appear.
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i><strong>Lung sliding:</strong> visceral and parietal pleura moving against each other with respiration — looks like ants sliding on a log</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Comet tails / B-lines:</strong> short white vertical lines arising from the pleural line (reverberation of US beam between visceral and parietal pleura)</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Lung pulse:</strong> cardiac pulsation transmitted to pleural line (in poorly aerated lung — atelectasis or mainstem intubation)</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Determinate negative:</strong> lung sliding OR lung pulse OR comet tails/B-lines present in most anterior rib space</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Pneumothorax findings:</p>
        <ul class="mb-2">
          <li>Absent lung sliding + absent comet tails + absent lung pulse in ≥1 rib space (≥3 resp cycles)</li>
          <li><strong>True lung point:</strong> sliding next to no sliding — 100% specific for PTX</li>
        </ul>
        <p class="mb-1 fw-bold">PTX size (supine patient):</p>
        <ul class="mb-0">
          <li>Small — lung point anteriorly (mid-clavicular to ant. axillary)</li>
          <li>Medium — lung point laterally (mid axillary line)</li>
          <li>Large — lung point posteriorly (posterior axillary line)</li>
        </ul>
      </div>
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Determinate positive scan:</p>
        <ul class="mb-0">
          <li>Stable patient: identify lung point to declare PTX</li>
          <li>Unstable patient: okay to declare PTX without finding lung point</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">False Positives (absent sliding without true PTX)</p>
    <ul>
      <li>Right mainstem intubation → look for comet tails/lung pulse in left lung</li>
      <li>Esophageal intubation (including in apneic patient or cardiac arrest)</li>
      <li>Phrenic nerve palsy (isolated absent sliding)</li>
      <li>ARDS, chronic pleurodesis (pleura adherent)</li>
      <li>Pulmonary fibrosis, large pulmonary infiltrates</li>
      <li>Pleural effusion or severe COPD with bullae (no pleura visible)</li>
      <li>Pulmonary contusions (comet tails still present; look for them)</li>
      <li>Interpreting physiologic lung point as pathologic (cardiac, splenic, gastric, liver)</li>
    </ul>
    <p class="mb-2 fw-bold">False Negatives</p>
    <ul>
      <li>Large PTX (&gt;65%) — no normal lung touching accessible pleura in supine patient</li>
      <li>Misidentifying poor hand control movement at pleural line as lung sliding</li>
    </ul>
    <p class="mb-2 fw-bold">Clinical Integration</p>
    <ul class="mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Treating for PTX based on a false positive</li>
      <li><i class="fas fa-times text-warning me-2"></i>Treating a very small PTX — some do not need a chest tube</li>
      <li><i class="fas fa-times text-warning me-2"></i>Not treating despite high clinical suspicion when scan is false negative or indeterminate</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Lung POCUS performed, [curvilinear/linear] probe, lung/abdomen preset, depth 10 cm.<br>
      Evaluated 3 pleural spaces per side in supine patient, most anterior rib space in mid-clavicular line.<br>
      Lung sliding [present/absent]. Comet tails [present/absent]. Lung pulse [present/absent].<br>
      [No lung point identified. / True lung point identified at ___ axillary line — consistent with [small/medium/large] PTX.]<br>
      <strong>Impression: [Determinate negative — no pneumothorax. / Pneumothorax identified.]</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">Quiz 10 — Pneumothorax POCUS</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-tasks me-2"></i><strong>Skills Checklist:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/scans/">Log Lung Scans</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""

# ---------------------------------------------------------------------------
# AAA — from AAA.pdf
# ---------------------------------------------------------------------------
AAA_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid #0D9488;">
  <div class="card-header" style="background-color: #0D9488; color: white;">
    <h4 class="mb-0"><i class="fas fa-circle-notch me-2"></i>Abdominal Aortic Aneurysm (AAA) POCUS</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Bedside evaluation of the abdominal aorta from xiphoid to iliac bifurcation. Sensitivity 99%, specificity 99% for AAA detection.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Curved array (curvilinear)</li>
          <li class="mb-2"><strong>Preset:</strong> Aorta / Abdominal</li>
          <li class="mb-2"><strong>Depth:</strong> 30 cm (penetration)</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Gain:</strong> Mid-range</li>
          <li class="mb-2"><strong>Plane:</strong> Transverse (primary)</li>
          <li class="mb-2"><strong>Position:</strong> Supine, abdomen exposed</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">External landmark: xiphoid process | Internal landmark: spine (hyperechoic, acoustic shadowing) | AOI: echogenic wall of the aorta</p>
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-step1"><label class="form-check-label" for="aaa-step1">Place probe just caudal to xiphoid in transverse plane</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-step2"><label class="form-check-label" for="aaa-step2">Identify spine (internal landmark) — locate aorta immediately anterior</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-step3"><label class="form-check-label" for="aaa-step3">Center and magnify the aorta</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-step4"><label class="form-check-label" for="aaa-step4">Keep probe at 90° to skin — slide caudally to iliac bifurcation</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-step5"><label class="form-check-label" for="aaa-step5">Measure outer wall to outer wall at widest point</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="aaa-doppler"><label class="form-check-label" for="aaa-doppler"><em>Optional: Doppler confirmation of aortic pulsatility</em></label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-lightbulb me-2"></i><strong>Aorta vs IVC:</strong> Aorta is patient LEFT of IVC, non-compressible, round, thick walls, no respiratory variability, pulsatile. IVC is patient RIGHT, compressible, thinner walls, respiratory variability.
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i><strong>Normal calibre:</strong> ≤3 cm outer wall to outer wall throughout entire aorta</li>
      <li><i class="fas fa-check text-success me-2"></i>Aorta located immediately anterior to spine, usually patient left of IVC</li>
      <li><i class="fas fa-check text-success me-2"></i>Non-compressible with probe pressure (unlike IVC)</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Determinate negative:</strong> entire aorta from xiphoid to iliac bifurcation visualized, outer wall never exceeds 3 cm</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Determinant positive findings:</p>
        <ul class="mb-2">
          <li>Outer wall &gt;3 cm — scan full aorta, return to widest point and measure</li>
          <li>Most AAAs are <strong>fusiform</strong> — measure largest outer-to-outer diameter</li>
          <li><strong>Saccular aneurysm</strong> — determinant positive at any size (all treated surgically; easily overlooked — be methodical)</li>
        </ul>
      </div>
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Measurement pitfalls:</p>
        <ul class="mb-0">
          <li><strong>Chronic thrombus:</strong> measure outer wall to outer wall including the more echogenic thrombus — do not measure patent lumen only</li>
          <li><strong>Indeterminate scan:</strong> cannot visualize entire aorta from xiphoid to bifurcation (bowel gas, obesity)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">Image Interpretation</p>
    <ul>
      <li>Chronic thrombus — measuring the false (patent) lumen only instead of outer wall to outer wall</li>
      <li>Saccular aneurysms easily overlooked — scan methodically</li>
      <li>Oblique probe angle — overestimates lumen size</li>
    </ul>
    <p class="mb-2 fw-bold">Image Generation</p>
    <ul>
      <li>Not scanning in true transverse — probe not at 90° can falsely increase or decrease lumen size</li>
      <li>Scanning too fast; not starting at the xiphoid process</li>
      <li>Bowel gas obscuring ≥1 cm of aorta</li>
    </ul>
    <p class="mb-2 fw-bold">Troubleshooting Bowel Gas</p>
    <ul>
      <li>Flex hips and knees; firm probe pressure and hold</li>
      <li>Ask patient to take a deep breath in and hold / exhale</li>
      <li>Slide laterally and heel medially to move around loops of bowel</li>
    </ul>
    <p class="mb-2 fw-bold">Clinical Integration</p>
    <ul class="mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Assuming a AAA &lt;5 cm cannot rupture</li>
      <li><i class="fas fa-times text-warning me-2"></i>Assuming debris in AAA represents thrombus and therefore means acute rupture</li>
      <li><i class="fas fa-times text-warning me-2"></i>Declaring a negative scan without having visualized the entire aorta</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Abdominal aortic ultrasound performed, curved array probe, aorta/abdominal preset, depth 30 cm.<br>
      Aorta visualized from xiphoid process to iliac bifurcation in transverse plane.<br>
      Maximum outer wall diameter: ___ cm. No portion exceeds 3 cm outer wall to outer wall.<br>
      [Chronic thrombus present — measured outer wall to outer wall including thrombus.]<br>
      <strong>Impression: [Determinant negative AAA scan. / AAA identified, max diameter ___ cm.]</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">Quiz 7 — Abdominal Aortic Aneurysm</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-tasks me-2"></i><strong>Skills Checklist:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/scans/">Log AAA Scans</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""

# ---------------------------------------------------------------------------
# OB POCUS — from OBs.pdf
# ---------------------------------------------------------------------------
OB_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid #7C3AED;">
  <div class="card-header" style="background-color: #7C3AED; color: white;">
    <h4 class="mb-0"><i class="fas fa-baby-carriage me-2"></i>OB POCUS — First Trimester (3-2-1 Rule)</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Evaluation of first-trimester pain and bleeding. Goal: <strong>rule in</strong> an intrauterine pregnancy. You cannot absolutely rule out an ectopic pregnancy.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Curvilinear</li>
          <li class="mb-2"><strong>Preset:</strong> OB</li>
          <li class="mb-2"><strong>Depth:</strong> 15 cm</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Gain:</strong> Mid-range</li>
          <li class="mb-2"><strong>Requirement:</strong> Full bladder (acoustic window to see uterus)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">External landmark: cephalad to symphysis pubis | Internal landmark: bladder | AOI: uterus / endometrial stripe</p>
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step1"><label class="form-check-label" for="ob-step1">Probe midline, longitudinal, immediately cephalad to symphysis pubis</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step2"><label class="form-check-label" for="ob-step2">Heel probe caudally — bladder to top right of screen; uterus appears farfield</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step3"><label class="form-check-label" for="ob-step3">Center uterus; identify endometrial stripe (higher echogenicity = AOI)</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step4"><label class="form-check-label" for="ob-step4">Sweep uterus longitudinally — should appear as elongated pear</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step5"><label class="form-check-label" for="ob-step5">Rotate 90° — sweep transversely (start from vaginal stripe)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="ob-step6"><label class="form-check-label" for="ob-step6">Confirm 3-2-1 criteria (see below)</label></div>
      </div>
    </div>
    <div class="alert alert-primary mt-3 mb-0">
      <i class="fas fa-ruler me-2"></i><strong>3-2-1 Rule for IUP:</strong>
      <ul class="mb-0 mt-1">
        <li><strong>3 Pregnancy Criteria</strong> (need all): decidual reaction + gestational sac + yolk sac OR fetal pole with fetal heart</li>
        <li><strong>2 Intrauterine Criteria</strong> (need both): bladder-uterine juxtaposition + vaginal-uterine continuity (in longitudinal view)</li>
        <li><strong>1 Safety Criterion</strong>: myometrial mantle ≥5 mm (shortest distance from inner GS edge to outer uterus edge)</li>
      </ul>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i><strong>Decidual reaction:</strong> strongly echogenic (white) lining — forms ~14 days post-fertilization</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Gestational sac:</strong> anechoic (black) area contained within the decidual reaction</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Yolk sac / double ring sign:</strong> yolk sac within gestational sac = earliest definitive IUP sign (visible by 5.5 wks TVUS / 6.5 wks ABUS)</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Fetal pole:</strong> visible by 6 wks TVUS / 7–8 wks ABUS; FHR &gt;100 bpm required for good outcome</li>
      <li><i class="fas fa-check text-success me-2"></i><strong>Myometrial mantle:</strong> ≥5 mm (inner GS edge to outer uterine edge)</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Pregnancy Failure Criteria:</p>
        <ul class="mb-0">
          <li>No gestational sac with BhCG &gt;3000 (transabdominal) or &gt;1500 (transvaginal)</li>
          <li>No yolk sac with gestational sac &gt;15 mm</li>
          <li>No fetal pole with gestational sac &gt;25 mm</li>
          <li>CRL &gt;5–7 mm with no fetal heart rate</li>
          <li>No FHR after 10–12 weeks gestational age</li>
        </ul>
      </div>
      <div class="col-md-6">
        <p class="mb-1 fw-bold">Other findings:</p>
        <ul class="mb-0">
          <li>Free fluid in recto-uterine or vesico-uterine spaces</li>
          <li>Myometrial mantle &lt;5 mm — unsafe IUP location</li>
          <li>3-2-1 criteria not fully met — cannot confirm IUP</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <p class="mb-2 fw-bold">Image Interpretation</p>
    <ul>
      <li>Mistaking a pseudo-gestational sac for a true gestational sac (confirming IUP without all 3 pregnancy criteria)</li>
      <li>Failure to demonstrate bladder/uterine juxtaposition</li>
      <li>Mistaking maternal blood flow in the decidual reaction for fetal cardiac activity</li>
    </ul>
    <p class="mb-2 fw-bold">Clinical Integration</p>
    <ul class="mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Assuming IUP despite 3-2-1 rule not being fully met</li>
      <li><i class="fas fa-times text-warning me-2"></i>Mistaking physiologic fluid for blood</li>
      <li><i class="fas fa-times text-warning me-2"></i>Assuming free fluid in the pelvis is physiologic</li>
      <li><i class="fas fa-times text-warning me-2"></i>Declaring safe IUP when no yolk sac is visible and presumed fetal pole has no obvious fetal heart</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Transabdominal pelvic ultrasound performed, curvilinear probe, OB preset, depth 15 cm. Full bladder used as acoustic window.<br>
      Uterus visualized in longitudinal and transverse planes. Endometrial stripe identified.<br>
      3-2-1 criteria: Decidual reaction [present/absent]. Gestational sac [present/absent — ___ mm]. Yolk sac [present/absent].<br>
      Bladder-uterine juxtaposition: [confirmed]. Vaginal-uterine continuity: [confirmed].<br>
      Myometrial mantle: ___ mm. Fetal heart rate: ___ bpm [if applicable].<br>
      No free fluid identified in recto-uterine / vesico-uterine spaces.<br>
      <strong>Impression: [IUP confirmed by 3-2-1 rule. / 3-2-1 criteria not met — cannot confirm IUP. / Cannot exclude ectopic pregnancy.]</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">Quiz 9 — OB POCUS &amp; 3-2-1 Rule</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-tasks me-2"></i><strong>Skills Checklist:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/scans/">Log OB Scans</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""


def update_protocols(apps, schema_editor):
    POCUSProtocol = apps.get_model("logbook", "POCUSProtocol")

    # Update FAST protocol
    POCUSProtocol.objects.filter(tab_id="fast").update(
        name="Abdominal FAST",
        description=(
            "Rapid bedside assessment for free intraperitoneal fluid in trauma patients. "
            "A negative scan only rules out significant hemoperitoneum (>250 ml) at one specific moment in time."
        ),
        content=FAST_CONTENT.strip(),
    )

    # Update Lung protocol with Pneumothorax PDF content
    POCUSProtocol.objects.filter(tab_id="lung").update(
        name="Pneumothorax POCUS",
        description=(
            "Systematic evaluation of the pleural line for pneumothorax — lung sliding, "
            "comet tails, lung pulse, and lung point in 3 pleural spaces per side."
        ),
        content=LUNG_CONTENT.strip(),
        icon_class="fas fa-lungs",
    )

    # Add AAA protocol (order=4 — after existing three)
    POCUSProtocol.objects.get_or_create(
        tab_id="aaa",
        defaults={
            "name": "AAA",
            "icon_class": "fas fa-circle-notch",
            "description": (
                "Bedside evaluation of the abdominal aorta from xiphoid to iliac bifurcation "
                "for aneurysm detection. Sensitivity and specificity 99%."
            ),
            "content": AAA_CONTENT.strip(),
            "order": 4,
            "is_published": True,
        },
    )

    # Add OB POCUS protocol (order=5)
    POCUSProtocol.objects.get_or_create(
        tab_id="ob",
        defaults={
            "name": "OB POCUS",
            "icon_class": "fas fa-baby-carriage",
            "description": (
                "First-trimester evaluation using the 3-2-1 rule to rule in an intrauterine pregnancy "
                "and assess for pregnancy failure. Cannot absolutely rule out ectopic pregnancy."
            ),
            "content": OB_CONTENT.strip(),
            "order": 5,
            "is_published": True,
        },
    )


def reverse_update(apps, schema_editor):
    POCUSProtocol = apps.get_model("logbook", "POCUSProtocol")
    # Remove newly added protocols
    POCUSProtocol.objects.filter(tab_id__in=["aaa", "ob"]).delete()
    # Cannot safely restore old FAST/Lung content — leave as-is


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0019_reseed_aaa_fast_obs_pnx_from_pdfs"),
    ]

    operations = [
        migrations.RunPython(update_protocols, reverse_update),
    ]
