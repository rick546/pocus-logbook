"""
Re-seed migration: Replace quiz 7–10 MC questions with content derived
strictly from the AAA.pdf, FAST.pdf, OBs.pdf, and Pneumothorax.pdf
curriculum documents.
"""

from django.db import migrations


QUIZ_7_QUESTIONS = [
    # ── Knobology / Preparation ─────────────────────────────────────────────
    dict(
        quiz_id=7, key="q1", order=1,
        section_heading="Knobology & Preparation",
        question_text="Which probe is specified for AAA scanning?",
        choice_a="Phased array",
        choice_b="Linear",
        choice_c="Curved array",
        choice_d="Endocavitary",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The AAA document specifies a curved array (curvilinear) probe with the system "
            "preset set to aorta/abdominal."
        ),
        label="AAA probe",
    ),
    dict(
        quiz_id=7, key="q2", order=2,
        section_heading="",
        question_text="What depth setting is specified for AAA scanning?",
        choice_a="10 cm",
        choice_b="15 cm",
        choice_c="20 cm",
        choice_d="30 cm",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The document specifies a depth of 30 cm for penetration when scanning for AAA."
        ),
        label="AAA depth",
    ),
    # ── Landmarks ────────────────────────────────────────────────────────────
    dict(
        quiz_id=7, key="q3", order=3,
        section_heading="Landmarks",
        question_text="What is the external landmark for AAA scanning?",
        choice_a="Umbilicus",
        choice_b="Costal margin",
        choice_c="Xiphoid process",
        choice_d="Symphysis pubis",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states the external landmark is the xiphoid process. The probe is "
            "placed just caudal to the xiphoid process in the transverse plane as the first step."
        ),
        label="AAA external landmark",
    ),
    dict(
        quiz_id=7, key="q4", order=4,
        section_heading="",
        question_text="What is the internal landmark used to locate the aorta during AAA scanning?",
        choice_a="IVC",
        choice_b="Spine",
        choice_c="Left kidney",
        choice_d="Celiac axis",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document identifies the spine as the internal landmark — it appears as a "
            "hyperechoic structure with acoustic shadowing past it, and the aorta lies "
            "immediately anterior to it."
        ),
        label="AAA internal landmark",
    ),
    # ── Aorta vs IVC ─────────────────────────────────────────────────────────
    dict(
        quiz_id=7, key="q5", order=5,
        section_heading="Aorta vs IVC",
        question_text=(
            "According to the document, the aorta is typically located on which side "
            "relative to the IVC?"
        ),
        choice_a="Patient's right, same side as the IVC",
        choice_b="Patient's left, in comparison to the IVC",
        choice_c="Directly posterior to the IVC",
        choice_d="Anterior to the IVC",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states the aorta is located immediately anterior to the spine, "
            "usually on the patient's left in comparison to the IVC."
        ),
        label="Aorta position vs IVC",
    ),
    dict(
        quiz_id=7, key="q6", order=6,
        section_heading="",
        question_text=(
            "According to the document, what happens to the aorta when firm probe "
            "pressure is applied to the abdomen?"
        ),
        choice_a="It collapses, like the IVC",
        choice_b="It shows respiratory variability",
        choice_c="It does NOT collapse — it is non-compressible",
        choice_d="It becomes more echogenic",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'if you push into the belly with the probe, the aorta "
            "should NOT collapse, whereas the IVC will.' Non-compressibility is a key feature "
            "distinguishing the aorta from the IVC."
        ),
        label="Aorta non-compressibility",
    ),
    # ── Measurement ──────────────────────────────────────────────────────────
    dict(
        quiz_id=7, key="q7", order=7,
        section_heading="Measurement",
        question_text="Normal aortic calibre is defined as:",
        choice_a="Inner wall to inner wall, less than 4 cm",
        choice_b="Outer wall to outer wall, 3 cm or less",
        choice_c="Inner lumen diameter, less than 3.5 cm",
        choice_d="Outer wall to inner wall, less than 2 cm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Normal aortic calibre is 3cm from outer wall to outer wall.'"
        ),
        label="Normal aortic calibre",
    ),
    dict(
        quiz_id=7, key="q8", order=8,
        section_heading="",
        question_text=(
            "The document states it is critical to keep the probe at a 90-degree angle to "
            "the skin. What is the consequence of NOT doing this?"
        ),
        choice_a="The spine will not be visible",
        choice_b="The gain will become too high",
        choice_c="You can falsely increase or decrease the lumen size and over- or under-call AAA",
        choice_d="Doppler signal will be lost",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'It is critical to keep the probe at a 90-degree angle "
            "to the skin, otherwise you can falsely increase/decrease the lumen size and "
            "over/under call AAA.'"
        ),
        label="Probe angle pitfall",
    ),
    # ── Pitfalls ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=7, key="q9", order=9,
        section_heading="Pitfalls",
        question_text=(
            "When chronic thrombus is present in an AAA, the document states measurement "
            "must include:"
        ),
        choice_a="Only the patent lumen, excluding the thrombus",
        choice_b="The distance from inner wall to outer wall only",
        choice_c="Outer wall to outer wall, including the more echogenic thrombus",
        choice_d="The thrombus alone, excluding the patent lumen",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document identifies this as an image interpretation pitfall: 'measuring the "
            "diameter of the false lumen, instead of the true lumen which is outer wall to "
            "outer wall — you have to measure all of it, including the more echogenic thrombus.'"
        ),
        label="Chronic thrombus measurement",
    ),
    dict(
        quiz_id=7, key="q10", order=10,
        section_heading="",
        question_text="The document defines an indeterminate AAA scan as:",
        choice_a="An aorta measuring between 2–3 cm",
        choice_b="A scan where the IVC and aorta cannot be distinguished",
        choice_c=(
            "When you cannot visualize the entire abdominal aorta from the xiphoid process "
            "down to the bifurcation"
        ),
        choice_d="Any scan with visible bowel gas on screen",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Indeterminate scans: When you cannot visualize the entire "
            "abdominal aorta from the xiphoid process down to the bifurcation — gas, obesity "
            "can very often get in the way and cause significant scatter.'"
        ),
        label="Indeterminate scan definition",
    ),
    dict(
        quiz_id=7, key="q11", order=11,
        section_heading="",
        question_text=(
            "Which of the following is listed under clinical integration pitfalls in the "
            "AAA document?"
        ),
        choice_a="Using a linear probe instead of a curved array",
        choice_b="Assuming a AAA less than 5 cm cannot rupture",
        choice_c="Not using Doppler to confirm aortic pulsatility",
        choice_d="Scanning in longitudinal rather than transverse plane",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document lists under clinical integration pitfalls: 'Assuming a AAA < 5cm "
            "cannot rupture.'"
        ),
        label="Clinical integration pitfall",
    ),
    # ── Determinant Positive ──────────────────────────────────────────────────
    dict(
        quiz_id=7, key="q12", order=12,
        section_heading="Determinant Positive Scan",
        question_text=(
            "The document states that most AAAs are which morphological shape, and this "
            "guides which diameter to measure?"
        ),
        choice_a="Saccular",
        choice_b="Pseudoaneurysm",
        choice_c="Fusiform",
        choice_d="Dissecting",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Most AAAs are fusiform in shape — pick the diameter "
            "that looks biggest in size — measure from outer wall to outer wall.' The document "
            "also notes that saccular aneurysms can be easily overlooked, so a methodical "
            "scan is important."
        ),
        label="Determinant positive — AAA shape",
    ),
]


