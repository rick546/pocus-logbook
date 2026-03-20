from django.db import migrations

FAST_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid var(--medical-primary);">
  <div class="card-header" style="background-color: var(--medical-primary); color: white;">
    <h4 class="mb-0"><i class="fas fa-search me-2"></i>Focused Assessment with Sonography in Trauma (FAST / eFAST)</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Rapid bedside assessment for free fluid in trauma patients.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Curvilinear (2-5 MHz)</li>
          <li class="mb-2"><strong>Preset:</strong> Abdominal / FAST</li>
          <li class="mb-2"><strong>Depth:</strong> 12-20 cm (adjust to visualize diaphragm + Morrison's)</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Gain:</strong> Optimize for fluid contrast</li>
          <li class="mb-2"><strong>Orientation:</strong> Indicator toward patient head (longitudinal)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-ruq1"><label class="form-check-label" for="fast-ruq1">RUQ - Morrison's pouch (hepatorenal recess)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-ruq2"><label class="form-check-label" for="fast-ruq2">RUQ - Right pleural space / diaphragm</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-luq1"><label class="form-check-label" for="fast-luq1">LUQ - Splenorenal recess</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-luq2"><label class="form-check-label" for="fast-luq2">LUQ - Left pleural space</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-pelvis"><label class="form-check-label" for="fast-pelvis">Pelvis - Pouch of Douglas / rectovesical</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-subx"><label class="form-check-label" for="fast-subx">Subxiphoid - Pericardial view</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="fast-lung"><label class="form-check-label" for="fast-lung"><em>Optional - Anterior lung (pneumothorax)</em></label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-info-circle me-2"></i><strong>Minimum acceptable study:</strong> All 4 abdominal windows + cardiac
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <p class="mb-2"><strong>No anechoic fluid in:</strong></p>
    <ul>
      <li>Morrison's pouch</li>
      <li>Splenorenal recess</li>
      <li>Pelvis</li>
    </ul>
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i>Crisp diaphragm line</li>
      <li><i class="fas fa-check text-success me-2"></i>No pericardial effusion</li>
      <li><i class="fas fa-check text-success me-2"></i>Lung sliding present bilaterally</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Free fluid in Morrison's pouch</li>
          <li>Pelvic free fluid posterior to bladder</li>
          <li>Pericardial effusion</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Hemothorax above diaphragm</li>
          <li>Absent lung sliding / lung point</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <p class="mb-2"><strong>Mistaking:</strong></p>
    <ul>
      <li>Perinephric fat for fluid</li>
      <li>Gastric fluid for hemoperitoneum</li>
      <li>Mirror artifact near diaphragm</li>
    </ul>
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Inadequate depth hides diaphragm</li>
      <li><i class="fas fa-times text-warning me-2"></i>Supine positioning underestimates pelvic fluid</li>
      <li><i class="fas fa-times text-warning me-2"></i>Early bleeds may be negative</li>
      <li><i class="fas fa-times text-warning me-2"></i>Obesity limits sensitivity</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      FAST exam performed. Adequate views obtained of RUQ, LUQ, pelvis, and subxiphoid.<br>
      No free intraperitoneal fluid identified. No pericardial effusion seen. Lung sliding present bilaterally.<br>
      Study limited by body habitus.<br>
      <strong>Impression: Negative FAST.</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-folder me-2"></i><strong>Related Cases:</strong></p>
        <ul class="list-unstyled">
          <li><a href="#">Blunt trauma hypotension</a></li>
          <li><a href="#">Penetrating trauma</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">FAST Fluid Recognition</a></li>
          <li><a href="/quizzes/">Pitfalls Quiz</a></li>
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

LUNG_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid var(--medical-secondary);">
  <div class="card-header" style="background-color: var(--medical-secondary); color: white;">
    <h4 class="mb-0"><i class="fas fa-lungs me-2"></i>Lung Ultrasound Protocol</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Systematic evaluation of lung parenchyma and pleura for pulmonary pathology.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Linear (preferred) or Curvilinear</li>
          <li class="mb-2"><strong>Preset:</strong> Lung / MSK</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Depth:</strong> 4-6 cm (pleura centered)</li>
          <li class="mb-2"><strong>Orientation:</strong> Indicator toward head</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="lung-ant-upper"><label class="form-check-label" for="lung-ant-upper">Anterior upper (R/L)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="lung-ant-lower"><label class="form-check-label" for="lung-ant-lower">Anterior lower (R/L)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="lung-lateral"><label class="form-check-label" for="lung-lateral">Lateral zones (R/L)</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="lung-posterior"><label class="form-check-label" for="lung-posterior">Posterior zones if able</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="lung-mmode"><label class="form-check-label" for="lung-mmode"><em>M-mode confirmation (optional)</em></label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-info-circle me-2"></i><strong>Minimum:</strong> 6-zone scan
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i>Lung sliding present</li>
      <li><i class="fas fa-check text-success me-2"></i>A-lines visible</li>
      <li><i class="fas fa-check text-success me-2"></i>Smooth pleural line</li>
      <li><i class="fas fa-check text-success me-2"></i>No consolidations or effusions</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <ul class="mb-0">
      <li><strong>Pneumothorax:</strong> absent sliding, barcode sign, lung point</li>
      <li><strong>Pulmonary edema:</strong> ≥3 B-lines per zone</li>
      <li><strong>Pneumonia:</strong> subpleural consolidation, shred sign</li>
      <li><strong>Pleural effusion:</strong> anechoic fluid with spine sign</li>
      <li><strong>ARDS:</strong> irregular pleura, patchy B-lines</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Mainstem intubation mimics pneumothorax</li>
      <li><i class="fas fa-times text-warning me-2"></i>Shallow breathing reduces sliding</li>
      <li><i class="fas fa-times text-warning me-2"></i>Subcutaneous emphysema blocks imaging</li>
      <li><i class="fas fa-times text-warning me-2"></i>Cardiac motion mimics sliding (lung pulse)</li>
      <li><i class="fas fa-times text-warning me-2"></i>Obesity reduces resolution</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Lung ultrasound performed with linear probe. Bilateral anterior and lateral zones visualized. Lung sliding present bilaterally with A-line pattern. No focal consolidations or pleural effusions identified.<br>
      <strong>Impression: Normal lung ultrasound.</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-folder me-2"></i><strong>Related Cases:</strong></p>
        <ul class="list-unstyled">
          <li><a href="#">Acute dyspnea</a></li>
          <li><a href="#">Trauma pneumothorax</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/">Lung Artifacts</a></li>
          <li><a href="/quizzes/">Pneumothorax Signs</a></li>
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

CARDIAC_CONTENT = """
<div class="card mb-4" style="border-left: 4px solid #E11D48;">
  <div class="card-header" style="background-color: #E11D48; color: white;">
    <h4 class="mb-0"><i class="fas fa-heart me-2"></i>Cardiac POCUS Protocol</h4>
  </div>
  <div class="card-body">
    <p class="text-muted">Focused cardiac assessment for acute presentations and hemodynamic evaluation.</p>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-sliders-h me-2"></i>Probe + Preset</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>Probe:</strong> Phased array (1-5 MHz)</li>
          <li class="mb-2"><strong>Preset:</strong> Cardiac</li>
          <li class="mb-2"><strong>Depth:</strong> 16-24 cm</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-0">
          <li class="mb-2"><strong>ECG gating:</strong> Optional</li>
          <li class="mb-2"><strong>Orientation:</strong> Indicator toward patient right</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-clipboard-list me-2"></i>Views Checklist</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="cardiac-plax"><label class="form-check-label" for="cardiac-plax">Parasternal Long Axis (PLAX)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="cardiac-psax"><label class="form-check-label" for="cardiac-psax">Parasternal Short Axis (PSAX)</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="cardiac-a4c"><label class="form-check-label" for="cardiac-a4c">Apical 4-Chamber</label></div>
      </div>
      <div class="col-md-6">
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="cardiac-subx"><label class="form-check-label" for="cardiac-subx">Subxiphoid</label></div>
        <div class="form-check mb-2"><input class="form-check-input" type="checkbox" id="cardiac-ivc"><label class="form-check-label" for="cardiac-ivc"><em>IVC (optional)</em></label></div>
      </div>
    </div>
    <div class="alert alert-info mt-3 mb-0">
      <i class="fas fa-info-circle me-2"></i><strong>Minimum:</strong> PLAX + Subxiphoid
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #D1FAE5;"><i class="fas fa-check-circle me-2" style="color: var(--medical-success);"></i>Normal Images</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-check text-success me-2"></i>Normal LV contractility</li>
      <li><i class="fas fa-check text-success me-2"></i>No pericardial effusion</li>
      <li><i class="fas fa-check text-success me-2"></i>RV smaller than LV</li>
      <li><i class="fas fa-check text-success me-2"></i>Collapsible IVC (if assessed)</li>
      <li><i class="fas fa-check text-success me-2"></i>Symmetric valve motion</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEE2E2;"><i class="fas fa-exclamation-triangle me-2" style="color: var(--medical-danger);"></i>Pathology Examples</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Pericardial effusion / tamponade</li>
          <li>RV dilation / strain</li>
          <li>Severely reduced LV function</li>
        </ul>
      </div>
      <div class="col-md-6">
        <ul class="mb-0">
          <li>Hyperdynamic LV (sepsis)</li>
          <li>Dilated cardiomyopathy</li>
          <li>Plethoric IVC</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header" style="background-color: #FEF3C7;"><i class="fas fa-exclamation-circle me-2" style="color: var(--medical-accent);"></i>Pitfalls</div>
  <div class="card-body">
    <ul class="list-unstyled mb-0">
      <li><i class="fas fa-times text-warning me-2"></i>Foreshortened apical view</li>
      <li><i class="fas fa-times text-warning me-2"></i>Mistaking epicardial fat for effusion</li>
      <li><i class="fas fa-times text-warning me-2"></i>Overestimating EF visually</li>
      <li><i class="fas fa-times text-warning me-2"></i>Lung artifact obscuring parasternal views</li>
      <li><i class="fas fa-times text-warning me-2"></i>Probe pressure collapsing IVC</li>
    </ul>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-file-medical me-2"></i>Documentation Template</div>
  <div class="card-body">
    <div class="p-3" style="background-color: var(--bg-main); border-radius: 8px; font-family: monospace; font-size: 0.9rem;">
      Cardiac POCUS performed with phased array probe. Adequate parasternal and subxiphoid views obtained. Left ventricular systolic function grossly normal. No pericardial effusion identified. Right ventricle not dilated.<br>
      <strong>Impression: No acute cardiac abnormality detected on focused exam.</strong>
    </div>
  </div>
</div>

<div class="card mb-4">
  <div class="card-header"><i class="fas fa-link me-2"></i>Related Resources</div>
  <div class="card-body">
    <div class="row">
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-folder me-2"></i><strong>Related Cases:</strong></p>
        <ul class="list-unstyled">
          <li><a href="#">Undifferentiated hypotension</a></li>
          <li><a href="#">Chest pain workup</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-brain me-2"></i><strong>Quiz Sets:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/quizzes/3/">Focused Echo Quiz</a></li>
          <li><a href="/quizzes/">Cardiac Views</a></li>
        </ul>
      </div>
      <div class="col-md-4">
        <p class="mb-1"><i class="fas fa-tasks me-2"></i><strong>Skills Checklist:</strong></p>
        <ul class="list-unstyled">
          <li><a href="/scans/">Log Cardiac Scans</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""


def seed_protocols(apps, schema_editor):
    POCUSProtocol = apps.get_model('logbook', 'POCUSProtocol')
    protocols = [
        {
            'name': 'FAST Scan',
            'tab_id': 'fast',
            'icon_class': 'fas fa-search',
            'description': 'Rapid bedside assessment for free fluid in trauma patients.',
            'content': FAST_CONTENT.strip(),
            'order': 1,
        },
        {
            'name': 'Lung Ultrasound',
            'tab_id': 'lung',
            'icon_class': 'fas fa-lungs',
            'description': 'Systematic evaluation of lung parenchyma and pleura for pulmonary pathology.',
            'content': LUNG_CONTENT.strip(),
            'order': 2,
        },
        {
            'name': 'Cardiac POCUS',
            'tab_id': 'cardiac',
            'icon_class': 'fas fa-heart',
            'description': 'Focused cardiac assessment for acute presentations and hemodynamic evaluation.',
            'content': CARDIAC_CONTENT.strip(),
            'order': 3,
        },
    ]
    for p in protocols:
        POCUSProtocol.objects.get_or_create(tab_id=p['tab_id'], defaults=p)


def unseed_protocols(apps, schema_editor):
    POCUSProtocol = apps.get_model('logbook', 'POCUSProtocol')
    POCUSProtocol.objects.filter(tab_id__in=['fast', 'lung', 'cardiac']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('logbook', '0010_pocusprotocol_resource_alter_quizquestion_key_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_protocols, unseed_protocols),
    ]
