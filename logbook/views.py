import difflib

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth import login
from django.db import models
from django.db.models import Count, Avg, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import ClinicalCase, CaseStep
from .models import QuizAttempt, QuizBestScore, QuizQuestion, QuizShortAnswer
from .models import Resource, POCUSProtocol
from .forms import ScanForm
from .models import Scan

User = get_user_model()

# Total number of quizzes available in the curriculum
TOTAL_QUIZZES = 10

# Quiz data
QUIZZES = {
    1: {
        "title": "E-FAST + US-Guided CVC Basics",
        "template": "logbook/quiz_1.html",
        "questions": {
            "q1": "C",
            "q2": "B",
            "q3": "C",
            "q4": "B",
            "q5": "B",
        },
        "question_labels": {
            "q1": "Primary purpose of E-FAST in trauma",
            "q2": "Most sensitive E-FAST area for free fluid",
            "q3": "Key advantage of US-guided CVC",
            "q4": "Risk of short-axis needle advancement",
            "q5": "True statement about POCUS",
        },
        "short_answers": {
            "sa1": {
                "prompt": "Briefly describe the E-FAST exam: what does it stand for and which body cavities does it assess?",
                "keywords": [
                    "extended", "focused", "assessment", "sonography", "trauma",
                    "peritoneal", "pericardial", "pleural", "thorax", "lung",
                    "pneumothorax", "hemothorax", "free fluid", "abdominal",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "E-FAST stands for Extended Focused Assessment with Sonography in Trauma. "
                    "It assesses the peritoneal cavity (for free fluid/hemoperitoneum), "
                    "the pericardial space (for tamponade), and bilateral pleural cavities "
                    "(for pneumothorax and hemothorax)."
                ),
            }
        },
    },
    2: {
        "title": "POCUS Session #1 - Pre-Session Quiz",
        "template": "logbook/quiz_2.html",
        "questions": {
            "q1": "B",
            "q2": "B",
            "q3": "B",
            "q4": "B",
            "q5": "B",
            "q6": "A",
            "q7": "A",
            "q8": "B",
            "q9": "B",
            "q10": "A",
        },
        "question_labels": {
            "q1": "Ultrasound wave property",
            "q2": "Probe frequency and penetration",
            "q3": "Aorta normal diameter",
            "q4": "AAA definition",
            "q5": "Aorta measurement technique",
            "q6": "B-line characteristics",
            "q7": "Lung sliding significance",
            "q8": "Pleural effusion appearance",
            "q9": "IVC and volume status",
            "q10": "POCUS limitation",
        },
        "short_answers": {
            "sa1": {
                "prompt": "Describe what ultrasound findings would be most concerning for an abdominal aortic aneurysm (AAA) and what measurement threshold is used.",
                "keywords": [
                    "aneurysm", "dilation", "dilated", "widened", "enlargement",
                    "3cm", "3 cm", "greater than 3", ">3", "diameter",
                    "anteroposterior", "AP", "outer wall", "transverse",
                    "rupture", "free fluid", "hematoma",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "An AAA is defined as aortic diameter >3 cm (outer wall to outer wall). "
                    "Concerning POCUS findings include an aorta measuring ≥3 cm in transverse "
                    "or anteroposterior diameter. Free fluid around the aorta suggests rupture "
                    "and is a surgical emergency."
                ),
            }
        },
    },
    3: {
        "title": "Focused Echo Pre-Session Quiz",
        "template": "logbook/quiz_3.html",
        "questions": {
            "q1": "D",
            "q2": "B",
            "q3": "B",
            "q4": "D",
            "q5": "C",
        },
        "question_labels": {
            "q1": "Chamber not visible in PLAX",
            "q2": "Apical 4-chamber probe position",
            "q3": "Differentiating pleural vs pericardial space",
            "q4": "Valve visibility in PSAX",
            "q5": "Fifth chamber on A4C tilt",
        },
        "short_answers": {
            "sa1": {
                "prompt": (
                    "Case A \u2014 New Onset Cardiomyopathy (PLAX view): "
                    "The EPSS measured on this scan is 23.7 mm. "
                    "What does EPSS measure, and what threshold suggests impaired LV systolic function?"
                ),
                "keywords": [
                    "E-point", "E point", "septal separation", "anterior leaflet", "mitral",
                    "interventricular septum", "septum", "systolic function", "ejection fraction",
                    "EF", "7mm", "7 mm", ">7", "reduced", "impaired", "dysfunction",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "EPSS measures the distance between the anterior mitral valve leaflet at its "
                    "E-point (peak early diastolic opening) and the interventricular septum. "
                    "Normal EPSS is <7 mm. An EPSS >7 mm suggests reduced LV systolic function. "
                    "An EPSS of 23.7 mm indicates severely reduced EF, consistent with EF <20%."
                ),
            },
            "sa2": {
                "prompt": (
                    "Case A \u2014 New Onset Cardiomyopathy (PLAX view): "
                    "Describe the key sonographic features visible on this PLAX image that are "
                    "consistent with dilated cardiomyopathy with severely reduced ejection fraction."
                ),
                "keywords": [
                    "dilated", "enlarged", "LV", "left ventricle", "dilation",
                    "hypokinesis", "poor contractility", "systolic dysfunction",
                    "cardiomyopathy", "globular", "EPSS", "mitral valve", "reduced",
                    "wall motion",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "PLAX findings of dilated cardiomyopathy with reduced EF include: "
                    "(1) Markedly dilated LV cavity \u2014 globular rather than oval. "
                    "(2) Global hypokinesis \u2014 reduced wall motion throughout. "
                    "(3) Elevated EPSS (>7 mm) reflecting poor LV contractility and reduced mitral valve opening. "
                    "In this case the LV is grossly dilated with an EPSS of 23.7 mm, correlating with EF <20%."
                ),
            },
            "sa3": {
                "prompt": (
                    "Case A \u2014 New Onset Cardiomyopathy: "
                    "This 47-year-old male has dyspnea and bilateral leg swelling. "
                    "Formal echo confirmed EF <20% with dilation of the LA, RA, and RV. "
                    "Explain how severely reduced LV function leads to these multi-chamber findings "
                    "and symptoms. What is the clinical term for this condition?"
                ),
                "keywords": [
                    "biventricular", "heart failure", "HFrEF", "congestion",
                    "pulmonary edema", "pulmonary hypertension", "right heart failure",
                    "peripheral edema", "venous congestion", "reduced ejection fraction",
                    "LA", "RV", "right ventricle", "dilation", "backward failure",
                    "left atrium", "forward failure",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "Severely reduced LV EF (<20%) causes: "
                    "(1) Elevated LV filling pressures back up into the LA \u2014 LA dilation and pulmonary "
                    "venous hypertension \u2014 pulmonary edema \u2014 dyspnea. "
                    "(2) Chronic pulmonary hypertension increases RV afterload \u2014 RV dilation and failure \u2014 "
                    "systemic venous congestion \u2014 RA dilation and peripheral leg edema. "
                    "This cascade is biventricular failure (HFrEF). All four chambers become involved."
                ),
            },
        },
    },
    4: {
        "title": "Ocular POCUS — Anatomy & Biosafety",
        "template": "logbook/quiz_4.html",
        "questions": {
            "q1": "C",
            "q2": "B",
            "q3": "B",
            "q4": "B",
            "q5": "B",
            "q6": "B",
            "q7": "B",
            "q8": "B",
            "q9": "C",
            "q10": "B",
        },
        "question_labels": {
            "q1": "Ocular probe selection and depth",
            "q2": "Globe pressure safety",
            "q3": "Anterior chamber thermal risk",
            "q4": "Safe TI and MI thresholds",
            "q5": "MSK preset safety concern",
            "q6": "Eye movement purpose during scan",
            "q7": "Optic nerve sonographic appearance",
            "q8": "Indications for ocular POCUS",
            "q9": "Gain management technique",
            "q10": "Pupillary response assessment technique",
        },
        "short_answers": {},
    },
    5: {
        "title": "Ocular Emergencies",
        "template": "logbook/quiz_5.html",
        "questions": {
            "q1": "B",
            "q2": "C",
            "q3": "C",
            "q4": "C",
            "q5": "B",
            "q6": "B",
            "q7": "B",
            "q8": "B",
            "q9": "B",
            "q10": "B",
        },
        "question_labels": {
            "q1": "Retinal detachment appearance",
            "q2": "Retinal vs vitreous detachment",
            "q3": "MAC off — macula involvement",
            "q4": "Vitreous hemorrhage in diabetics",
            "q5": "Combined retinal + choroidal detachment",
            "q6": "ONSD for elevated ICP",
            "q7": "Hyphema management",
            "q8": "Vitreous detachment features",
            "q9": "Ocular foreign body — gold standard",
            "q10": "Lens dislocation mechanism",
        },
        "short_answers": {},
    },
    6: {
        "title": "First Trimester Ultrasound",
        "template": "logbook/quiz_6.html",
        "questions": {
            "q1": "C", "q2": "C", "q3": "B", "q4": "C",
            "q5": "C", "q6": "C", "q7": "C", "q8": "C", "q9": "C", "q10": "C",
            "q11": "C", "q12": "C", "q13": "C", "q14": "C",
            "q15": "C", "q16": "B", "q17": "B",
            "q18": "B", "q19": "C", "q20": "B", "q21": "C",
            "q22": "C", "q23": "B",
            "q24": "C", "q25": "C", "q26": "C", "q27": "C",
            "q28": "C", "q29": "B",
            "q30": "B", "q31": "C",
            "q32": "C", "q33": "B",
            "q34": "B", "q35": "B",
            "q36": "C", "q37": "B", "q38": "D",
            "q39": "B", "q40": "B",
        },
        "question_labels": {
            "q1": "Primary goal of first trimester POCUS",
            "q2": "Heterotopic pregnancy risk",
            "q3": "Scanning sequence",
            "q4": "Free fluid assessment timing",
            "q5": "First step confirming IUP",
            "q6": "Gestational sac location",
            "q7": "What confirms IUP",
            "q8": "Myometrial mantle thickness",
            "q9": "NDIUP declaration",
            "q10": "Heterotopic risk factor",
            "q11": "Earliest GS visibility (TA)",
            "q12": "Discriminatory β-hCG (TA)",
            "q13": "FEEDS criteria",
            "q14": "Minimum GS size in FEEDS",
            "q15": "Pseudogestational sac feature",
            "q16": "True gestational sac appearance",
            "q17": "Pseudogestational sac size",
            "q18": "Yolk sac appearance timing",
            "q19": "Fetal pole appearance timing",
            "q20": "CRL for cardiac activity",
            "q21": "FHR <100 significance",
            "q22": "NDIUP differential",
            "q23": "Empty uterus + β-hCG >3000",
            "q24": "Most specific ectopic sign",
            "q25": "Tubal ring sign",
            "q26": "Free fluid to Morrison's pouch",
            "q27": "Empty uterus + free fluid",
            "q28": "Most common 1st trimester bleeding cause",
            "q29": "Large subchorionic hemorrhage outcome",
            "q30": "Diagnostic of pregnancy failure",
            "q31": "CRL cutoff for failed pregnancy",
            "q32": "Blighted ovum definition",
            "q33": "Blighted ovum diagnostic feature",
            "q34": "Molar pregnancy ultrasound finding",
            "q35": "Molar pregnancy mimics",
            "q36": "β-hCG and ectopic",
            "q37": "TA ultrasound limitation",
            "q38": "Peak ectopic rupture timing",
            "q39": "Fetal loss with cardiac activity",
            "q40": "Empty uterus + bleeding/cramping",
        },
        "short_answers": {},
    },
    7: {
        "title": "Abdominal Aortic Aneurysm (AAA)",
        "template": "logbook/quiz_7.html",
        "questions": {
            "q1": "C", "q2": "D", "q3": "C", "q4": "B",
            "q5": "B", "q6": "C", "q7": "B", "q8": "C",
            "q9": "C", "q10": "C", "q11": "B", "q12": "C",
        },
        "question_labels": {
            "q1": "AAA probe",
            "q2": "AAA depth",
            "q3": "AAA external landmark",
            "q4": "AAA internal landmark",
            "q5": "Aorta position vs IVC",
            "q6": "Aorta non-compressibility",
            "q7": "Normal aortic calibre",
            "q8": "Probe angle pitfall",
            "q9": "Chronic thrombus measurement",
            "q10": "Indeterminate scan definition",
            "q11": "Clinical integration pitfall",
            "q12": "Determinant positive — AAA shape",
        },
        "short_answers": {
            "sa1": {
                "prompt": "In one sentence, state what defines a determinant negative AAA scan.",
                "keywords": [
                    "outer wall", "xiphoid", "iliac bifurcation", "3cm", "exceeds",
                    "entire", "visualized", "evaluation",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "A determinant negative scan is evaluation of the outer wall of the abdominal aorta "
                    "from the xiphoid process to the iliac bifurcation where at no point the outer wall exceeds 3cm."
                ),
            },
            "sa2": {
                "prompt": "In one sentence, name two troubleshooting manoeuvres from the document for when bowel gas obstructs aortic visualization.",
                "keywords": [
                    "flex", "hips", "knees", "firm", "probe", "pressure",
                    "breath", "deep", "slide", "laterally", "heel", "medially",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "Troubleshooting options include flexing the patient's hips and knees, using firm probe pressure "
                    "and hold, asking the patient to take a deep breath in and hold it or exhale, and sliding "
                    "laterally while heeling medially to move around loops of bowel."
                ),
            },
            "sa3": {
                "prompt": "In one sentence, describe what the document states about saccular aneurysms and their surgical significance compared to fusiform AAA.",
                "keywords": [
                    "saccular", "any size", "surgical", "determinant positive",
                    "overlooked", "methodical",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "Unlike fusiform aneurysms which are measured by diameter, a saccular aneurysm "
                    "is a determinant positive finding at any size because all saccular aneurysms "
                    "are treated surgically and can be easily overlooked without a methodical scan."
                ),
            },
        },
    },
    8: {
        "title": "Abdominal FAST Exam",
        "template": "logbook/quiz_8.html",
        "questions": {
            "q1": "C", "q2": "C", "q3": "B", "q4": "C",
            "q5": "C", "q6": "B", "q7": "D", "q8": "C",
            "q9": "B", "q10": "B", "q11": "B",
        },
        "question_labels": {
            "q1": "FAST probe",
            "q2": "FAST depth",
            "q3": "Upper quadrant internal landmark",
            "q4": "Upper quadrant probe plane",
            "q5": "Most sensitive free fluid site",
            "q6": "Most likely LUQ free fluid site",
            "q7": "Minimum hemoperitoneum ruled out",
            "q8": "Male pelvic false positive structure",
            "q9": "Pelvic AOI in males",
            "q10": "Trendelenberg tip",
            "q11": "Clinical integration pitfall",
        },
        "short_answers": {
            "sa1": {
                "prompt": (
                    "In one sentence, describe the Tips and Tricks manoeuvre the document specifies "
                    "for ensuring you can see the liver/kidney or spleen/kidney interface during "
                    "the upper quadrant FAST views."
                ),
                "keywords": [
                    "slide", "posteriorly", "anteriorly", "kidney", "interface",
                    "probe", "solid organ",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "The document states the kidney does not define the interface; the probe must "
                    "slide posteriorly and anteriorly to ensure you can see both the solid organ "
                    "and the renal interface clearly."
                ),
            },
            "sa2": {
                "prompt": (
                    "In one sentence, name the external landmark and describe the probe starting "
                    "orientation for the pelvic FAST view, as stated in the document."
                ),
                "keywords": [
                    "symphysis pubis", "cephalad", "transverse", "bladder", "pelvic",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "The probe is placed just cephalad to the symphysis pubis in the transverse "
                    "plane, using the bladder as an acoustic window to visualize the pelvic structures."
                ),
            },
            "sa3": {
                "prompt": (
                    "In one sentence, name two substances other than blood that could cause a "
                    "positive-appearing FAST exam, as listed in the document."
                ),
                "keywords": [
                    "ascites", "urine", "dialysate", "bowel contents",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "The document lists ascites, urine, dialysate, and bowel contents as substances "
                    "that can appear as free fluid on the FAST exam and be mistaken for hemoperitoneum."
                ),
            },
        },
    },
    9: {
        "title": "OB POCUS — Scanning Technique & 3-2-1 Rule",
        "template": "logbook/quiz_9.html",
        "questions": {
            "q1": "B", "q2": "C", "q3": "B", "q4": "C",
            "q5": "C", "q6": "B", "q7": "C", "q8": "B",
            "q9": "B", "q10": "C", "q11": "B", "q12": "C",
        },
        "question_labels": {
            "q1": "Primary goal of OB POCUS",
            "q2": "Number of pregnancy criteria",
            "q3": "Double ring sign",
            "q4": "Yolk sac — TVUS timing",
            "q5": "Minimum FHR for good outcome",
            "q6": "Minimum myometrial mantle",
            "q7": "Pregnancy failure — CRL criterion",
            "q8": "Bladder-uterine juxtaposition",
            "q9": "Full bladder reason",
            "q10": "OB probe",
            "q11": "Vaginal uterine continuity",
            "q12": "Clinical integration pitfall",
        },
        "short_answers": {
            "sa1": {
                "prompt": (
                    "In one sentence, list all three pregnancy criteria from the 3-2-1 rule "
                    "that must be met to confirm an intrauterine pregnancy."
                ),
                "keywords": [
                    "decidual reaction", "gestational sac", "yolk sac",
                    "fetal pole", "fetal heart", "three",
                ],
                "min_keywords": 3,
                "sample_answer": (
                    "The three pregnancy criteria that must all be present are: a decidual reaction, "
                    "a gestational sac, and a yolk sac OR a fetal pole with visible fetal heart activity."
                ),
            },
            "sa2": {
                "prompt": (
                    "In one sentence, state the gestational sac size threshold above which the "
                    "absence of a yolk sac constitutes pregnancy failure, as listed in the document."
                ),
                "keywords": [
                    "gestational sac", "15mm", "yolk sac", "failure", "pregnancy failure",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "Pregnancy failure is indicated when no yolk sac is present with a gestational "
                    "sac measuring greater than 15mm."
                ),
            },
            "sa3": {
                "prompt": (
                    "In one sentence, state the BhCG level above which the absence of a gestational "
                    "sac on transabdominal scanning indicates pregnancy failure, as listed in the document."
                ),
                "keywords": [
                    "BhCG", "3000", "transabdominal", "gestational sac", "failure",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "The document lists pregnancy failure when there is no gestational sac on "
                    "transabdominal scanning with a BhCG greater than 3000."
                ),
            },
        },
    },
    10: {
        "title": "Pneumothorax POCUS",
        "template": "logbook/quiz_10.html",
        "questions": {
            "q1": "C", "q2": "B", "q3": "C", "q4": "B",
            "q5": "B", "q6": "B", "q7": "C", "q8": "C",
            "q9": "C", "q10": "C", "q11": "B", "q12": "C",
        },
        "question_labels": {
            "q1": "Best image quality probe",
            "q2": "PTX starting depth",
            "q3": "External landmark",
            "q4": "Lung sliding definition",
            "q5": "Lung pulse definition",
            "q6": "True lung point",
            "q7": "Number of pleural spaces",
            "q8": "Determinate negative scan",
            "q9": "Stable patient — lung point protocol",
            "q10": "Large PTX — lung point location",
            "q11": "False positive — right mainstem",
            "q12": "Small PTX clinical pitfall",
        },
        "short_answers": {
            "sa1": {
                "prompt": (
                    "In one sentence, define comet tails or B-lines as described in the pneumothorax "
                    "document and explain what their presence at the pleural line indicates."
                ),
                "keywords": [
                    "comet tails", "B-lines", "vertical", "reverberation",
                    "pleural line", "lung", "contact", "aerated",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "Comet tails or B-lines are vertical reverberation artifacts arising from the "
                    "pleural line, confirming that aerated lung tissue is in contact with the chest wall."
                ),
            },
            "sa2": {
                "prompt": (
                    "In one sentence, describe the two M-mode patterns used in pneumothorax assessment "
                    "and what each indicates, as described in the document."
                ),
                "keywords": [
                    "seashore", "barcode", "M-mode", "sliding", "absent", "pneumothorax",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "On M-mode, the seashore sign indicates normal lung sliding is present, while the "
                    "barcode sign (parallel horizontal lines) indicates absent lung sliding and is "
                    "consistent with pneumothorax."
                ),
            },
            "sa3": {
                "prompt": (
                    "In one sentence, describe what the document states about declaring a pneumothorax "
                    "in an unstable patient when lung sliding, comet tails, and lung pulse are all absent."
                ),
                "keywords": [
                    "unstable", "absent", "lung point", "declare", "pneumothorax",
                    "rib space", "respiratory cycles",
                ],
                "min_keywords": 2,
                "sample_answer": (
                    "In an unstable patient, if lung sliding, comet tails, and lung pulse are all absent "
                    "in at least one rib space over three respiratory cycles, a pneumothorax can be "
                    "declared without needing to identify a lung point."
                ),
            },
        },
    },
}