QUIZ_8_QUESTIONS = [
    # ── Knobology ────────────────────────────────────────────────────────────
    dict(
        quiz_id=8, key="q1", order=1,
        section_heading="Knobology & Preparation",
        question_text="Which probe is specified for the abdominal FAST exam?",
        choice_a="Linear",
        choice_b="Phased array",
        choice_c="Curvilinear",
        choice_d="Endocavitary",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The FAST document specifies a curvilinear probe with the systems preset set to "
            "abdominal."
        ),
        label="FAST probe",
    ),
    dict(
        quiz_id=8, key="q2", order=2,
        section_heading="",
        question_text="What is the recommended depth setting for the abdominal FAST exam?",
        choice_a="10 cm",
        choice_b="15 cm",
        choice_c="20 cm or machine max",
        choice_d="30 cm",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document specifies depth of 20 cm or machine max for the abdominal FAST exam."
        ),
        label="FAST depth",
    ),
    # ── Upper Quadrants ───────────────────────────────────────────────────────
    dict(
        quiz_id=8, key="q3", order=3,
        section_heading="Upper Quadrant Views",
        question_text="What is the internal landmark for the upper quadrant FAST views?",
        choice_a="Liver",
        choice_b="Kidney",
        choice_c="Diaphragm",
        choice_d="Spine",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document identifies the kidney as the internal landmark for upper quadrant "
            "FAST views. The probe is slid posteriorly/anteriorly to locate the kidney and "
            "ensure the best view of the solid organ/renal interface."
        ),
        label="Upper quadrant internal landmark",
    ),
    dict(
        quiz_id=8, key="q4", order=4,
        section_heading="",
        question_text=(
            "In the upper quadrant views, the probe is placed at the mid to posterior "
            "axillary line at the level of the xiphoid process in which plane, with the "
            "indicator pointing cephalad?"
        ),
        choice_a="Transverse",
        choice_b="Oblique",
        choice_c="Longitudinal",
        choice_d="Coronal oblique",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document specifies: 'Place probe at mid to post axillary line at the level "
            "of the xiphoid process in the longitudinal plane, indicator pointing cephalad.'"
        ),
        label="Upper quadrant probe plane",
    ),
    dict(
        quiz_id=8, key="q5", order=5,
        section_heading="",
        question_text=(
            "The document identifies which location as the most sensitive place to find "
            "free fluid on the FAST exam?"
        ),
        choice_a="Subdiaphragmatic space in the LUQ",
        choice_b="Splenorenal interface",
        choice_c="Caudal tip of the liver",
        choice_d="Pelvic rectovesical pouch",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Identify the caudal tip of the liver and interrogate for "
            "free fluid ✱✱This is the most sensitive place to identify free fluid on the "
            "FAST exam.'"
        ),
        label="Most sensitive free fluid site",
    ),
    dict(
        quiz_id=8, key="q6", order=6,
        section_heading="",
        question_text=(
            "In the LUQ, the document identifies which space as the most likely place to "
            "find free fluid?"
        ),
        choice_a="Splenorenal interface",
        choice_b="Subdiaphragmatic space",
        choice_c="Perisplenic space",
        choice_d="Between the stomach and spleen",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'The subdiaphragmatic space is the most likely place to "
            "find free fluid in the LUQ.' The probe is slid cephalad to visualize the "
            "subdiaphragmatic space from 6 to 9 o'clock."
        ),
        label="Most likely LUQ free fluid site",
    ),
    # ── Pitfalls ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=8, key="q7", order=7,
        section_heading="Pitfalls",
        question_text=(
            "According to the document, a negative FAST exam can only rule out hemoperitoneum "
            "greater than what volume, at one specific moment in time?"
        ),
        choice_a="100 ml",
        choice_b="150 ml",
        choice_c="200 ml",
        choice_d="250 ml",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The document states under clinical integration pitfalls: 'Only can rule out "
            "significant hemoperitoneum (>250ml of fluid) in one specific moment in time.'"
        ),
        label="Minimum hemoperitoneum ruled out",
    ),
    dict(
        quiz_id=8, key="q8", order=8,
        section_heading="",
        question_text=(
            "The document identifies which pelvic structure in males as having a bow-tie "
            "appearance that can be misidentified as free fluid?"
        ),
        choice_a="Prostate",
        choice_b="Rectum",
        choice_c="Seminal vesicles",
        choice_d="Iliac vessels",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document lists under pelvic pitfalls: 'Misidentifying the seminal vesicles "
            "as free fluid (will look like a bow-tie).'"
        ),
        label="Male pelvic false positive structure",
    ),
    # ── Pelvic ───────────────────────────────────────────────────────────────
    dict(
        quiz_id=8, key="q9", order=9,
        section_heading="Pelvic View",
        question_text="What is the area of interest (AOI) for the pelvic FAST view in male patients?",
        choice_a="Vesicouterine pouch",
        choice_b="Rectovesical pouch",
        choice_c="Subdiaphragmatic space",
        choice_d="Hepatorenal interface",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states the pelvic AOI is the 'rectovesical pouch in men and "
            "rectouterine pouch and vesicouterine pouch in women.'"
        ),
        label="Pelvic AOI in males",
    ),
    # ── Tips & Tricks ─────────────────────────────────────────────────────────
    dict(
        quiz_id=8, key="q10", order=10,
        section_heading="Tips & Tricks",
        question_text=(
            "According to the Tips and Tricks section of the FAST document, placing the "
            "patient in Trendelenberg delivers fluid to which area?"
        ),
        choice_a="Pelvis",
        choice_b="RUQ",
        choice_c="LUQ",
        choice_d="Subdiaphragmatic space",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states under Tips and Tricks: 'Place patient in Trendelenberg — "
            "delivers fluid to the RUQ.' (Note: the pelvic section specifies reverse "
            "Trendelenburg for pelvic free fluid visibility.)"
        ),
        label="Trendelenberg tip",
    ),
    dict(
        quiz_id=8, key="q11", order=11,
        section_heading="",
        question_text=(
            "Which of the following is listed as a clinical integration pitfall in the "
            "FAST document?"
        ),
        choice_a="Starting the scan in the transverse rather than longitudinal plane",
        choice_b=(
            "Assuming that absence of free fluid rules out solid organ, hollow viscus, "
            "or vascular injury"
        ),
        choice_c="Using too much gain in the upper quadrant views",
        choice_d="Not starting at the level of the xiphoid process",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Assuming the absence of free fluid in an acute trauma "
            "patient rules out solid organ, hollow viscus or vascular injury.' This is listed "
            "explicitly as a clinical integration pitfall."
        ),
        label="Clinical integration pitfall",
    ),
]


