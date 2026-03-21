"""
Seed migration: Quiz 7 (AAA), Quiz 8 (Abdominal FAST), Quiz 9 (OB POCUS),
Quiz 10 (Pneumothorax) — MC questions + short-answer questions.
"""

from django.db import migrations


QUIZ_7_QUESTIONS = [
    dict(
        quiz_id=7, key="q1", order=1,
        section_heading="Probe & Technical Setup",
        question_text="Which ultrasound probe is best suited for AAA scanning?",
        choice_a="High-frequency linear (10–15 MHz)",
        choice_b="Phased array/cardiac probe",
        choice_c="Curvilinear low-frequency (2–5 MHz)",
        choice_d="Endocavitary probe",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The curvilinear low-frequency probe (2–5 MHz) provides adequate depth penetration "
            "to visualize the abdominal aorta, which lies deep in the abdomen. High-frequency "
            "probes lack sufficient penetration for structures this deep."
        ),
        label="AAA probe selection",
    ),
    dict(
        quiz_id=7, key="q2", order=2,
        section_heading="",
        question_text="What is the appropriate initial depth setting when scanning for AAA?",
        choice_a="5 cm",
        choice_b="10 cm",
        choice_c="15 cm",
        choice_d="Adjust until the posterior aortic wall and vertebral body are visible",
        choice_e="",
        correct_answer="D",
        explanation=(
            "Depth should be adjusted to ensure the full aorta — including the posterior wall "
            "and the hyperechoic vertebral body behind it — is visible. This confirms you are "
            "imaging the correct structure at an appropriate depth."
        ),
        label="AAA scan depth",
    ),
    dict(
        quiz_id=7, key="q3", order=3,
        section_heading="",
        question_text="What is the upper limit of normal for the abdominal aortic diameter?",
        choice_a="4 cm",
        choice_b="3 cm",
        choice_c="2 cm",
        choice_d="3.5 cm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "An abdominal aortic diameter ≥ 3 cm (measured outer wall to outer wall) is the "
            "accepted threshold for defining an AAA. Normal aortic diameter is < 3 cm."
        ),
        label="Normal aortic diameter",
    ),
    dict(
        quiz_id=7, key="q4", order=4,
        section_heading="Scanning Landmarks",
        question_text="Which external landmark is used to guide initial transverse probe placement for AAA scanning?",
        choice_a="Umbilicus",
        choice_b="Costal margin",
        choice_c="Xiphoid process",
        choice_d="Pubic symphysis",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The xiphoid process marks the approximate level of the diaphragm and is used as "
            "the superior starting point for AAA scanning. The scan then progresses caudally "
            "toward the iliac bifurcation."
        ),
        label="External landmark for AAA",
    ),
    dict(
        quiz_id=7, key="q5", order=5,
        section_heading="",
        question_text="Which internal structure is typically identified first to help locate the aorta during scanning?",
        choice_a="Renal arteries",
        choice_b="Iliac bifurcation",
        choice_c="Celiac artery or superior mesenteric artery (SMA)",
        choice_d="Inferior mesenteric artery",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The celiac artery and SMA are prominent proximal aortic branches that can be "
            "identified as internal landmarks to confirm you are imaging the aorta. They arise "
            "from the anterior surface of the aorta just below the diaphragm."
        ),
        label="Internal landmark for AAA",
    ),
    dict(
        quiz_id=7, key="q6", order=6,
        section_heading="Aorta vs. IVC",
        question_text="In a transverse cross-sectional view, where is the aorta positioned relative to the spine?",
        choice_a="To the right of the spine",
        choice_b="To the left of the spine",
        choice_c="Directly anterior to the spine",
        choice_d="Posterior to the IVC",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The aorta lies slightly to the left of midline anterior to the vertebral column. "
            "The IVC lies to the patient's right. Remembering 'aorta on the left' helps "
            "distinguish it from the IVC during scanning."
        ),
        label="Aorta vs IVC position",
    ),
    dict(
        quiz_id=7, key="q7", order=7,
        section_heading="",
        question_text="Which feature best distinguishes the aorta from the IVC on POCUS?",
        choice_a="Larger diameter",
        choice_b="Pulsatility and thicker, brighter walls",
        choice_c="Color Doppler showing bidirectional flow",
        choice_d="Position relative to the liver",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The aorta is pulsatile and has thick, echogenic walls. The IVC has thin walls, "
            "is compressible, and demonstrates respiratory variability. Color Doppler can help "
            "but pulsatility and wall thickness are the primary POCUS differentiators."
        ),
        label="Aorta vs IVC differentiation",
    ),
    dict(
        quiz_id=7, key="q8", order=8,
        section_heading="Interpretation",
        question_text="What defines a determinate negative (truly negative) AAA scan?",
        choice_a="Aorta < 2 cm in transverse diameter",
        choice_b="The entire aorta from xiphoid to iliac bifurcation is visualized with no dilation ≥ 3 cm",
        choice_c="Absence of any aneurysm in the right upper quadrant",
        choice_d="Normal IVC collapsibility on inspiration",
        choice_e="",
        correct_answer="B",
        explanation=(
            "A negative scan requires full visualization of the entire abdominal aorta from "
            "the xiphoid to the iliac bifurcation with no segment measuring ≥ 3 cm. If any "
            "portion cannot be seen, the scan is indeterminate — not negative."
        ),
        label="Determinate negative AAA scan",
    ),
    dict(
        quiz_id=7, key="q9", order=9,
        section_heading="",
        question_text="When chronic intraluminal thrombus is present in an AAA, how should the diameter be measured?",
        choice_a="From inner lumen to inner lumen (patent channel only)",
        choice_b="Excluding the thrombus from the measurement",
        choice_c="From outer wall to outer wall, including the thrombus",
        choice_d="Along the central axis only",
        choice_e="",
        correct_answer="C",
        explanation=(
            "Measuring only the patent lumen underestimates the true aortic size when thrombus "
            "is present. The correct technique is outer wall to outer wall — including any "
            "thrombus — to capture the full aortic diameter."
        ),
        label="Chronic thrombus measurement",
    ),
    dict(
        quiz_id=7, key="q10", order=10,
        section_heading="",
        question_text="What is the most common morphological type of abdominal aortic aneurysm?",
        choice_a="Saccular",
        choice_b="Fusiform",
        choice_c="False aneurysm (pseudoaneurysm)",
        choice_d="Dissecting",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Fusiform aneurysms, involving circumferential dilation of the entire vessel "
            "diameter, account for the vast majority of AAAs. Saccular aneurysms are less "
            "common and involve asymmetric outpouching of one wall."
        ),
        label="Most common AAA shape",
    ),
    dict(
        quiz_id=7, key="q11", order=11,
        section_heading="Troubleshooting",
        question_text="When overlying bowel gas obscures the aorta, which maneuver is recommended?",
        choice_a="Ask the patient to take a deep breath and hold",
        choice_b="Apply firm graded compression or use a heel-toe rocking maneuver",
        choice_c="Switch to a high-frequency linear probe",
        choice_d="Scan from a posterior approach",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Gentle but firm graded compression with the probe can displace overlying bowel "
            "gas. The heel-toe (rocking) maneuver angles the probe to find a gas-free window. "
            "These are the standard first-line troubleshooting techniques."
        ),
        label="Bowel gas troubleshooting",
    ),
    dict(
        quiz_id=7, key="q12", order=12,
        section_heading="",
        question_text="Why is it essential that the probe be perpendicular to the aorta when measuring its diameter?",
        choice_a="To improve colour Doppler sensitivity",
        choice_b="To more easily locate the renal arteries",
        choice_c="To obtain a true circular cross-section and avoid over- or underestimating the diameter",
        choice_d="To identify intramural thrombus",
        choice_e="",
        correct_answer="C",
        explanation=(
            "An oblique probe angle produces an oval cross-section of the aorta, artificially "
            "enlarging the apparent diameter. The probe must be perpendicular to obtain a true "
            "round cross-section for accurate measurement."
        ),
        label="Probe angle importance",
    ),
]


