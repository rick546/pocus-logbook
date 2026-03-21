"""
Replace quiz 1-3 MC questions with content from Dr. Josh Zimmerman's
University of Utah focused cardiac ultrasound lecture series:
  Quiz 1 — FOCUS Introduction
  Quiz 2 — Parasternal Long Axis (PLAX)
  Quiz 3 — Parasternal Short Axis (PSAX)
"""
from django.db import migrations


QUIZ_1_QUESTIONS = [
    # ── Overview ─────────────────────────────────────────────────────────────
    dict(
        quiz_id=1, key="q1", order=1,
        section_heading="Windows & Goals",
        question_text="In focused cardiac ultrasound, a 'window' refers to:",
        choice_a="An opening in the pericardium",
        choice_b="A specific depth setting on the machine",
        choice_c="The location where the probe is placed — what the ultrasound beam looks through to see the heart",
        choice_d="The display mode on the ultrasound machine",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture defines a window as 'where the ultrasound probe is, like a window "
            "in your house — it's what the ultrasound beam looks through to see the structures.'"
        ),
        label="Definition of a window",
    ),
    dict(
        quiz_id=1, key="q2", order=2,
        section_heading="",
        question_text="According to the lecture, how many windows are used in focused cardiac ultrasound (FOCUS)?",
        choice_a="Two",
        choice_b="Three",
        choice_c="Four",
        choice_d="Five",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'We'll be talking about three windows — the parasternal window, "
            "the apical window, and the subcostal window.'"
        ),
        label="Number of FOCUS windows",
    ),
    dict(
        quiz_id=1, key="q3", order=3,
        section_heading="",
        question_text="From the apical window, which view does the lecture describe obtaining?",
        choice_a="Long axis and short axis",
        choice_b="Subcostal IVC long axis",
        choice_c="Four-chamber view",
        choice_d="Parasternal long axis",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'From the apex, we'll have a four chamber.' "
            "The apical window provides the apical four-chamber view."
        ),
        label="Apical window view",
    ),
    dict(
        quiz_id=1, key="q4", order=4,
        section_heading="",
        question_text="The subcostal window is located:",
        choice_a="Just to the left of the sternum",
        choice_b="At the cardiac apex, just lateral and caudal to the nipple",
        choice_c="Just underneath the xiphoid process",
        choice_d="In the suprasternal notch",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'The subcostal, sometimes called subxiphoid window, "
            "which is right underneath the xiphoid process.'"
        ),
        label="Subcostal window location",
    ),
    # ── Patient Positioning ───────────────────────────────────────────────────
    dict(
        quiz_id=1, key="q5", order=5,
        section_heading="Patient Positioning & Exam Principles",
        question_text=(
            "For both parasternal and apical windows, the patient is ideally positioned in:"
        ),
        choice_a="Supine with head elevated 30 degrees",
        choice_b="Right lateral decubitus",
        choice_c="Sitting upright at 90 degrees",
        choice_d="Left lateral decubitus with the left arm up behind the head",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture states: 'We will position our patients for both the apical and "
            "parasternal windows in the left lateral decubitus position all the way up on "
            "their side with the left arm up kinda behind the head there, which spreads "
            "the ribs apart.'"
        ),
        label="Patient positioning for parasternal/apical",
    ),
    dict(
        quiz_id=1, key="q6", order=6,
        section_heading="",
        question_text="The focused cardiac exam is designed to be which type of assessment?",
        choice_a="Quantitative and spectral",
        choice_b="Qualitative and relatively binary",
        choice_c="Comprehensive like a formal echocardiogram",
        choice_d="Doppler-based and color flow",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'Our focus exam, as an extension of the physical exam, "
            "is designed to be qualitative and relatively binary — are we or are we not "
            "worried about abnormalities?'"
        ),
        label="Nature of the focused exam",
    ),
    dict(
        quiz_id=1, key="q7", order=7,
        section_heading="",
        question_text=(
            "Which of the following is NOT listed as an item assessed on the focused "
            "cardiac exam in the lecture?"
        ),
        choice_a="Global biventricular systolic function",
        choice_b="Relative chamber size",
        choice_c="Pericardial effusion",
        choice_d="Coronary artery anatomy",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture lists: relative chamber size, global biventricular systolic "
            "function, gross valvular abnormalities, pericardial effusion, and general "
            "volume status concepts. Coronary artery anatomy is not assessed."
        ),
        label="Item NOT assessed on FOCUS",
    ),
    # ── Intentional Practice ──────────────────────────────────────────────────
    dict(
        quiz_id=1, key="q8", order=8,
        section_heading="Keys to Success",
        question_text="What is described as 'intentional practice' in the lecture?",
        choice_a="Scanning every patient regardless of symptoms",
        choice_b="Reviewing each image with a cardiologist after scanning",
        choice_c=(
            "After achieving a good image, deliberately making it bad in a specific way "
            "then correcting it back to understand probe-image relationships"
        ),
        choice_d="Only practicing on difficult-to-image patients",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture describes intentional practice as: 'Once you've gotten the basics "
            "down — take a good image, make it bad in a very specific way, see if you're "
            "correct, then turn it from bad back to normal again. This is super valuable.'"
        ),
        label="Intentional practice",
    ),
    dict(
        quiz_id=1, key="q9", order=9,
        section_heading="",
        question_text=(
            "According to the lecture, the parasternal window is typically located:"
        ),
        choice_a="Below the clavicle, medial to the nipple",
        choice_b="Just to the left of the sternum",
        choice_c="At the cardiac apex lateral and caudal to the nipple",
        choice_d="Just caudal to the xiphoid process",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'The parasternal window being typically just to the left "
            "of the sternum — maybe it's in the third or fourth interspace.'"
        ),
        label="Parasternal window location",
    ),
    dict(
        quiz_id=1, key="q10", order=10,
        section_heading="",
        question_text=(
            "According to the lecture, affecting lung volumes in a ventilated patient can:"
        ),
        choice_a="Worsen imaging in all cases",
        choice_b="Have no significant impact on cardiac imaging",
        choice_c="Have a significant impact on cardiac image quality",
        choice_d="Only improve the subcostal window",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'Affecting lung volumes even in the ventilated patient "
            "can have a significant impact on your imaging.'"
        ),
        label="Lung volumes in ventilated patients",
    ),
]