QUIZ_9_QUESTIONS = [
    # ── Goals of Exam ─────────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q1", order=1,
        section_heading="Goals of Exam",
        question_text=(
            "According to the document, what is the primary stated goal of OB POCUS in "
            "the first trimester?"
        ),
        choice_a="Rule out an ectopic pregnancy",
        choice_b="Rule in an intrauterine pregnancy",
        choice_c="Measure the crown-rump length",
        choice_d="Assess fetal heart rate variability",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Rule in an intrauterine pregnancy, remember you cannot "
            "absolutely rule out an ectopic pregnancy.' The goal is to rule IN an IUP, not "
            "to rule out ectopic."
        ),
        label="Primary goal of OB POCUS",
    ),
    # ── 3-2-1 Rule ───────────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q2", order=2,
        section_heading="3-2-1 Rule — Pregnancy Criteria",
        question_text="According to the 3-2-1 rule in the document, how many pregnancy criteria are required?",
        choice_a="1",
        choice_b="2",
        choice_c="3",
        choice_d="4",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Pregnancy Criteria (3) — need all to confirm a pregnancy: "
            "1. Decidual reaction, 2. Gestational sac, 3. Yolk sac OR fetal pole with "
            "visible fetal heart.'"
        ),
        label="Number of pregnancy criteria",
    ),
    dict(
        quiz_id=9, key="q3", order=3,
        section_heading="",
        question_text="The document describes the 'double ring sign' as:",
        choice_a="Two adjacent gestational sacs",
        choice_b=(
            "The yolk sac within the gestational sac — the earliest sign of a definitive IUP"
        ),
        choice_c="The fetal pole and yolk sac seen together",
        choice_d="The bladder and uterus appearing side by side",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'The \"double ring sign\" — the yolk sac within gestational "
            "sac, is the earliest sign of a definitive IUP.'"
        ),
        label="Double ring sign",
    ),
    dict(
        quiz_id=9, key="q4", order=4,
        section_heading="",
        question_text="According to the document, the yolk sac can be seen by transvaginal ultrasound (TVUS) starting at:",
        choice_a="4 weeks",
        choice_b="5 weeks",
        choice_c="5.5 weeks",
        choice_d="6.5 weeks",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states the yolk sac 'Can be seen by 5.5 weeks by TVUS' and by "
            "6.5 weeks by ABUS."
        ),
        label="Yolk sac — TVUS timing",
    ),
    dict(
        quiz_id=9, key="q5", order=5,
        section_heading="",
        question_text=(
            "For a living intrauterine pregnancy, the document states a fetal heart rate of "
            "greater than ___ bpm is required to be consistent with a good fetal outcome."
        ),
        choice_a="80 bpm",
        choice_b="90 bpm",
        choice_c="100 bpm",
        choice_d="120 bpm",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Must have a heart rate of > 100 to be consistent with "
            "a good fetal outcome.'"
        ),
        label="Minimum FHR for good outcome",
    ),
    # ── Safety Criterion ──────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q6", order=6,
        section_heading="3-2-1 Rule — Safety Criterion",
        question_text=(
            "The safety criterion of the 3-2-1 rule requires the shortest distance between "
            "the inner edge of the gestational sac and the outer edge of the uterus to be "
            "at least:"
        ),
        choice_a="3 mm",
        choice_b="5 mm",
        choice_c="8 mm",
        choice_d="10 mm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Adequate myometrial mantle. The shortest distance between "
            "the inner edge of the gestational sac and the outer edge of the uterus must be "
            "at least 5mm.'"
        ),
        label="Minimum myometrial mantle",
    ),
    # ── Pregnancy Failure ─────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q7", order=7,
        section_heading="Pregnancy Failure",
        question_text=(
            "Which of the following is listed as a criterion for pregnancy failure in the "
            "document?"
        ),
        choice_a="No gestational sac at BhCG greater than 1000 transabdominally",
        choice_b="No yolk sac with gestational sac greater than 10 mm",
        choice_c="CRL greater than 5–7 mm with no fetal heart rate",
        choice_d="No fetal heart rate after 8 weeks gestational age",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document lists pregnancy failure criterion #4 as: 'CRL > 5-7mm with no FHR.' "
            "Other listed criteria include no GS at BhCG >3000 transabdominally (not >1000), "
            "no yolk sac with GS >15mm (not >10mm), and no FHR after 10-12 weeks (not 8 weeks)."
        ),
        label="Pregnancy failure — CRL criterion",
    ),
    # ── Intrauterine Criteria ─────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q8", order=8,
        section_heading="3-2-1 Rule — Intrauterine Criteria",
        question_text="What does the bladder-uterine juxtaposition criterion require?",
        choice_a="The bladder must be completely empty",
        choice_b=(
            "At least one image must clearly show the bladder and uterine tissue in direct "
            "contact"
        ),
        choice_c="The bladder must be posterior to the uterus",
        choice_d="The bladder must overlay the fundus of the uterus",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Bladder-uterine juxtaposition. At least one image must "
            "clearly show the bladder and uterine tissue in direct contact.'"
        ),
        label="Bladder-uterine juxtaposition",
    ),
    # ── Knobology ────────────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q9", order=9,
        section_heading="Knobology & Preparation",
        question_text="According to the document, why is a full bladder required for transabdominal OB POCUS?",
        choice_a="To push the uterus into a more superior position",
        choice_b="To allow for a good acoustic window to look through to see the uterus",
        choice_c="To measure free fluid in the pelvis accurately",
        choice_d="To identify the endometrial stripe",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Requires a full bladder (allows for a good acoustic "
            "window to look through to see the uterus).'"
        ),
        label="Full bladder reason",
    ),
    dict(
        quiz_id=9, key="q10", order=10,
        section_heading="",
        question_text="Which probe is specified for OB POCUS in the document?",
        choice_a="Phased array",
        choice_b="Linear",
        choice_c="Curvilinear",
        choice_d="Endocavitary (transvaginal)",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document specifies a curvilinear probe with system preset OB and depth 15cm "
            "for transabdominal OB POCUS."
        ),
        label="OB probe",
    ),
    # ── Intrauterine Criteria ─────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q11", order=11,
        section_heading="Vaginal Uterine Continuity",
        question_text="What does vaginal uterine continuity require in the longitudinal view?",
        choice_a="The vagina must be fully imaged from introitus to cervix",
        choice_b=(
            "The vagina must be shown to transverse directly into uterine tissue"
        ),
        choice_c="The uterus must appear circular in this orientation",
        choice_d="Color Doppler must confirm flow in both vagina and uterus",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Vaginal uterine continuity. In longitudinal view, the "
            "vagina must be shown to transverse directly into uterine tissue.'"
        ),
        label="Vaginal uterine continuity",
    ),
    # ── Pitfalls ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=9, key="q12", order=12,
        section_heading="Pitfalls",
        question_text=(
            "Which of the following is listed as a clinical integration pitfall in the "
            "OBs document?"
        ),
        choice_a="Using too much gain during scanning",
        choice_b="Starting the scan in the transverse rather than longitudinal plane",
        choice_c="Assuming IUP despite the 3-2-1 rule not being fulfilled",
        choice_d="Not using the endocavitary probe for transabdominal scanning",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states under Pitfalls Clinical Integration: 'Assuming IUP, "
            "despite 3-2-1 rule not being fulfilled.'"
        ),
        label="Clinical integration pitfall",
    ),
]