QUIZ_8_QUESTIONS = [
    dict(
        quiz_id=8, key="q1", order=1,
        section_heading="Probe & Setup",
        question_text="Which probe is preferred for the abdominal FAST exam?",
        choice_a="High-frequency linear (10–15 MHz)",
        choice_b="Phased array cardiac probe",
        choice_c="Curvilinear low-frequency (2–5 MHz)",
        choice_d="Microconvex probe",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The curvilinear low-frequency (2–5 MHz) probe provides the depth penetration "
            "needed for abdominal FAST views. The phased array may be used for the cardiac "
            "subxiphoid view but the curvilinear is the primary FAST probe."
        ),
        label="FAST probe selection",
    ),
    dict(
        quiz_id=8, key="q2", order=2,
        section_heading="",
        question_text="What is the recommended initial depth for the RUQ FAST view?",
        choice_a="5 cm",
        choice_b="10 cm",
        choice_c="16–20 cm",
        choice_d="25 cm",
        choice_e="",
        correct_answer="C",
        explanation=(
            "A depth of 16–20 cm is typically needed to visualize the full hepatorenal "
            "interface in the RUQ. This allows the right kidney and the caudal tip of the "
            "liver to be seen simultaneously."
        ),
        label="FAST scan depth",
    ),
    dict(
        quiz_id=8, key="q3", order=3,
        section_heading="Areas of Interest",
        question_text="Which location is the most sensitive for detecting free fluid in the RUQ on FAST?",
        choice_a="Perihepatic space (between liver and diaphragm)",
        choice_b="Splenorenal space",
        choice_c="Caudal tip of the liver at the hepatorenal interface (Morrison's pouch)",
        choice_d="Pelvic cul-de-sac",
        choice_e="",
        correct_answer="C",
        explanation=(
            "Morrison's pouch (hepatorenal space) is the most gravity-dependent intraperitoneal "
            "space in a supine patient. Free fluid accumulates here first, making the caudal "
            "tip of the liver the most sensitive single location for FAST."
        ),
        label="Most sensitive free fluid location",
    ),
    dict(
        quiz_id=8, key="q4", order=4,
        section_heading="",
        question_text="In the LUQ, free fluid most commonly accumulates:",
        choice_a="Around the spleen itself (perisplenic)",
        choice_b="In the left subphrenic space",
        choice_c="Between the spleen and the left kidney (splenorenal recess)",
        choice_d="Around the stomach",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The splenorenal recess is the dependent space in the LUQ for a supine patient. "
            "Free fluid collects here before accumulating in the less dependent perisplenic "
            "or subphrenic spaces."
        ),
        label="Free fluid location in LUQ",
    ),
    dict(
        quiz_id=8, key="q5", order=5,
        section_heading="",
        question_text="For the RUQ FAST view, the probe should be oriented:",
        choice_a="Transverse at the mid-axillary line",
        choice_b="Longitudinal/coronal at the posterior axillary line",
        choice_c="Transverse at the anterior axillary line",
        choice_d="Sagittal at the midline",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The RUQ view is obtained with a longitudinal (coronal) probe orientation at the "
            "posterior axillary line between the 8th and 11th intercostal spaces. This "
            "provides the best window to the hepatorenal interface."
        ),
        label="Upper quadrant probe position",
    ),
    dict(
        quiz_id=8, key="q6", order=6,
        section_heading="Interpretation",
        question_text="What is the approximate minimum volume of free fluid detectable by FAST?",
        choice_a="100 mL",
        choice_b="250 mL",
        choice_c="500 mL",
        choice_d="1000 mL",
        choice_e="",
        correct_answer="B",
        explanation=(
            "FAST has been shown to detect as little as 250 mL of free peritoneal fluid in "
            "experienced hands, though sensitivity improves with larger volumes. Below this "
            "threshold, free fluid may not be visible."
        ),
        label="Minimum fluid volume detectable",
    ),
    dict(
        quiz_id=8, key="q7", order=7,
        section_heading="",
        question_text="A negative FAST exam does NOT exclude which of the following?",
        choice_a="Massive hemoperitoneum (>1 L)",
        choice_b="Pericardial effusion",
        choice_c="Solid organ injury or hollow viscus injury without hemoperitoneum",
        choice_d="Large pleural effusion",
        choice_e="",
        correct_answer="C",
        explanation=(
            "FAST detects free fluid, not organ injury itself. Solid organ lacerations with "
            "contained bleeding, and hollow viscus injuries without significant hemorrhage, "
            "will not be detected by FAST. A negative FAST does not exclude injury."
        ),
        label="Negative FAST limitations",
    ),
    dict(
        quiz_id=8, key="q8", order=8,
        section_heading="",
        question_text="The key internal landmark for the RUQ FAST view is:",
        choice_a="The interface between the right kidney and the psoas muscle",
        choice_b="The diaphragm–liver interface",
        choice_c="The hepatorenal interface (Morrison's pouch)",
        choice_d="The right subphrenic space",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The hepatorenal interface — where the liver and right kidney lie adjacent — is "
            "the primary target of the RUQ FAST view. Free fluid appears as an anechoic "
            "stripe between these two structures."
        ),
        label="Upper quadrant internal landmark",
    ),
    dict(
        quiz_id=8, key="q9", order=9,
        section_heading="Pelvic View",
        question_text="In male patients, the area of interest for the pelvic FAST view is:",
        choice_a="Anterior to the bladder",
        choice_b="Posterior to the bladder (rectovesical pouch)",
        choice_c="Superior to the pubic symphysis",
        choice_d="Perisplenic region",
        choice_e="",
        correct_answer="B",
        explanation=(
            "In males, free fluid accumulates posterior to the bladder in the rectovesical "
            "pouch (pouch of Douglas equivalent). In females, the rectouterine pouch "
            "(pouch of Douglas) posterior to the uterus is the key location."
        ),
        label="Pelvic AOI in males",
    ),
    dict(
        quiz_id=8, key="q10", order=10,
        section_heading="",
        question_text="Trendelenburg positioning during the pelvic FAST view is used to:",
        choice_a="Reduce bowel gas artifact in the pelvis",
        choice_b="Improve IVC collapsibility assessment",
        choice_c="Encourage pooling of small amounts of free fluid toward the pelvis",
        choice_d="Improve acoustic window through the full bladder",
        choice_e="",
        correct_answer="C",
        explanation=(
            "Trendelenburg positioning (head down) causes peritoneal fluid to move by gravity "
            "toward the pelvis, concentrating even small volumes near the pelvic floor and "
            "improving sensitivity for small amounts of free fluid."
        ),
        label="Trendelenburg position indication",
    ),
    dict(
        quiz_id=8, key="q11", order=11,
        section_heading="Pitfalls",
        question_text="Which of the following is a recognized pitfall in FAST interpretation?",
        choice_a="Large hemoperitoneum is always visible on FAST",
        choice_b="Pelvic structures such as seminal vesicles can be mistaken for free fluid",
        choice_c="Free fluid is always completely anechoic",
        choice_d="Solid organs cannot be visualized with FAST",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Seminal vesicles in males appear as hypoechoic structures posterior to the bladder "
            "and can mimic free fluid. Careful identification of their characteristic bow-tie "
            "shape and bilateral symmetry helps avoid this pitfall."
        ),
        label="FAST interpretation pitfall",
    ),
]