QUIZ_2_QUESTIONS = [
    # ── Probe Orientation ─────────────────────────────────────────────────────
    dict(
        quiz_id=2, key="q1", order=1,
        section_heading="Probe Orientation & Setup",
        question_text="For the parasternal long axis (PLAX), the probe indicator is pointed toward:",
        choice_a="The patient's left shoulder",
        choice_b="The patient's right hip",
        choice_c="The patient's right shoulder",
        choice_d="The sternum",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'We're gonna point our indicator toward the patient's "
            "right shoulder' for the parasternal long axis view."
        ),
        label="PLAX indicator direction",
    ),
    dict(
        quiz_id=2, key="q2", order=2,
        section_heading="",
        question_text=(
            "Using the abdominal mode/preset instead of cardiac mode will make the "
            "PLAX image appear:"
        ),
        choice_a="Too deep to interpret",
        choice_b="180 degrees flipped compared to cardiac mode",
        choice_c="With excessive gain",
        choice_d="Without the left ventricle",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'If you put the probe on and it looks a hundred and eighty "
            "degrees off, something's wrong in your settings — just flip your probe around, "
            "and it'll work out.' Abdominal mode flips the image 180 degrees vs cardiac mode."
        ),
        label="Effect of abdominal vs cardiac preset",
    ),
    # ── Probe Motions ─────────────────────────────────────────────────────────
    dict(
        quiz_id=2, key="q3", order=3,
        section_heading="Probe Motions",
        question_text="The 'rock' motion of the probe means:",
        choice_a="Moving the transducer to a new position on the skin",
        choice_b="Rotating the indicator to a new direction like a key",
        choice_c=(
            "Moving the tail toward or away from the indicator, staying in the same "
            "imaging plane while centering different structures"
        ),
        choice_d="Moving the tail perpendicular to the imaging plane",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture defines rock as 'motion in the plane of the beam — motion of the "
            "tail toward or away from the indicator' which keeps the same plane but centres "
            "a different portion of the heart on screen."
        ),
        label="Rock motion definition",
    ),
    dict(
        quiz_id=2, key="q4", order=4,
        section_heading="",
        question_text="The 'tilt' motion of the probe creates:",
        choice_a="A sliding motion that changes windows",
        choice_b="Rotation around the indicator",
        choice_c="The same imaging plane centered on a different structure",
        choice_d="New parallel imaging planes perpendicular to the original beam",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture defines tilt as 'moving the tail perpendicular to the plane of the "
            "beam, creating new parallel imaging planes' — in contrast to rock which stays "
            "in the same plane."
        ),
        label="Tilt motion definition",
    ),
    dict(
        quiz_id=2, key="q5", order=5,
        section_heading="",
        question_text=(
            "Tilting from the PLAX with the tail toward the patient's LEFT shoulder "
            "reveals:"
        ),
        choice_a="The LV apex",
        choice_b="Parasternal RV inflow — tricuspid valve and right ventricle",
        choice_c="The pulmonic valve and RVOT",
        choice_d="The subcostal four-chamber view",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'As I tilt one way from the parasternal long axis — tail "
            "toward the patient's left shoulder — I see the parasternal RV inflow, the "
            "tricuspid valve and right ventricle.'"
        ),
        label="Tilting tail toward left shoulder",
    ),
    # ── Window Shopping ───────────────────────────────────────────────────────
    dict(
        quiz_id=2, key="q6", order=6,
        section_heading="Window Shopping & Breath Control",
        question_text="'Window shopping' in the context of probe technique refers to:",
        choice_a="Selecting the imaging preset from a machine menu",
        choice_b="Reviewing saved images after scanning",
        choice_c="Sliding the probe across multiple interspaces to find the best imaging window",
        choice_d="Rotating the probe to compare long and short axis views",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture describes window shopping as sliding — moving the probe to "
            "different interspaces 'walking from window to window' to find the best "
            "parasternal window before optimizing the image."
        ),
        label="Window shopping definition",
    ),
    dict(
        quiz_id=2, key="q7", order=7,
        section_heading="",
        question_text=(
            "For parasternal imaging, the window is typically improved when the patient:"
        ),
        choice_a="Takes a deep breath in and holds it",
        choice_b="Breathes normally",
        choice_c="Is sitting at 30 degrees",
        choice_d="Breathes all the way out and holds it",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture states: 'For me, unless I breathe all the way out and hold it all "
            "the way out, it's really hard to make any parasternal window at all.' As patients "
            "exhale, the left lung moves away from the sternum improving the window."
        ),
        label="Breath hold for parasternal window",
    ),
    # ── Qualitative Assessment ────────────────────────────────────────────────
    dict(
        quiz_id=2, key="q8", order=8,
        section_heading="Qualitative Image Assessment",
        question_text=(
            "In the PLAX, the RVOT, aortic root/sinuses, and left atrium should appear:"
        ),
        choice_a="In a 1:2:4 size ratio",
        choice_b="With the LA significantly larger than the RVOT",
        choice_c="Approximately the same size",
        choice_d="With the RVOT always larger than the LA",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states a qualitative guide: 'RVOT, aortic root and sinuses, and "
            "left atrium — these should be relatively the same size.' A reference marker "
            "the size of the RVOT should fit the sinuses and LA approximately."
        ),
        label="Relative size of RVOT, aortic root, LA",
    ),
    dict(
        quiz_id=2, key="q9", order=9,
        section_heading="",
        question_text=(
            "As a qualitative guide, if LV wall thickness in diastole is 1 unit, the "
            "aortic annulus should be approximately:"
        ),
        choice_a="The same (1 unit)",
        choice_b="2 units",
        choice_c="4 units",
        choice_d="0.5 units",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'Wall thickness in diastole is, give or take, half the "
            "aortic annulus — if wall thickness is 1, our annulus would be 2, and our "
            "chamber size would be 4.' Wall thickness approaching annulus size suggests "
            "significant hypertrophy."
        ),
        label="Aortic annulus vs wall thickness ratio",
    ),
    dict(
        quiz_id=2, key="q10", order=10,
        section_heading="",
        question_text="'Sliding' as a probe motion refers to:",
        choice_a="Moving the tail toward or away from the indicator",
        choice_b="Moving the tail perpendicular to the beam plane",
        choice_c="Rotating the probe around the indicator",
        choice_d="Moving the transducer on the patient's skin to a new window location",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture defines sliding (translating) as 'moving the transducer on the "
            "patient's skin — changing windows, moving it from one spot to the next.' "
            "It is distinct from rock, tilt, and rotate."
        ),
        label="Sliding definition",
    ),
]