QUIZ_10_QUESTIONS = [
    # ── Knobology ────────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q1", order=1,
        section_heading="Knobology & Preparation",
        question_text=(
            "According to the document, which probe provides the best image quality for "
            "pneumothorax assessment?"
        ),
        choice_a="Curvilinear",
        choice_b="Phased array",
        choice_c="Linear",
        choice_d="Endocavitary",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Probe: curvilinear, linear (best image quality).' "
            "The linear probe provides the best image quality for the pleural line."
        ),
        label="Best image quality probe",
    ),
    dict(
        quiz_id=10, key="q2", order=2,
        section_heading="",
        question_text="What is the starting depth specified for pneumothorax scanning?",
        choice_a="5 cm",
        choice_b="10 cm, then center the pleural line",
        choice_c="15 cm",
        choice_d="20 cm",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document specifies: 'Depth: 10cm and then center pleural line.'"
        ),
        label="PTX starting depth",
    ),
    # ── Landmarks ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q3", order=3,
        section_heading="Landmarks",
        question_text="What is the external landmark for pneumothorax scanning?",
        choice_a="The sternum",
        choice_b="The posterior axillary line",
        choice_c=(
            "The most anterior part of the lung in the mid-clavicular line of a supine patient"
        ),
        choice_d="The xiphoid process",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'External: most anterior part of lung in mid-clavicular "
            "line of a supine patient.' Air rises to the most anterior, non-dependent position "
            "in a supine patient."
        ),
        label="External landmark",
    ),
    # ── What to Assess ────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q4", order=4,
        section_heading="What to Assess",
        question_text="How does the document describe lung sliding?",
        choice_a="B-lines moving in and out with respiration",
        choice_b=(
            "Visceral and parietal pleura moving against each other with respiration — "
            "looks like ants sliding on a log"
        ),
        choice_c="Cardiac pulsation transmitted to the pleural line",
        choice_d="A reverberation of the ultrasound beam off the chest wall",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Lung Sliding: visceral and parietal pleura moving against "
            "each other with respiration. Looks like ants sliding on a log.'"
        ),
        label="Lung sliding definition",
    ),
    dict(
        quiz_id=10, key="q5", order=5,
        section_heading="",
        question_text="The document defines the lung pulse as:",
        choice_a="The normal cardiac-synchronous pulsation seen in a well-aerated lung",
        choice_b=(
            "Cardiac pulsation transmitted to the pleural line in a poorly aerated lung "
            "(e.g., atelectasis or mainstem intubation)"
        ),
        choice_c="The respiratory movement of the pleural line in a normal patient",
        choice_d="A reverberation artifact at the pleural line",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'Lung Pulse: cardiac pulsation transmitted to the pleural "
            "line in a poorly aerated lung (i.e. atelectasis or main stem intubation).'"
        ),
        label="Lung pulse definition",
    ),
    dict(
        quiz_id=10, key="q6", order=6,
        section_heading="",
        question_text="The document defines the True Lung Point (pathological) as:",
        choice_a="Sliding next to something else that is also sliding",
        choice_b="Sliding next to no sliding — 100% specific for pneumothorax",
        choice_c="Absence of all pleural signs in 3 or more rib spaces",
        choice_d="The point from which comet tails arise on the pleural line",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'True Lung Point (pathological) — sliding next to no "
            "sliding (100% specific).' This distinguishes it from the physiologic lung point "
            "which is sliding next to something else that is also sliding."
        ),
        label="True lung point",
    ),
    # ── Steps ─────────────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q7", order=7,
        section_heading="Steps",
        question_text=(
            "According to the document's steps, the pleural line is evaluated for "
            "pneumothorax in how many pleural spaces?"
        ),
        choice_a="1",
        choice_b="2",
        choice_c="3",
        choice_d="4",
        choice_e="",
        correct_answer="C",
        explanation=(
            "Step 4 of the document states: 'Evaluate the pleural line for pneumothorax, "
            "do this in 3 pleural spaces.'"
        ),
        label="Number of pleural spaces",
    ),
    # ── Determinate Scans ─────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q8", order=8,
        section_heading="Determinate Scans",
        question_text="The document defines a determinate negative pneumothorax scan as:",
        choice_a="Absence of comet tails in all rib spaces",
        choice_b="Lung sliding AND lung pulse AND comet tails all present simultaneously",
        choice_c=(
            "Lung sliding OR lung pulse OR comet tails/B-lines present in the most "
            "anterior rib space"
        ),
        choice_d="No lung point identified anywhere on the chest wall",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Determinate Negative Scan: Lung sliding OR Lung pulse "
            "OR Comet Tails / B-lines present in most anterior rib space.' Only one of "
            "these three signs needs to be present."
        ),
        label="Determinate negative scan",
    ),
    dict(
        quiz_id=10, key="q9", order=9,
        section_heading="",
        question_text=(
            "When lung sliding, comet tails, and lung pulse are absent in at least one rib "
            "space over 3 respiratory cycles AND the patient is stable, what does the "
            "document say should be done before declaring a pneumothorax?"
        ),
        choice_a="Obtain a chest X-ray for confirmation",
        choice_b="Repeat the scan in 30 minutes",
        choice_c="Identify the lung point",
        choice_d="Declare the scan indeterminate",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'If lung sliding, comet tails and lung pulse are not "
            "visible in one or more intercostal spaces for at least 3 respiratory cycles "
            "AND the patient is stable, a lung point should be identified to declare a "
            "pneumothorax.'"
        ),
        label="Stable patient — lung point protocol",
    ),
    # ── Size of PTX ───────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q10", order=10,
        section_heading="Pneumothorax Size",
        question_text=(
            "According to the document, where is the lung point located in a LARGE "
            "pneumothorax in a supine patient?"
        ),
        choice_a="Anteriorly — between mid-clavicular and anterior axillary lines",
        choice_b="Laterally — at the mid axillary line",
        choice_c="Posteriorly — at the posterior axillary line",
        choice_d="At the xiphoid process",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states: 'Large = lung point located posteriorly (i.e. posterior "
            "axillary line).' Small = anteriorly, Medium = laterally (mid axillary line)."
        ),
        label="Large PTX — lung point location",
    ),
    # ── Pitfalls ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=10, key="q11", order=11,
        section_heading="Pitfalls — False Positives",
        question_text=(
            "The document lists right mainstem intubation as a false positive cause. What "
            "does the document recommend looking for in this situation?"
        ),
        choice_a="Lung point in the right lung",
        choice_b="Comet tails or lung pulse in the left lung",
        choice_c="B-lines in the right lung",
        choice_d="Lung sliding in the right lung only",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The document states: 'R. mainstem intubation → look for comet tails/lung pulse "
            "in L. lung.' This helps distinguish right mainstem intubation from true left "
            "pneumothorax."
        ),
        label="False positive — right mainstem",
    ),
    dict(
        quiz_id=10, key="q12", order=12,
        section_heading="Pitfalls — Clinical Integration",
        question_text=(
            "According to the clinical integration pitfalls in the document, what concern "
            "is raised about treating a very small pneumothorax?"
        ),
        choice_a="It will always worsen without intervention",
        choice_b="It may cause a tension pneumothorax if a chest tube is placed",
        choice_c="Some small pneumothoraces do not need a chest tube",
        choice_d="Specialist consultation is always required first",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The document states under clinical integration pitfalls: 'Treating a very small "
            "pneumothorax (remember, some don't need a chest tube!)'."
        ),
        label="Small PTX clinical pitfall",
    ),
]