QUIZ_9_QUESTIONS = [
    dict(
        quiz_id=9, key="q1", order=1,
        section_heading="The 3-2-1 Rule",
        question_text="According to the 3-2-1 rule for IUP confirmation, how many pregnancy criteria must be identified?",
        choice_a="1",
        choice_b="2",
        choice_c="3",
        choice_d="4",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The '3' in the 3-2-1 rule refers to 3 pregnancy criteria: decidual reaction, "
            "gestational sac, and yolk sac (or fetal pole). All three must be identified "
            "within the uterus along with the 2 intrauterine criteria and 1 safety criterion."
        ),
        label="Number of pregnancy criteria in 3-2-1 rule",
    ),
    dict(
        quiz_id=9, key="q2", order=2,
        section_heading="",
        question_text="The decidual reaction typically first appears on transvaginal ultrasound at approximately:",
        choice_a="3 weeks gestational age",
        choice_b="4–5 weeks gestational age",
        choice_c="6–7 weeks gestational age",
        choice_d="8 weeks gestational age",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The decidual reaction — echogenic thickening of the endometrium in response to "
            "pregnancy — is typically visible by transvaginal ultrasound around 4–5 weeks "
            "gestational age. It precedes visualization of the gestational sac."
        ),
        label="Decidual reaction timing",
    ),
    dict(
        quiz_id=9, key="q3", order=3,
        section_heading="",
        question_text="The earliest definitive ultrasound sign of an intrauterine pregnancy is:",
        choice_a="Cardiac activity",
        choice_b="Crown-rump length measurement",
        choice_c="A yolk sac within a gestational sac",
        choice_d="A fetal pole",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The yolk sac is the first definitive structure that confirms an intrauterine "
            "pregnancy. A gestational sac alone can be confused with a pseudogestational sac "
            "in ectopic pregnancy — the yolk sac confirms true IUP."
        ),
        label="Earliest definitive IUP sign",
    ),
    dict(
        quiz_id=9, key="q4", order=4,
        section_heading="Developmental Milestones",
        question_text="On transvaginal ultrasound, the yolk sac is typically first visible at:",
        choice_a="3–4 weeks gestational age",
        choice_b="5–6 weeks gestational age",
        choice_c="7–8 weeks gestational age",
        choice_d="9–10 weeks gestational age",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The yolk sac is typically visible on transvaginal ultrasound at approximately "
            "5–6 weeks gestational age, when the mean gestational sac diameter reaches about "
            "8–10 mm."
        ),
        label="Yolk sac visibility by TVUS",
    ),
    dict(
        quiz_id=9, key="q5", order=5,
        section_heading="",
        question_text="On transvaginal ultrasound, the fetal pole is typically first visible at:",
        choice_a="4–5 weeks gestational age",
        choice_b="5.5–6 weeks gestational age",
        choice_c="7–8 weeks gestational age",
        choice_d="9–10 weeks gestational age",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The fetal pole is typically visible on TVUS by 5.5–6 weeks. Cardiac activity "
            "should be identifiable once a fetal pole is seen. Earlier than this the "
            "embryo may not yet be measurable."
        ),
        label="Fetal pole visibility by TVUS",
    ),
    dict(
        quiz_id=9, key="q6", order=6,
        section_heading="",
        question_text="A minimum fetal heart rate of ___ bpm is associated with a more favorable outcome in early pregnancy:",
        choice_a="80 bpm",
        choice_b="100 bpm",
        choice_c="120 bpm",
        choice_d="140 bpm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "A fetal heart rate below 100 bpm in early pregnancy (bradycardia) is associated "
            "with a significantly higher risk of pregnancy loss. A rate ≥ 100 bpm is considered "
            "a more reassuring finding."
        ),
        label="Minimum FHR for good outcome",
    ),
    dict(
        quiz_id=9, key="q7", order=7,
        section_heading="Beta-hCG & Discriminatory Levels",
        question_text="The discriminatory β-hCG level above which a gestational sac should be visible on transabdominal ultrasound is approximately:",
        choice_a="1,000 IU/L",
        choice_b="2,500 IU/L",
        choice_c="6,500 IU/L",
        choice_d="10,000 IU/L",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The transabdominal discriminatory zone is approximately 6,500 IU/L — above this "
            "level a gestational sac should be visible on transabdominal US if the pregnancy "
            "is intrauterine. For TVUS the threshold is lower, around 1,500–2,000 IU/L."
        ),
        label="Discriminatory β-hCG (transabdominal)",
    ),
    dict(
        quiz_id=9, key="q8", order=8,
        section_heading="Pregnancy Failure Criteria",
        question_text="Pregnancy failure is confirmed when:",
        choice_a="No cardiac activity is detected by 6 weeks",
        choice_b="CRL ≥ 7 mm with no cardiac activity on TVUS",
        choice_c="Gestational sac > 10 mm without a yolk sac",
        choice_d="β-hCG fails to double over 48 hours",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Per ACOG/AIUM criteria, a fetal pole with CRL ≥ 7 mm and no cardiac activity "
            "on TVUS confirms pregnancy failure (embryonic demise). This threshold is used "
            "to avoid false-positive diagnosis of failed pregnancy."
        ),
        label="Pregnancy failure criterion",
    ),
    dict(
        quiz_id=9, key="q9", order=9,
        section_heading="Safety Criterion",
        question_text="The minimum myometrial mantle thickness required to meet the safety criterion of the 3-2-1 rule is:",
        choice_a="2 mm",
        choice_b="5 mm",
        choice_c="8 mm",
        choice_d="10 mm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The safety criterion (the '1' in 3-2-1) requires a myometrial mantle of ≥ 5 mm "
            "between the gestational sac and the uterine serosa. A mantle < 5 mm raises "
            "concern for interstitial or cornual ectopic pregnancy."
        ),
        label="Minimum myometrial mantle",
    ),
    dict(
        quiz_id=9, key="q10", order=10,
        section_heading="Intrauterine Criteria",
        question_text="In the transverse view, the endometrial stripe containing the gestational sac should be:",
        choice_a="Completely absent",
        choice_b="Centrally located within uterine tissue on all sides",
        choice_c="Adjacent to the anterior bladder wall",
        choice_d="Located at the fundus only",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The endometrial stripe — and any gestational sac within it — must be surrounded "
            "by myometrial tissue on all sides in the transverse view. This confirms the sac "
            "is truly within the uterine cavity, not interstitially or cervically located."
        ),
        label="Endometrial stripe in transverse view",
    ),
    dict(
        quiz_id=9, key="q11", order=11,
        section_heading="",
        question_text="Bladder-uterine juxtaposition refers to:",
        choice_a="The bladder filling above the uterine fundus",
        choice_b="The bladder and uterus sharing a contiguous tissue plane in the longitudinal view",
        choice_c="The bladder lying posterior to the uterus",
        choice_d="A cystic structure adjacent to the uterus that could be confused with a gestational sac",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Bladder-uterine juxtaposition is one of the two intrauterine criteria in the "
            "3-2-1 rule. In the longitudinal view, the anterior bladder wall must be shown "
            "to be contiguous (touching) with the anterior uterine wall — confirming the "
            "structure identified is indeed the uterus."
        ),
        label="Bladder-uterine juxtaposition",
    ),
    dict(
        quiz_id=9, key="q12", order=12,
        section_heading="Equipment",
        question_text="For transabdominal OB POCUS, the preferred probe is:",
        choice_a="High-frequency linear (10–15 MHz)",
        choice_b="Phased array cardiac probe",
        choice_c="Curvilinear low-frequency (2–5 MHz)",
        choice_d="Endocavitary transvaginal probe",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The curvilinear low-frequency probe (2–5 MHz) is used for transabdominal OB "
            "POCUS due to its adequate depth penetration and wide field of view. The "
            "endocavitary probe is used for transvaginal scanning."
        ),
        label="OB POCUS probe (transabdominal)",
    ),
]