# Keep QUIZ_1 for backward compatibility
QUIZ_1 = QUIZZES[1]


# ---------------------------------------------------------------------------
# Short-answer scoring helper
# ---------------------------------------------------------------------------
def score_short_answer(user_answer, keywords, threshold=0.75):
    """
    Score a free-text answer against a list of target keywords using fuzzy
    matching.  Returns (matched_count, total_keywords, matched_keywords).
    """
    if not user_answer or not keywords:
        return 0, len(keywords), []

    answer_lower = user_answer.lower()
    # Tokenise the answer into individual words for word-level fuzzy matching
    answer_words = answer_lower.split()
    matched = []

    for keyword in keywords:
        kw_lower = keyword.lower()
        # 1. Exact substring match (handles multi-word keywords like "free fluid")
        if kw_lower in answer_lower:
            matched.append(keyword)
            continue
        # 2. Fuzzy word-level match for single words
        for word in answer_words:
            ratio = difflib.SequenceMatcher(None, kw_lower, word).ratio()
            if ratio >= threshold:
                matched.append(keyword)
                break

    return len(matched), len(keywords), matched


# ---------------------------------------------------------------------------
# Email notification helper
# ---------------------------------------------------------------------------
def send_quiz_completion_email(user, quiz, quiz_id, score, total,
                               answer_key, submitted_answers,
                               is_new_best, sa_results=None):
    """Send quiz-completion email to the learner."""
    if not user.email:
        return

    percentage = round((score / total) * 100) if total > 0 else 0
    passed = percentage >= 70
    status_line = "PASSED ✓" if passed else "Did not pass (70% required)"
    new_best_note = "  — New personal best!" if is_new_best else ""

    # Build wrong-answer summary
    wrong_lines = []
    for q_key, correct in answer_key.items():
        user_ans = submitted_answers.get(q_key)
        if user_ans != correct:
            q_num = q_key.replace("q", "")
            user_ans_str = user_ans if user_ans else "not answered"
            wrong_lines.append(
                f"  Q{q_num}: your answer = {user_ans_str}  |  correct = {correct}"
            )

    wrong_section = ""
    if wrong_lines:
        wrong_section = "Questions to review:\n" + "\n".join(wrong_lines) + "\n\n"
    else:
        wrong_section = "Perfect score — excellent work!\n\n"

    # Short-answer section
    sa_section = ""
    if sa_results:
        sa_lines = []
        for sa_key, sa_data in sa_results.items():
            sa_num = sa_key.replace("sa", "")
            matched = sa_data.get("matched_keywords", [])
            sa_lines.append(
                f"  SA{sa_num}: {sa_data['prompt'][:80]}...\n"
                f"    Your answer: {sa_data['user_answer'][:200]}\n"
                f"    Keywords matched: {', '.join(matched) if matched else 'none detected'}\n"
                f"    Sample answer: {sa_data['sample_answer'][:300]}"
            )
        sa_section = "Short-answer questions (for self-review):\n" + "\n".join(sa_lines) + "\n\n"

    subject = (
        f"[POCUS Portal] Quiz Complete: {quiz['title']} — "
        f"{score}/{total} ({percentage}%)"
    )
    body = (
        f"Hi {user.get_full_name() or user.username},\n\n"
        f"You completed: {quiz['title']}\n"
        f"Score: {score}/{total} ({percentage}%) — {status_line}{new_best_note}\n\n"
        f"{wrong_section}"
        f"{sa_section}"
        f"Keep up the great work on your POCUS training!\n\n"
        f"— POCUS Portal"
    )

    try:
        send_mail(
            subject,
            body,
            django_settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        pass  # Never let email failure break quiz submission


def send_admin_quiz_notification(user, quiz, quiz_id, score, total,
                                 answer_key, submitted_answers, sa_results=None):
    """Send a quiz-completion notification to all staff/admin users."""
    admin_emails = list(
        User.objects.filter(is_staff=True).exclude(email="").values_list("email", flat=True)
    )
    if not admin_emails:
        return

    percentage = round((score / total) * 100) if total > 0 else 0
    passed = percentage >= 70
    status_line = "PASSED ✓" if passed else "Did not pass"

    # MC wrong answers
    wrong_lines = []
    for q_key, correct in answer_key.items():
        user_ans = submitted_answers.get(q_key)
        if user_ans != correct:
            q_num = q_key.replace("q", "")
            wrong_lines.append(
                f"  Q{q_num}: answered {user_ans or 'skipped'}  |  correct: {correct}"
            )
    wrong_section = (
        "Wrong answers:\n" + "\n".join(wrong_lines) + "\n\n"
        if wrong_lines else "All MC questions correct.\n\n"
    )

    # SA responses
    sa_section = ""
    if sa_results:
        sa_lines = []
        for sa_key, sa_data in sa_results.items():
            sa_num = sa_key.replace("sa", "")
            matched = sa_data.get("matched_keywords", [])
            auto = "Auto-pass" if sa_data.get("auto_passed") else "Needs review"
            sa_lines.append(
                f"  SA{sa_num} [{auto}]: {sa_data['prompt'][:80]}...\n"
                f"    Response: {sa_data['user_answer'][:300] or '(blank)'}\n"
                f"    Keywords matched: {', '.join(matched) if matched else 'none'}"
            )
        sa_section = "Short answers:\n" + "\n".join(sa_lines) + "\n\n"

    subject = (
        f"[POCUS Portal] {user.username} completed: {quiz['title']} — "
        f"{score}/{total} ({percentage}%) {status_line}"
    )
    body = (
        f"A learner has completed a quiz on POCUS Portal.\n\n"
        f"User:    {user.get_full_name() or user.username} ({user.email or 'no email'})\n"
        f"Quiz:    {quiz['title']}\n"
        f"Score:   {score}/{total} ({percentage}%) — {status_line}\n\n"
        f"{wrong_section}"
        f"{sa_section}"
        f"View all scores: /admin/quiz-analytics/\n\n"
        f"— POCUS Portal"
    )

    try:
        send_mail(
            subject,
            body,
            django_settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            fail_silently=True,
        )
    except Exception:
        pass


# Quiz home page showing all available quizzes
@login_required
def quizzes_home(request):
    # Get user's best scores for all quizzes
    user_best_scores = {
        score.quiz_id: score
        for score in QuizBestScore.objects.filter(user=request.user)
    }

    # Calculate statistics
    quizzes_completed = len(user_best_scores)
    quizzes_passed = sum(1 for score in user_best_scores.values() if score.passed)

    # Calculate average score
    if user_best_scores:
        avg_score = sum(score.percentage for score in user_best_scores.values()) / len(user_best_scores)
    else:
        avg_score = None

    return render(request, "logbook/quizzes_home.html", {
        "user_best_scores": user_best_scores,
        "quizzes_completed": quizzes_completed,
        "quizzes_passed": quizzes_passed,
        "avg_score": avg_score,
        "total_quizzes": TOTAL_QUIZZES,
    })

# Individual quiz detail page
@login_required
def quiz_detail(request, quiz_id):
    if quiz_id not in QUIZZES:
        return render(request, "logbook/quiz_unavailable.html", {"quiz_id": quiz_id})

    quiz = QUIZZES[quiz_id]

    # Load questions from DB; fall back to QUIZZES dict for answer key
    db_questions = list(QuizQuestion.objects.filter(quiz_id=quiz_id).order_by('order'))
    if db_questions:
        answer_key = {q.key: q.correct_answer for q in db_questions}
    else:
        answer_key = quiz["questions"]

    total = len(answer_key)

    # Load SA definitions: merge DB records over QUIZZES dict defaults
    db_sa_map = {sa.key: sa for sa in QuizShortAnswer.objects.filter(quiz_id=quiz_id)}
    quizzes_sa = quiz.get("short_answers", {})
    short_answer_defs = {}
    for sa_key, sa_def in quizzes_sa.items():
        db_sa = db_sa_map.get(sa_key)
        short_answer_defs[sa_key] = {
            "prompt": db_sa.prompt if db_sa else sa_def["prompt"],
            "keywords": db_sa.keywords_list() if db_sa else sa_def.get("keywords", []),
            "min_keywords": db_sa.min_keywords if db_sa else sa_def.get("min_keywords", 1),
            "sample_answer": db_sa.sample_answer if db_sa else sa_def.get("sample_answer", ""),
            "image_url": db_sa.image_url if db_sa else "",
        }
    # Also include any SA keys only in DB (not in QUIZZES dict)
    for sa_key, db_sa in db_sa_map.items():
        if sa_key not in short_answer_defs:
            short_answer_defs[sa_key] = {
                "prompt": db_sa.prompt,
                "keywords": db_sa.keywords_list(),
                "min_keywords": db_sa.min_keywords,
                "sample_answer": db_sa.sample_answer,
                "image_url": db_sa.image_url,
            }

    submitted_answers = {}
    score = None
    is_new_best = False
    previous_best = QuizBestScore.objects.filter(user=request.user, quiz_id=quiz_id).first()
    sa_results = {}

    if request.method == "POST":
        submitted_answers = {q: request.POST.get(q) for q in answer_key.keys()}
        score = sum(1 for q, correct in answer_key.items() if submitted_answers.get(q) == correct)

        for sa_key, sa_def in short_answer_defs.items():
            user_sa = (request.POST.get(sa_key) or "").strip()
            matched_count, total_kw, matched_kws = score_short_answer(
                user_sa, sa_def["keywords"]
            )
            sa_results[sa_key] = {
                "prompt": sa_def["prompt"],
                "user_answer": user_sa,
                "matched_keywords": matched_kws,
                "matched_count": matched_count,
                "total_keywords": total_kw,
                "min_keywords": sa_def.get("min_keywords", 1),
                "sample_answer": sa_def["sample_answer"],
                "auto_passed": matched_count >= sa_def.get("min_keywords", 1),
            }
            submitted_answers[sa_key] = user_sa

        QuizAttempt.objects.create(
            user=request.user,
            quiz_id=quiz_id,
            quiz_title=quiz["title"],
            answers=submitted_answers,
            score=score,
            total=total,
        )

        best_score, created = QuizBestScore.objects.get_or_create(
            user=request.user,
            quiz_id=quiz_id,
            defaults={
                "quiz_title": quiz["title"],
                "best_score": score,
                "total": total,
                "attempts": 1,
            }
        )

        if not created:
            best_score.attempts += 1
            if score > best_score.best_score:
                best_score.best_score = score
                is_new_best = True
            best_score.save()
        else:
            is_new_best = True

        mc_answers = {k: v for k, v in submitted_answers.items() if not k.startswith("sa")}

        send_quiz_completion_email(
            user=request.user,
            quiz=quiz,
            quiz_id=quiz_id,
            score=score,
            total=total,
            answer_key=answer_key,
            submitted_answers=mc_answers,
            is_new_best=is_new_best,
            sa_results=sa_results if sa_results else None,
        )

        send_admin_quiz_notification(
            user=request.user,
            quiz=quiz,
            quiz_id=quiz_id,
            score=score,
            total=total,
            answer_key=answer_key,
            submitted_answers=mc_answers,
            sa_results=sa_results if sa_results else None,
        )

    # Build processed_questions for dynamic template rendering
    processed_questions = []
    for q in db_questions:
        user_answer = submitted_answers.get(q.key, '')
        is_correct = None
        if score is not None:
            is_correct = str(user_answer).upper() == q.correct_answer.upper()
        processed_questions.append({
            'key': q.key,
            'text': q.question_text,
            'choices': q.get_choices(),
            'correct': q.correct_answer,
            'explanation': q.explanation,
            'image_url': q.image_url,
            'section_heading': q.section_heading,
            'user_answer': user_answer,
            'is_correct': is_correct,
        })

    template = quiz.get("template", "logbook/quiz_unavailable.html")

    return render(request, template, {
        "quiz": quiz,
        "quiz_id": quiz_id,
        "answer_key": answer_key,
        "submitted_answers": submitted_answers,
        "score": score,
        "total": total,
        "previous_best": previous_best,
        "is_new_best": is_new_best,
        "short_answer_defs": short_answer_defs,
        "sa_results": sa_results,
        "processed_questions": processed_questions,
    })


def case_step(request, case_id, step_order):
    case = get_object_or_404(ClinicalCase, id=case_id)
    step = get_object_or_404(CaseStep, case=case, order=step_order)

    return render(
        request,
        "logbook/case_step.html",
        {"case": case, "step": step}
    )

def home(request):
    context = {}

    if request.user.is_authenticated:
        # Get user's scans
        user_scans = Scan.objects.filter(user=request.user)

        # Total scans by type
        scans_by_type = (
            user_scans
            .values("exam_type")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Total scan count
        total_scans = user_scans.count()

        # Quiz progress
        user_best_scores = QuizBestScore.objects.filter(user=request.user)
        quizzes_completed = user_best_scores.filter(best_score__gte=F('total') * 0.7).count()
        quiz_percentage = round((quizzes_completed / TOTAL_QUIZZES) * 100) if TOTAL_QUIZZES > 0 else 0

        quiz_progress = {
            "completed": quizzes_completed,
            "total": TOTAL_QUIZZES,
            "percentage": quiz_percentage,
        }

        # Calculate weak areas (exam types with low volume)
        # Define minimum target for each exam type
        exam_targets = {
            "RUQ": 25,
            "LUQ": 25,
            "AORTA": 15,
            "SUBXIPHOID": 25,
            "PLAX": 25,
            "PSAX": 25,
            "IVC": 15,
            "OB_FIRST": 10,
        }

        # Get counts per exam type
        scan_counts = {item["exam_type"]: item["total"] for item in scans_by_type}

        # Find weak areas (less than 50% of target)
        weak_areas = []
        for exam_type, target in exam_targets.items():
            current = scan_counts.get(exam_type, 0)
            if current < target * 0.5:  # Less than 50% of target
                weak_areas.append({
                    "exam_type": exam_type,
                    "current": current,
                    "target": target,
                    "percentage": round((current / target) * 100) if target > 0 else 0,
                })

        # Sort weak areas by percentage (lowest first)
        weak_areas.sort(key=lambda x: x["percentage"])

        # QA feedback pending (placeholder - can be expanded later)
        # For now, count scans without supervisor present as "needs QA"
        qa_pending = user_scans.filter(supervisor_present=False).count()

        context = {
            "quiz_progress": quiz_progress,
            "scans_by_type": scans_by_type,
            "total_scans": total_scans,
            "weak_areas": weak_areas[:4],  # Show top 4 weak areas
            "qa_pending": qa_pending,
            "exam_targets": exam_targets,
            "scan_counts": scan_counts,
        }

    return render(request, "home.html", context)


@login_required
def scan_create(request):
    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.user = request.user
            scan.save()
            return redirect("my_scans")
    else:
        form = ScanForm()

    return render(request, "logbook/scan_form.html", {"form": form})


@login_required
def scan_edit(request, pk):
    scan = get_object_or_404(Scan, pk=pk, user=request.user)

    if request.method == "POST":
        form = ScanForm(request.POST, instance=scan)
        if form.is_valid():
            form.save()
            return redirect("my_scans")
    else:
        form = ScanForm(instance=scan)

    return render(request, "logbook/scan_form.html", {"form": form, "is_edit": True})


@login_required
def scan_delete(request, pk):
    scan = get_object_or_404(Scan, pk=pk, user=request.user)

    if request.method == "POST":
        scan.delete()
        return redirect("my_scans")

    return render(request, "logbook/scan_confirm_delete.html", {"scan": scan})


@login_required
def my_scans(request):
    user_scans = Scan.objects.filter(user=request.user).order_by("-performed_at", "-created_at")

    # Separate scans by context
    academic_scans = user_scans.filter(scan_context="ACADEMIC")
    self_scans = user_scans.filter(scan_context="SELF")

    # Counts by exam type for each context
    academic_counts = (
        academic_scans
        .values("exam_type")
        .annotate(total=Count("id"))
        .order_by("exam_type")
    )

    self_counts = (
        self_scans
        .values("exam_type")
        .annotate(total=Count("id"))
        .order_by("exam_type")
    )

    # Overall counts
    total_counts = (
        user_scans
        .values("exam_type")
        .annotate(total=Count("id"))
        .order_by("exam_type")
    )

    return render(request, "logbook/my_scans.html", {
        "academic_scans": academic_scans,
        "self_scans": self_scans,
        "academic_counts": academic_counts,
        "self_counts": self_counts,
        "total_counts": total_counts,
        "academic_total": academic_scans.count(),
        "self_total": self_scans.count(),
    })

@staff_member_required
def scan_totals(request):
    total_scans = Scan.objects.count()

    totals_by_user = (
        Scan.objects.values("user__username")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    totals_by_exam = (
        Scan.objects.values("exam_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(
        request,
        "logbook/scan_totals.html",
        {
            "total_scans": total_scans,
            "totals_by_user": totals_by_user,
            "totals_by_exam": totals_by_exam,
        },
    )

from .models import ClinicalCase   # add this at the top if not already imported

def cases_list(request):
    cases = ClinicalCase.objects.filter(is_published=True)
    return render(request, "logbook/cases_list.html", {"cases": cases})


def case_step(request, case_id, step_order):
    case = get_object_or_404(ClinicalCase, id=case_id)
    step = get_object_or_404(CaseStep, case=case, order=step_order)
    question = getattr(step, 'question', None)
    feedback = None
    selected = None

    if request.method == "POST" and question:
        selected = request.POST.get("answer")
        if selected:
            try:
                choice = question.choices.get(pk=selected)
                feedback = choice.feedback or ("✅ Correct!" if choice.is_correct else "❌ Incorrect — review the findings and try again.")
                selected = choice
            except question.choices.model.DoesNotExist:
                pass

    total_steps = case.steps.count()
    next_step = step_order + 1 if step_order < total_steps else None
    prev_step = step_order - 1 if step_order > 1 else None

    return render(request, "logbook/case_step.html", {
        "case": case,
        "step": step,
        "question": question,
        "feedback": feedback,
        "selected": selected,
        "next_step": next_step,
        "prev_step": prev_step,
        "total_steps": total_steps,
    })


def pocus_calendar(request):
    return render(request, "logbook/pocus_calendar.html")


def resources(request):
    resources_qs = Resource.objects.filter(is_published=True)
    categories = {}
    for r in resources_qs:
        categories.setdefault(r.get_category_display(), []).append(r)
    return render(request, "logbook/resources.html", {
        "resources": resources_qs,
        "categories": categories,
    })


def protocols(request):
    protocols_qs = POCUSProtocol.objects.filter(is_published=True)
    return render(request, "logbook/protocols.html", {"db_protocols": protocols_qs})


def faculty_evaluation(request):
    return render(request, "logbook/faculty_evaluation.html")


def search(request):
    query = request.GET.get("q", "").strip()
    results = {
        "scans": [],
        "quizzes": [],
        "cases": [],
        "protocols": [],
    }

    if query and request.user.is_authenticated:
        # Search user's scans
        results["scans"] = Scan.objects.filter(
            user=request.user
        ).filter(
            Q(exam_type__icontains=query) |
            Q(indication__icontains=query) |
            Q(notes__icontains=query) |
            Q(finding__icontains=query)
        ).order_by("-performed_at")[:10]

        # Search quizzes
        matching_quizzes = []
        for quiz_id, quiz_data in QUIZZES.items():
            if query.lower() in quiz_data["title"].lower():
                matching_quizzes.append({
                    "id": quiz_id,
                    "title": quiz_data["title"],
                })
        results["quizzes"] = matching_quizzes

        # Search clinical cases
        results["cases"] = ClinicalCase.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        )[:10]

        # Search protocols (static content matching)
        protocol_keywords = {
            "fast": {"name": "FAST Scan", "tab": "fast", "keywords": ["fast", "trauma", "morrison", "hepatorenal", "splenorenal", "pericardial", "hemoperitoneum", "free fluid"]},
            "lung": {"name": "Lung Ultrasound", "tab": "lung", "keywords": ["lung", "pneumothorax", "b-lines", "pleural", "consolidation", "effusion", "sliding", "barcode"]},
            "cardiac": {"name": "Cardiac POCUS", "tab": "cardiac", "keywords": ["cardiac", "heart", "echo", "plax", "psax", "apical", "subxiphoid", "ivc", "pericardial", "tamponade", "lv", "rv"]},
        }

        matching_protocols = []
        for protocol_id, protocol_data in protocol_keywords.items():
            if any(query.lower() in kw for kw in protocol_data["keywords"]) or query.lower() in protocol_data["name"].lower():
                matching_protocols.append({
                    "id": protocol_id,
                    "name": protocol_data["name"],
                    "tab": protocol_data["tab"],
                })
        results["protocols"] = matching_protocols

    total_results = (
        len(results["scans"]) +
        len(results["quizzes"]) +
        len(results["cases"]) +
        len(results["protocols"])
    )

    return render(request, "logbook/search_results.html", {
        "query": query,
        "results": results,
        "total_results": total_results,
    })

from django.utils import timezone
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_scan_bundle(request, bundle):
    # Map bundle slugs to exam types
    scan_types = {
        "ruq": "RUQ",
        "luq": "LUQ",
        "aorta": "AORTA",
        "subxiphoid": "SUBXIPHOID",
        "plax": "PLAX",
        "psax": "PSAX",
        "ivc": "IVC",
        "ob_first": "OB_FIRST",
    }

    exam_type = scan_types.get(bundle)
    if not exam_type:
        return redirect("home")

    # Get scan context (default to SELF if not provided)
    scan_context = request.POST.get("scan_context", "SELF")
    if scan_context not in ["ACADEMIC", "SELF"]:
        scan_context = "SELF"

    today = timezone.localdate()

    Scan.objects.create(
        user=request.user,
        exam_type=exam_type,
        scan_context=scan_context,
        performed_at=today,
        finding="NORMAL",
    )

    return redirect("my_scans")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend to ensure proper session setup
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome to POCUS Portal, {user.username}!")
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "logbook/profile.html", {"form": form})


@login_required
@require_POST
def batch_add_scans(request):
    """Add multiple scans of different types at once."""
    valid_types = ["RUQ", "LUQ", "AORTA", "SUBXIPHOID", "PLAX", "PSAX", "IVC", "OB_FIRST"]
    type_names = {
        "RUQ": "RUQ Abdomen",
        "LUQ": "LUQ Abdomen",
        "AORTA": "Aorta",
        "SUBXIPHOID": "Subxiphoid",
        "PLAX": "PLAX",
        "PSAX": "PSAX",
        "IVC": "IVC",
        "OB_FIRST": "First-Trimester OB",
    }

    # Get scan context (default to SELF if not provided)
    scan_context = request.POST.get("scan_context", "SELF")
    if scan_context not in ["ACADEMIC", "SELF"]:
        scan_context = "SELF"

    today = timezone.localdate()
    scans_to_create = []
    added_summary = []

    # Process each scan type
    for scan_type in valid_types:
        qty_key = f"qty_{scan_type}"
        quantity = request.POST.get(qty_key, 0)

        try:
            quantity = int(quantity)
            if quantity < 0:
                quantity = 0
            elif quantity > 50:
                quantity = 50
        except (ValueError, TypeError):
            quantity = 0

        if quantity > 0:
            for _ in range(quantity):
                scans_to_create.append(
                    Scan(
                        user=request.user,
                        exam_type=scan_type,
                        scan_context=scan_context,
                        performed_at=today,
                        finding="NORMAL",
                    )
                )
            added_summary.append(f"{quantity} {type_names.get(scan_type, scan_type)}")

    if scans_to_create:
        Scan.objects.bulk_create(scans_to_create)
        total_added = len(scans_to_create)
        summary = ", ".join(added_summary)
        messages.success(request, f"Successfully added {total_added} scan(s): {summary}")
    else:
        messages.warning(request, "No scans were added. Please enter at least 1 for any scan type.")

    return redirect("my_scans")


@login_required
def badges(request):
    """Display user's badges and achievements."""
    user_scans = Scan.objects.filter(user=request.user)
    total_scans = user_scans.count()

    # Scan counts by type
    scan_counts = {}
    for scan in user_scans.values("exam_type").annotate(total=Count("id")):
        scan_counts[scan["exam_type"]] = scan["total"]

    # Scan counts by context
    academic_count = user_scans.filter(scan_context="ACADEMIC").count()
    self_count = user_scans.filter(scan_context="SELF").count()

    # Quiz progress
    user_best_scores = QuizBestScore.objects.filter(user=request.user)
    quizzes_passed = user_best_scores.filter(best_score__gte=F('total') * 0.7).count()
    quizzes_attempted = user_best_scores.count()

    # Define badges with criteria
    badges_list = []

    # === SCAN MILESTONE BADGES ===
    scan_milestones = [
        (10, "First Steps", "Complete 10 scans", "fas fa-shoe-prints", "#6366f1"),
        (25, "Getting Started", "Complete 25 scans", "fas fa-seedling", "#22c55e"),
        (50, "Halfway There", "Complete 50 scans", "fas fa-mountain", "#3b82f6"),
        (100, "Century Club", "Complete 100 scans", "fas fa-star", "#f59e0b"),
        (200, "POCUS Pro", "Complete 200 scans", "fas fa-crown", "#ec4899"),
        (500, "Master Scanner", "Complete 500 scans", "fas fa-gem", "#8b5cf6"),
    ]

    for threshold, name, description, icon, color in scan_milestones:
        badges_list.append({
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "earned": total_scans >= threshold,
            "progress": min(100, round((total_scans / threshold) * 100)),
            "current": total_scans,
            "target": threshold,
            "category": "Scan Milestones",
        })

    # === EXAM TYPE MASTERY BADGES ===
    exam_badges = [
        ("RUQ", 25, "RUQ Expert", "Master RUQ examinations", "fas fa-wave-square", "#0d6efd"),
        ("LUQ", 25, "LUQ Expert", "Master LUQ examinations", "fas fa-wave-square", "#0d6efd"),
        ("AORTA", 15, "Aorta Specialist", "Master aorta examinations", "fas fa-circle", "#0ea5e9"),
        ("SUBXIPHOID", 25, "Cardiac View Pro", "Master subxiphoid views", "fas fa-heartbeat", "#dc3545"),
        ("PLAX", 25, "PLAX Master", "Master PLAX cardiac views", "fas fa-heartbeat", "#dc3545"),
        ("PSAX", 25, "PSAX Master", "Master PSAX cardiac views", "fas fa-heartbeat", "#dc3545"),
        ("IVC", 15, "IVC Specialist", "Master IVC examinations", "fas fa-arrows-alt-v", "#f59e0b"),
        ("OB_FIRST", 10, "OB Certified", "Master first-trimester OB", "fas fa-baby", "#22c55e"),
    ]

    for exam_type, threshold, name, description, icon, color in exam_badges:
        current = scan_counts.get(exam_type, 0)
        badges_list.append({
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "earned": current >= threshold,
            "progress": min(100, round((current / threshold) * 100)),
            "current": current,
            "target": threshold,
            "category": "Exam Mastery",
        })

    # === QUIZ BADGES ===
    quiz_badges = [
        (1, "Quiz Starter", "Pass your first quiz", "fas fa-clipboard-check", "#10b981"),
        (2, "Quiz Enthusiast", "Pass 2 quizzes", "fas fa-brain", "#3b82f6"),
        (3, "Quiz Master", "Pass all 3 quizzes", "fas fa-graduation-cap", "#8b5cf6"),
    ]

    for threshold, name, description, icon, color in quiz_badges:
        badges_list.append({
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "earned": quizzes_passed >= threshold,
            "progress": min(100, round((quizzes_passed / threshold) * 100)) if threshold > 0 else 0,
            "current": quizzes_passed,
            "target": threshold,
            "category": "Quizzes",
        })

    # === ACADEMIC HALF DAY BADGES ===
    academic_badges = [
        (5, "Academic Participant", "Log 5 Academic Half Day scans", "fas fa-chalkboard-teacher", "#6366f1"),
        (20, "Academic Achiever", "Log 20 Academic Half Day scans", "fas fa-university", "#8b5cf6"),
        (50, "Academic Excellence", "Log 50 Academic Half Day scans", "fas fa-award", "#a855f7"),
    ]

    for threshold, name, description, icon, color in academic_badges:
        badges_list.append({
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "earned": academic_count >= threshold,
            "progress": min(100, round((academic_count / threshold) * 100)) if threshold > 0 else 0,
            "current": academic_count,
            "target": threshold,
            "category": "Academic Half Day",
        })

    # Calculate summary stats
    earned_badges = [b for b in badges_list if b["earned"]]
    total_badges = len(badges_list)
    earned_count = len(earned_badges)

    # Group badges by category
    categories = {}
    for badge in badges_list:
        cat = badge["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(badge)

    return render(request, "logbook/badges.html", {
        "badges_list": badges_list,
        "categories": categories,
        "earned_count": earned_count,
        "total_badges": total_badges,
        "total_scans": total_scans,
        "quizzes_passed": quizzes_passed,
        "academic_count": academic_count,
        "self_count": self_count,
    })



# ---------------------------------------------------------------------------
# Admin: Quiz Analytics
# ---------------------------------------------------------------------------
@staff_member_required
def quiz_analytics(request):
    """
    Staff-only view showing per-quiz statistics and per-question difficulty,
    helping instructors identify topics that learners find most challenging.
    """
    quiz_stats = []

    for quiz_id, quiz_data in QUIZZES.items():
        attempts_qs = QuizAttempt.objects.filter(quiz_id=quiz_id)
        total_attempts = attempts_qs.count()
        unique_users = attempts_qs.values("user").distinct().count()

        if total_attempts > 0:
            agg = attempts_qs.aggregate(avg_score=Avg("score"))
            avg_score = agg["avg_score"] or 0
            mc_total = len(quiz_data["questions"])
            avg_pct = round((avg_score / mc_total) * 100, 1) if mc_total else 0

            pass_count = sum(1 for a in attempts_qs if a.percentage >= 70)
            pass_rate = round((pass_count / total_attempts) * 100, 1)
        else:
            avg_pct = 0.0
            pass_rate = 0.0

        all_answers = list(attempts_qs.values_list("answers", flat=True))
        answer_key = quiz_data["questions"]
        question_labels = quiz_data.get("question_labels", {})

        question_stats = []
        for q_key, correct_answer in answer_key.items():
            responses = [a.get(q_key) for a in all_answers if a.get(q_key)]
            total_resp = len(responses)
            if total_resp > 0:
                correct_count = sum(1 for r in responses if r == correct_answer)
                pct_correct = round((correct_count / total_resp) * 100, 1)
                wrong_choices = {}
                for r in responses:
                    if r != correct_answer:
                        wrong_choices[r] = wrong_choices.get(r, 0) + 1
                wrong_choices_sorted = sorted(wrong_choices.items(), key=lambda x: -x[1])
            else:
                pct_correct = 0.0
                wrong_choices_sorted = []

            question_stats.append({
                "key": q_key,
                "label": question_labels.get(q_key, q_key),
                "correct_answer": correct_answer,
                "total_responses": total_resp,
                "pct_correct": pct_correct,
                "pct_incorrect": round(100 - pct_correct, 1),
                "wrong_choices": wrong_choices_sorted,
                "is_difficult": pct_correct < 60,
            })

        question_stats.sort(key=lambda x: x["pct_correct"])

        sa_defs = quiz_data.get("short_answers", {})
        sa_responses = []
        for sa_key, sa_def in sa_defs.items():
            responses_for_sa = []
            for attempt in attempts_qs.select_related("user"):
                text = attempt.answers.get(sa_key, "")
                if text:
                    matched_count, total_kw, matched_kws = score_short_answer(
                        text, sa_def["keywords"]
                    )
                    responses_for_sa.append({
                        "username": attempt.user.username,
                        "date": attempt.created_at,
                        "text": text,
                        "matched_keywords": matched_kws,
                        "matched_count": matched_count,
                        "total_keywords": total_kw,
                        "auto_passed": matched_count >= sa_def.get("min_keywords", 1),
                    })
            sa_responses.append({
                "key": sa_key,
                "prompt": sa_def["prompt"],
                "sample_answer": sa_def["sample_answer"],
                "responses": responses_for_sa,
                "total_responses": len(responses_for_sa),
            })

        # Per-user individual attempt records
        sa_defs = quiz_data.get("short_answers", {})
        user_attempts = []
        for attempt in attempts_qs.select_related("user").order_by("-created_at"):
            attempt_sa = {}
            for sa_key, sa_def in sa_defs.items():
                text = attempt.answers.get(sa_key, "")
                if text:
                    matched_count, total_kw, matched_kws = score_short_answer(
                        text, sa_def["keywords"]
                    )
                    attempt_sa[sa_key] = {
                        "prompt": sa_def["prompt"],
                        "text": text,
                        "matched_keywords": matched_kws,
                        "auto_passed": matched_count >= sa_def.get("min_keywords", 1),
                    }
                else:
                    attempt_sa[sa_key] = {
                        "prompt": sa_def["prompt"],
                        "text": "",
                        "matched_keywords": [],
                        "auto_passed": False,
                    }
            user_attempts.append({
                "username": attempt.user.username,
                "email": attempt.user.email,
                "date": attempt.created_at,
                "score": attempt.score,
                "total": attempt.total,
                "percentage": attempt.percentage,
                "passed": attempt.percentage >= 70,
                "sa": attempt_sa,
            })

        quiz_stats.append({
            "quiz_id": quiz_id,
            "title": quiz_data["title"],
            "total_attempts": total_attempts,
            "unique_users": unique_users,
            "avg_pct": avg_pct,
            "pass_rate": pass_rate,
            "question_stats": question_stats,
            "sa_responses": sa_responses,
            "user_attempts": user_attempts,
            "sa_keys": list(sa_defs.keys()),
        })

    return render(request, "logbook/quiz_analytics.html", {
        "quiz_stats": quiz_stats,
    })