def reseed_quizzes_7_10(apps, schema_editor):
    QuizQuestion = apps.get_model("logbook", "QuizQuestion")
    # Remove all previous questions for quizzes 7–10
    QuizQuestion.objects.filter(quiz_id__in=[7, 8, 9, 10]).delete()

    all_questions = (
        QUIZ_7_QUESTIONS
        + QUIZ_8_QUESTIONS
        + QUIZ_9_QUESTIONS
        + QUIZ_10_QUESTIONS
    )

    for q in all_questions:
        QuizQuestion.objects.create(
            quiz_id=q["quiz_id"],
            key=q["key"],
            order=q["order"],
            section_heading=q.get("section_heading", ""),
            question_text=q["question_text"],
            choice_a=q.get("choice_a", ""),
            choice_b=q.get("choice_b", ""),
            choice_c=q.get("choice_c", ""),
            choice_d=q.get("choice_d", ""),
            choice_e=q.get("choice_e", ""),
            correct_answer=q["correct_answer"],
            explanation=q.get("explanation", ""),
            label=q.get("label", ""),
        )


def reverse_reseed(apps, schema_editor):
    QuizQuestion = apps.get_model("logbook", "QuizQuestion")
    QuizQuestion.objects.filter(quiz_id__in=[7, 8, 9, 10]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0018_seed_aaa_fast_obs_pnx_quizzes"),
    ]

    operations = [
        migrations.RunPython(reseed_quizzes_7_10, reverse_reseed),
    ]