QUIZ_10_QUESTIONS = [
    dict(
        quiz_id=10, key="q1", order=1,
        section_heading="Probe & Technique",
        question_text="The optimal probe for pneumothorax POCUS is:",
        choice_a="Curvilinear low-frequency (2–5 MHz)",
        choice_b="Phased array cardiac probe",
        choice_c="High-frequency linear (7.5–15 MHz)",
        choice_d="Microconvex probe",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The high-frequency linear probe provides the best resolution of the superficial "
            "pleural line and is the preferred probe for lung sliding assessment. However, "
            "any probe placed over the anterior chest will show absence of lung sliding "
            "in pneumothorax."
        ),
        label="Best probe for pneumothorax",
    ),
    dict(
        quiz_id=10, key="q2", order=2,
        section_heading="",
        question_text="The primary area of interest (AOI) for pneumothorax detection is:",
        choice_a="Lower posterior lung zones",
        choice_b="Upper anterior chest wall (2nd–4th intercostal spaces)",
        choice_c="Posterior chest wall at the scapular line",
        choice_d="Lateral chest wall only",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Air rises to the most non-dependent (anterior) position in a supine patient. "
            "Therefore, the upper anterior chest at the 2nd–4th intercostal spaces in the "
            "midclavicular line is the primary AOI for pneumothorax detection."
        ),
        label="AOI for pneumothorax",
    ),
    dict(
        quiz_id=10, key="q3", order=3,
        section_heading="Lung Sliding",
        question_text="Lung sliding on POCUS is best described as:",
        choice_a="Paradoxical chest wall movement with breathing",
        choice_b="Movement of pleural effusion fluid with respiration",
        choice_c="To-and-fro movement of the visceral and parietal pleura against each other with respiration",
        choice_d="Diaphragmatic excursion visible on M-mode",
        choice_e="",
        correct_answer="C",
        explanation=(
            "Lung sliding is the real-time shimmering movement of the visceral pleura (lung "
            "surface) against the fixed parietal pleura with each breath. It has been "
            "described as looking like 'ants marching on a log' and is absent in pneumothorax."
        ),
        label="Lung sliding definition",
    ),
    dict(
        quiz_id=10, key="q4", order=4,
        section_heading="Artifacts",
        question_text="B-lines (comet-tail artifacts) in lung POCUS originate from:",
        choice_a="Air-fluid interfaces within diseased alveoli",
        choice_b="The pleural line, caused by acoustic reflections from fluid-filled interlobular septa",
        choice_c="Rib shadows casting posterior acoustic shadows",
        choice_d="Subcutaneous emphysema near the skin surface",
        choice_e="",
        correct_answer="B",
        explanation=(
            "B-lines arise from the pleural line when acoustic waves reverberate between "
            "fluid-thickened interlobular septa (subpleural) and the probe. They are absent "
            "in normal aerated lung and in pneumothorax — air prevents their generation."
        ),
        label="Comet tail origin",
    ),
    dict(
        quiz_id=10, key="q5", order=5,
        section_heading="Lung Point",
        question_text="The lung point is 100% specific for pneumothorax because:",
        choice_a="It is only seen with large pneumothoraces",
        choice_b="It represents the exact transition between present lung sliding and absent sliding — a finding only possible with true pneumothorax",
        choice_c="It appears as a hyperechoic line on M-mode",
        choice_d="It is absent in all other lung pathologies",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lung point is the dynamic point where the partially collapsed lung re-touches "
            "the chest wall at the edge of the pneumothorax. This alternating sliding/no-sliding "
            "transition is pathognomonic for pneumothorax and has ~100% specificity."
        ),
        label="True lung point specificity",
    ),
    dict(
        quiz_id=10, key="q6", order=6,
        section_heading="Protocol",
        question_text="For a complete pneumothorax POCUS evaluation, how many pleural zones should be assessed?",
        choice_a="1 (most anterior left)",
        choice_b="2 (bilateral anterior)",
        choice_c="4 (bilateral anterior and lateral)",
        choice_d="6 (bilateral anterior, lateral, and posterior)",
        choice_e="",
        correct_answer="C",
        explanation=(
            "A complete scan assesses 4 zones bilaterally: anterior upper (2nd ICS MCL), "
            "anterior lower (4th ICS MCL), and lateral zones on each side. Bilateral "
            "evaluation is essential as pneumothorax may be unilateral."
        ),
        label="Number of pleural spaces to evaluate",
    ),
    dict(
        quiz_id=10, key="q7", order=7,
        section_heading="Interpretation",
        question_text="A determinate negative (truly negative) pneumothorax scan requires:",
        choice_a="Absence of B-lines in all zones",
        choice_b="Lung sliding present in bilateral anterior zones",
        choice_c="A normal seashore sign on M-mode from one side",
        choice_d="Cardiac activity visible subxiphoid",
        choice_e="",
        correct_answer="B",
        explanation=(
            "A negative scan requires demonstration of lung sliding bilaterally in the "
            "anterior zones. Lung sliding confirms the visceral and parietal pleura are in "
            "contact, ruling out pneumothorax at that location. One-sided assessment is "
            "insufficient."
        ),
        label="Determinate negative scan",
    ),
    dict(
        quiz_id=10, key="q8", order=8,
        section_heading="",
        question_text="When searching for the lung point, you should start:",
        choice_a="At the most medial (parasternal) zone",
        choice_b="At the lung apex",
        choice_c="At the most lateral extent of absent lung sliding and scan medially",
        choice_d="At the lateral chest wall and scan posteriorly",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lung point is found at the boundary of the pneumothorax. Start where lung "
            "sliding is absent and move the probe laterally or inferiorly until the alternating "
            "sliding/no-sliding transition (lung point) is identified."
        ),
        label="Starting point for lung point search",
    ),
    dict(
        quiz_id=10, key="q9", order=9,
        section_heading="",
        question_text="In a large pneumothorax, the lung point is typically located:",
        choice_a="At the anterior chest wall",
        choice_b="At the 2nd intercostal space",
        choice_c="At the midclavicular line",
        choice_d="Laterally or posteriorly — or may not be found at all",
        choice_e="",
        correct_answer="D",
        explanation=(
            "As the pneumothorax enlarges, the collapsed lung retracts further medially. "
            "The lung point moves laterally or posteriorly. In a very large or tension "
            "pneumothorax, the lung point may not be visible at all within the scan range."
        ),
        label="Large pneumothorax lung point location",
    ),
    dict(
        quiz_id=10, key="q10", order=10,
        section_heading="Pitfalls",
        question_text="Which of the following can cause a FALSE POSITIVE pneumothorax (absent lung sliding without true PTX)?",
        choice_a="Pulmonary edema",
        choice_b="Right mainstem intubation causing absent left lung ventilation",
        choice_c="Rib fracture artifact",
        choice_d="Pleural effusion",
        choice_e="",
        correct_answer="B",
        explanation=(
            "Right mainstem intubation causes the left lung to stop ventilating. Because "
            "lung sliding depends on ventilation moving the visceral pleura, absent ventilation "
            "eliminates lung sliding — producing a false-positive pneumothorax appearance on "
            "the left side."
        ),
        label="False positive cause",
    ),
    dict(
        quiz_id=10, key="q11", order=11,
        section_heading="",
        question_text="The lung pulse in pneumothorax POCUS refers to:",
        choice_a="Cardiac impulse transmitted through fully aerated normal lung",
        choice_b="Subtle cardiac-synchronous motion of the pleural line when the lung is collapsed and not ventilated",
        choice_c="Respiratory variation of the pleural line in normal patients",
        choice_d="M-mode finding showing alternating seashore and barcode patterns",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lung pulse is a subtle cardiac-transmitted pulsation visible at the pleural "
            "line in a non-ventilated but non-pneumothorax lung. It indicates the lung is "
            "atelectatic but still in contact with the chest wall — differentiating atelectasis "
            "from pneumothorax."
        ),
        label="Lung pulse definition",
    ),
    dict(
        quiz_id=10, key="q12", order=12,
        section_heading="Clinical Integration",
        question_text="In an unstable patient with suspected tension pneumothorax and absent lung sliding, POCUS should:",
        choice_a="Replace clinical decision-making and be repeated until lung point is confirmed",
        choice_b="Support but not delay needle decompression when clinical signs indicate tension PTX",
        choice_c="Only be performed if chest X-ray is unavailable",
        choice_d="Only be interpreted by a radiologist in the resuscitation bay",
        choice_e="",
        correct_answer="B",
        explanation=(
            "POCUS is a valuable adjunct in suspected tension pneumothorax but must not delay "
            "treatment. In a hemodynamically unstable patient with clinical signs of tension "
            "PTX (absent breath sounds, tracheal deviation, hypotension), needle decompression "
            "should not be withheld pending POCUS confirmation."
        ),
        label="Unstable patient management",
    ),
]