QUIZ_3_QUESTIONS = [
    # ── Probe Setup ───────────────────────────────────────────────────────────
    dict(
        quiz_id=3, key="q1", order=1,
        section_heading="Probe Setup & Standard Level",
        question_text=(
            "To move from the parasternal long axis (PLAX) to the parasternal short axis "
            "(PSAX), the probe indicator is rotated to point toward:"
        ),
        choice_a="The patient's right shoulder",
        choice_b="The patient's left shoulder",
        choice_c="The xiphoid process",
        choice_d="The right hip",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'In the parasternal long axis we had the indicator pointed "
            "toward the patient's right shoulder. Now we're gonna rotate just ninety degrees "
            "— indicator pointed toward the left shoulder.'"
        ),
        label="PSAX indicator direction",
    ),
    dict(
        quiz_id=3, key="q2", order=2,
        section_heading="",
        question_text=(
            "The standard focus-level parasternal short axis view is obtained at the level of:"
        ),
        choice_a="The aortic valve",
        choice_b="The mitral valve",
        choice_c="The papillary muscles (mid LV)",
        choice_d="The LV apex",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'For our most basic focus ultrasound, we're gonna be at "
            "the level of the papillary muscles — right ventricle, all left ventricle, "
            "and papillary muscles.'"
        ),
        label="Standard FOCUS PSAX level",
    ),
    # ── Tilt Range ────────────────────────────────────────────────────────────
    dict(
        quiz_id=3, key="q3", order=3,
        section_heading="Tilt Range",
        question_text=(
            "In the PSAX, tilting the probe allows scanning from:"
        ),
        choice_a="Right ventricle to left ventricle",
        choice_b="Apex through mid LV to the base and aortic valve level",
        choice_c="IVC to the aorta",
        choice_d="Tricuspid valve to the pulmonic valve only",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture describes: 'We're gonna start off at the apex of the LV — tip "
            "the tail down to the mid portion where the papillary muscles are — keep "
            "tipping down — now we see the mitral valve — now the aortic valve in short "
            "axis.' Full tilt range goes from apex to aortic valve level."
        ),
        label="Tilt range in PSAX",
    ),
    # ── Clinical Assessment ───────────────────────────────────────────────────
    dict(
        quiz_id=3, key="q4", order=4,
        section_heading="Clinical Assessment",
        question_text=(
            "According to the lecture, significant flattening of the interventricular "
            "septum on PSAX raises concern for:"
        ),
        choice_a="LV systolic dysfunction",
        choice_b="Hypertrophic cardiomyopathy",
        choice_c="Pericardial effusion",
        choice_d="Right heart pathology",
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture states: 'Significant flattening of the interventricular septum "
            "is a concern about the right heart.' In a normal PSAX, the LV should appear "
            "circular throughout systole and diastole."
        ),
        label="Septal flattening significance",
    ),
    dict(
        quiz_id=3, key="q5", order=5,
        section_heading="",
        question_text=(
            "The lecture states that the mid-papillary PSAX includes visualization of "
            "which coronary territories?"
        ),
        choice_a="Only LAD and RCA",
        choice_b="LAD, circumflex (LCx/SERC), and RCA territories",
        choice_c="Only the LAD territory",
        choice_d="RCA and circumflex only",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture states: 'It's worth understanding that we do see both LAD, SERC, "
            "and RCA territories in this view.' All three major coronary territories are "
            "represented at the mid-papillary level."
        ),
        label="Coronary territories in PSAX",
    ),
    # ── LV Segmentation ───────────────────────────────────────────────────────
    dict(
        quiz_id=3, key="q6", order=6,
        section_heading="LV Segmentation",
        question_text=(
            "How many mid-level segments of the left ventricle are described in the "
            "PSAX at the papillary muscle level?"
        ),
        choice_a="Four",
        choice_b="Eight",
        choice_c="Six",
        choice_d="Sixteen",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'We describe six walls of the left ventricle and sixteen "
            "segments in echocardiography.' At the mid level there are six segments — "
            "three anterior and three inferior."
        ),
        label="Number of mid-level LV segments",
    ),
    dict(
        quiz_id=3, key="q7", order=7,
        section_heading="",
        question_text=(
            "When tilting all the way to the most anterior/basal position from the "
            "mid-papillary PSAX, you obtain:"
        ),
        choice_a="The apical four-chamber view",
        choice_b="The subcostal IVC view",
        choice_c="The aortic valve short axis, also showing RVOT, tricuspid, and pulmonic valves",
        choice_d="The parasternal long axis",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'Now I see the aortic valve in short axis — this is sort "
            "of the aortic valve short axis, also the right ventricular inflow-outflow "
            "view. So this is tricuspid and pulmonic valves here.'"
        ),
        label="Most anterior tilt view",
    ),
    # ── Image Quality Pitfalls ────────────────────────────────────────────────
    dict(
        quiz_id=3, key="q8", order=8,
        section_heading="Image Quality Pitfalls",
        question_text=(
            "If the PLAX shows the LV axis at an angle (not horizontal on screen) and you "
            "then rotate to PSAX, the expected result is:"
        ),
        choice_a="A perfectly circular LV",
        choice_b="Loss of all cardiac structures",
        choice_c=(
            "An oval or egg-shaped LV that may mimic septal flattening and confuse "
            "wall motion assessment"
        ),
        choice_d="The mitral valve appearing in the center",
        choice_e="",
        correct_answer="C",
        explanation=(
            "The lecture states: 'If this is the window, we're not going to be able to "
            "make a true short axis cross section of the LV — we're gonna get this weird "
            "orthogonal view that is likely to look oblong. It's gonna look oval, and it's "
            "gonna confuse us. It may make it appear that there's septal flattening.'"
        ),
        label="Angled PLAX effect on PSAX",
    ),
    dict(
        quiz_id=3, key="q9", order=9,
        section_heading="",
        question_text=(
            "The two septal segment names in the mid-papillary PSAX are:"
        ),
        choice_a="Anterior and inferior",
        choice_b="Anteroseptal and inferoseptal",
        choice_c="Lateral and posterior",
        choice_d="Anterolateral and inferolateral",
        choice_e="",
        correct_answer="B",
        explanation=(
            "The lecture names the segments: 'I have anteroseptum, anterior, anterolateral, "
            "inferoseptal, inferior, inferolateral — two septal segments between the RV "
            "and the LV, two lateral segments.'"
        ),
        label="Two septal segment names",
    ),
    dict(
        quiz_id=3, key="q10", order=10,
        section_heading="",
        question_text=(
            "When the probe barely catches the edge of a rib during PSAX imaging, the "
            "expected image result is:"
        ),
        choice_a="The image turns completely black",
        choice_b="No change to image quality",
        choice_c="The rib casts a bright artifact across the whole image",
        choice_d=(
            "The image may appear just slightly crummy without being totally black — "
            "small micro-adjustments to the probe position can sharpen it"
        ),
        choice_e="",
        correct_answer="D",
        explanation=(
            "The lecture states: 'When your transducer is over a rib, you might imagine "
            "your image would turn completely black — but that's not quite how it works. "
            "Because we can just catch the edge of a rib, refract the ultrasound, and make "
            "the image just a little bit crummy. These little motions can just help sharpen "
            "your image a little bit.'"
        ),
        label="Probe barely over rib edge",
    ),
]


def reseed_quizzes_1_3(apps, schema_editor):
    QuizQuestion = apps.get_model("logbook", "QuizQuestion")
    QuizQuestion.objects.filter(quiz_id__in=[1, 2, 3]).delete()
    for q in QUIZ_1_QUESTIONS + QUIZ_2_QUESTIONS + QUIZ_3_QUESTIONS:
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
    QuizQuestion.objects.filter(quiz_id__in=[1, 2, 3]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0020_update_protocols_from_pdfs"),
    ]

    operations = [
        migrations.RunPython(reseed_quizzes_1_3, reverse_reseed),
    ]