def seed_quizzes_7_10(apps, schema_editor):
    QuizQuestion = apps.get_model("logbook", "QuizQuestion")

    all_questions = (
        QUIZ_7_QUESTIONS
        + QUIZ_8_QUESTIONS
        + QUIZ_9_QUESTIONS
        + QUIZ_10_QUESTIONS
    )

    for q in all_questions:
        QuizQuestion.objects.get_or_create(
            quiz_id=q["quiz_id"],
            key=q["key"],
            defaults={
                "order": q["order"],
                "section_heading": q.get("section_heading", ""),
                "question_text": q["question_text"],
                "choice_a": q.get("choice_a", ""),
                "choice_b": q.get("choice_b", ""),
                "choice_c": q.get("choice_c", ""),
                "choice_d": q.get("choice_d", ""),
                "choice_e": q.get("choice_e", ""),
                "correct_answer": q["correct_answer"],
                "explanation": q.get("explanation", ""),
                "label": q.get("label", ""),
            },
        )


def unseed_quizzes_7_10(apps, schema_editor):
    QuizQuestion = apps.get_model("logbook", "QuizQuestion")
    QuizQuestion.objects.filter(quiz_id__in=[7, 8, 9, 10]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0017_seed_first_trimester_quiz"),
    ]

    operations = [
        migrations.RunPython(seed_quizzes_7_10, unseed_quizzes_7_10),
    ]
