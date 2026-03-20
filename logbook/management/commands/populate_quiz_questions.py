"""
Management command to seed QuizQuestion and QuizShortAnswer from existing hardcoded data.
Run once after migration: python manage.py populate_quiz_questions
"""
from django.core.management.base import BaseCommand
from logbook.models import QuizQuestion, QuizShortAnswer

QUIZ_DATA = {
    1: {
        "questions": [
            {
                "key": "q1", "order": 1,
                "label": "Primary purpose of E-FAST in trauma",
                "section_heading": "",
                "text": "What is the primary purpose of the E-FAST exam in trauma patients?",
                "choice_a": "To identify fractures",
                "choice_b": "To guide operative management of bowel injury",
                "choice_c": "To rapidly detect life-threatening thoracoabdominal bleeding or air",
                "choice_d": "To evaluate cardiac ejection fraction",
                "choice_e": "",
                "correct": "C",
            },
            {
                "key": "q2", "order": 2,
                "label": "Most sensitive E-FAST area for free fluid",
                "section_heading": "",
                "text": "What is the most sensitive area of the E-FAST for free fluid in adults?",
                "choice_a": "Utero-bladder",
                "choice_b": "Subdiaphragmatic space in the LUQ",
                "choice_c": "Hepatorenal interface",
                "choice_d": "Caudal tip of the liver",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q3", "order": 3,
                "label": "Key advantage of US-guided CVC",
                "section_heading": "",
                "text": "What is a key advantage of real-time ultrasound guidance for central venous access?",
                "choice_a": "Eliminates the need for sterile technique",
                "choice_b": "Allows for identification of arterial structures",
                "choice_c": "Increases first-attempt success and reduces complications",
                "choice_d": "Allows for cannulation of deeper vessels",
                "choice_e": "",
                "correct": "C",
            },
            {
                "key": "q4", "order": 4,
                "label": "Risk of short-axis needle advancement",
                "section_heading": "",
                "text": "When visualizing a vessel in short-axis (transverse view), what is a common risk during needle advancement?",
                "choice_a": "Piercing the carotid artery",
                "choice_b": "Losing track of the needle tip due to out-of-plane imaging",
                "choice_c": "Overestimating the diameter of the vein",
                "choice_d": "Damaging the brachial plexus",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q5", "order": 5,
                "label": "True statement about POCUS",
                "section_heading": "",
                "text": "Which of the following statements is true?",
                "choice_a": "POCUS can identify the source of hemorrhage",
                "choice_b": "POCUS cannot assess for solid organ injury",
                "choice_c": "POCUS is poor at identifying pneumothorax",
                "choice_d": "POCUS can differentiate the type of fluid present",
                "choice_e": "",
                "correct": "B",
            },
        ],
        "short_answers": [
            {
                "key": "sa1", "order": 1,
                "prompt": "Briefly describe the E-FAST exam: what does it stand for and which body cavities does it assess?",
                "sample_answer": "E-FAST stands for Extended Focused Assessment with Sonography in Trauma. It assesses the peritoneal cavity (for free fluid/hemoperitoneum), the pericardial space (for tamponade), and bilateral pleural cavities (for pneumothorax and hemothorax).",
                "keywords": "extended, focused, assessment, sonography, trauma, peritoneal, pericardial, pleural, thorax, lung, pneumothorax, hemothorax, free fluid, abdominal",
                "min_keywords": 3,
            },
        ],
    },
    2: {
        "questions": [
            {
                "key": "q1", "order": 1,
                "label": "Ultrasound wave property",
                "section_heading": "Ultrasound Physics Questions",
                "text": "Which of the following describes the relationship between ultrasound frequency and penetration depth?",
                "choice_a": "Higher frequency leads to deeper penetration.",
                "choice_b": "Lower frequency leads to deeper penetration.",
                "choice_c": "Frequency and penetration depth are unrelated.",
                "choice_d": "Frequency only affects image resolution, not penetration.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q2", "order": 2,
                "label": "Probe frequency and penetration",
                "section_heading": "",
                "text": "What is the primary benefit of using a higher frequency transducer in POCUS?",
                "choice_a": "Increased penetration depth for deep structures.",
                "choice_b": "Improved spatial resolution for superficial structures.",
                "choice_c": "Reduced artifact generation.",
                "choice_d": "Wider field of view.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q3", "order": 3,
                "label": "Acoustic shadowing artifact",
                "section_heading": "",
                "text": "Which artifact is characterized by a bright, hyperechoic line with posterior shadowing, often seen with gallstones?",
                "choice_a": "Reverberation artifact.",
                "choice_b": "Acoustic shadowing.",
                "choice_c": "Enhancement artifact.",
                "choice_d": "Comet tail artifact.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q4", "order": 4,
                "label": "Gain setting function",
                "section_heading": "",
                "text": "The gain setting on an ultrasound machine primarily controls:",
                "choice_a": "The depth of penetration.",
                "choice_b": "The overall brightness of the image.",
                "choice_c": "The frequency of the emitted sound waves.",
                "choice_d": "The speed of sound in tissue.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q5", "order": 5,
                "label": "Piezoelectricity principle",
                "section_heading": "",
                "text": "Which of the following best describes the principle of piezoelectricity in ultrasound transducers?",
                "choice_a": "The conversion of electrical energy into light energy.",
                "choice_b": "The emission of sound waves by a vibrating crystal and the conversion of reflected sound waves back into electrical signals.",
                "choice_c": "The amplification of sound waves within the transducer.",
                "choice_d": "The focusing of the ultrasound beam.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q6", "order": 6,
                "label": "B-line characteristics",
                "section_heading": "",
                "text": "What does 'B-mode' imaging primarily represent in ultrasound?",
                "choice_a": "Brightness mode, displaying echoes as dots with varying brightness.",
                "choice_b": "Blood flow mode, used for Doppler imaging.",
                "choice_c": "Bi-directional mode, showing flow in two directions.",
                "choice_d": "Bone mode, optimized for bone visualization.",
                "choice_e": "",
                "correct": "A",
            },
            {
                "key": "q7", "order": 7,
                "label": "Aorta anatomical landmark",
                "section_heading": "Abdominal Aorta Questions",
                "text": "Which anatomical landmark is crucial for identifying the abdominal aorta during a POCUS exam?",
                "choice_a": "The inferior vena cava (IVC) anterior to the aorta.",
                "choice_b": "The gallbladder to the left of the aorta.",
                "choice_c": "The splenic vein posterior to the aorta.",
                "choice_d": "The left kidney anterior to the aorta.",
                "choice_e": "Spine",
                "correct": "A",
            },
            {
                "key": "q8", "order": 8,
                "label": "AAA definition",
                "section_heading": "",
                "text": "When scanning the abdominal aorta, what is the normal range for its diameter in an adult male, which, if exceeded, should raise concern for an aneurysm?",
                "choice_a": "Less than 1.5 cm.",
                "choice_b": "Greater than 3.0 cm.",
                "choice_c": "Between 4.0 and 5.0 cm.",
                "choice_d": "Any diameter with visible calcifications.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q9", "order": 9,
                "label": "Pneumothorax ultrasound finding",
                "section_heading": "Lung Ultrasound Questions",
                "text": "What is the characteristic ultrasound finding in a patient with a pneumothorax?",
                "choice_a": "Presence of 'lung sliding' and B-lines.",
                "choice_b": "Absence of 'lung sliding' and presence of a 'barcode sign' (stratosphere sign) in M-mode.",
                "choice_c": "Increased pleural effusion.",
                "choice_d": "Consolidation with air bronchograms.",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q10", "order": 10,
                "label": "Lung point significance",
                "section_heading": "",
                "text": "Which ultrasound sign helps differentiate a large pneumothorax from other lung pathologies, particularly when lung sliding is absent?",
                "choice_a": "Lung point.",
                "choice_b": "B-lines presence.",
                "choice_c": "Consolidation.",
                "choice_d": "Tissue shred sign.",
                "choice_e": "",
                "correct": "A",
            },
        ],
        "short_answers": [
            {
                "key": "sa1", "order": 1,
                "prompt": "Describe what ultrasound findings would be most concerning for an abdominal aortic aneurysm (AAA) and what measurement threshold is used.",
                "sample_answer": "An AAA is defined as aortic diameter >3 cm (outer wall to outer wall). Concerning POCUS findings include an aorta measuring >=3 cm in transverse or anteroposterior diameter. Free fluid around the aorta suggests rupture and is a surgical emergency.",
                "keywords": "aneurysm, dilation, dilated, widened, enlargement, 3cm, 3 cm, greater than 3, >3, diameter, anteroposterior, AP, outer wall, transverse, rupture, free fluid, hematoma",
                "min_keywords": 2,
            },
        ],
    },
    3: {
        "questions": [
            {
                "key": "q1", "order": 1,
                "label": "Chamber not visible in PLAX",
                "section_heading": "",
                "text": "In a standard parasternal long-axis (PLAX) view, which cardiac chamber is typically not visualized?",
                "choice_a": "Left atrium",
                "choice_b": "Right ventricle",
                "choice_c": "Left ventricle",
                "choice_d": "Right atrium",
                "choice_e": "",
                "correct": "D",
            },
            {
                "key": "q2", "order": 2,
                "label": "Apical 4-chamber probe position",
                "section_heading": "",
                "text": "To obtain a proper apical 4-chamber (A4C) view, the ultrasound beam should be parallel to the interventricular septum, avoiding foreshortening. What is the correct position and orientation for the probe?",
                "choice_a": "Probe at the left sternal border, indicator to patient's right shoulder",
                "choice_b": "Probe at the point of maximal impulse (PMI), indicator to patient's left",
                "choice_c": "Probe at the left sternal border, indicator to patient's left shoulder",
                "choice_d": "Probe at the point of maximal impulse (PMI), indicator to patient's right",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q3", "order": 3,
                "label": "Differentiating pleural vs pericardial space",
                "section_heading": "",
                "text": "Which structure is important to identify to differentiate the pleural from the pericardial spaces?",
                "choice_a": "Left atrium",
                "choice_b": "Inferior vena cava (IVC)",
                "choice_c": "Thoracic aorta",
                "choice_d": "Left ventricle",
                "choice_e": "",
                "correct": "B",
            },
            {
                "key": "q4", "order": 4,
                "label": "Valve visibility in PSAX",
                "section_heading": "",
                "text": "Which valve is not visible in the parasternal short-axis view (PSAX)?",
                "choice_a": "Aortic valve",
                "choice_b": "Tricuspid valve",
                "choice_c": "Pulmonic valve",
                "choice_d": "All valves are potentially visible in the PSAX view",
                "choice_e": "",
                "correct": "D",
            },
            {
                "key": "q5", "order": 5,
                "label": "Fifth chamber on A4C tilt",
                "section_heading": "",
                "text": "From a standard apical 4-chamber view, you gently tilt the probe anteriorly (towards the ceiling) until a fifth chamber comes into view. What is this 'fifth chamber'?",
                "choice_a": "The superior vena cava",
                "choice_b": "The coronary sinus",
                "choice_c": "The aortic valve/LVOT",
                "choice_d": "The pulmonary artery",
                "choice_e": "",
                "correct": "C",
            },
        ],
        "short_answers": [
            {
                "key": "sa1", "order": 1,
                "prompt": "Case A — New Onset Cardiomyopathy (PLAX view): The EPSS measured on this scan is 23.7 mm. What does EPSS measure, and what threshold suggests impaired LV systolic function?",
                "sample_answer": "EPSS measures the distance between the anterior mitral valve leaflet at its E-point (peak early diastolic opening) and the interventricular septum. Normal EPSS is <7 mm. An EPSS >7 mm suggests reduced LV systolic function. An EPSS of 23.7 mm indicates severely reduced EF, consistent with EF <20%.",
                "keywords": "E-point, E point, septal separation, anterior leaflet, mitral, interventricular septum, septum, systolic function, ejection fraction, EF, 7mm, 7 mm, >7, reduced, impaired, dysfunction",
                "min_keywords": 3,
            },
            {
                "key": "sa2", "order": 2,
                "prompt": "Case A — New Onset Cardiomyopathy (PLAX view): Describe the key sonographic features visible on this PLAX image that are consistent with dilated cardiomyopathy with severely reduced ejection fraction.",
                "sample_answer": "PLAX findings of dilated cardiomyopathy with reduced EF include: (1) Markedly dilated LV cavity — globular rather than oval. (2) Global hypokinesis — reduced wall motion throughout. (3) Elevated EPSS (>7 mm) reflecting poor LV contractility and reduced mitral valve opening. In this case the LV is grossly dilated with an EPSS of 23.7 mm, correlating with EF <20%.",
                "keywords": "dilated, enlarged, LV, left ventricle, dilation, hypokinesis, poor contractility, systolic dysfunction, cardiomyopathy, globular, EPSS, mitral valve, reduced, wall motion",
                "min_keywords": 3,
            },
            {
                "key": "sa3", "order": 3,
                "prompt": "Case A — New Onset Cardiomyopathy: This 47-year-old male has dyspnea and bilateral leg swelling. Formal echo confirmed EF <20% with dilation of the LA, RA, and RV. Explain how severely reduced LV function leads to these multi-chamber findings and symptoms. What is the clinical term for this condition?",
                "sample_answer": "Severely reduced LV EF (<20%) causes: (1) Elevated LV filling pressures back up into the LA — LA dilation and pulmonary venous hypertension — pulmonary edema — dyspnea. (2) Chronic pulmonary hypertension increases RV afterload — RV dilation and failure — systemic venous congestion — RA dilation and peripheral leg edema. This cascade is biventricular failure (HFrEF). All four chambers become involved.",
                "keywords": "biventricular, heart failure, HFrEF, congestion, pulmonary edema, pulmonary hypertension, right heart failure, peripheral edema, venous congestion, reduced ejection fraction, LA, RV, right ventricle, dilation, backward failure, left atrium, forward failure",
                "min_keywords": 3,
            },
        ],
    },
}


class Command(BaseCommand):
    help = "Seed QuizQuestion and QuizShortAnswer from existing hardcoded quiz data"

    def handle(self, *args, **options):
        created_q = 0
        updated_q = 0
        created_sa = 0
        updated_sa = 0

        for quiz_id, data in QUIZ_DATA.items():
            for q in data.get("questions", []):
                obj, created = QuizQuestion.objects.update_or_create(
                    quiz_id=quiz_id,
                    key=q["key"],
                    defaults={
                        "order": q["order"],
                        "label": q["label"],
                        "section_heading": q["section_heading"],
                        "question_text": q["text"],
                        "choice_a": q["choice_a"],
                        "choice_b": q["choice_b"],
                        "choice_c": q["choice_c"],
                        "choice_d": q["choice_d"],
                        "choice_e": q.get("choice_e", ""),
                        "correct_answer": q["correct"],
                        "image_url": "",
                        "label": q["label"],
                    },
                )
                if created:
                    created_q += 1
                else:
                    updated_q += 1

            for sa in data.get("short_answers", []):
                obj, created = QuizShortAnswer.objects.update_or_create(
                    quiz_id=quiz_id,
                    key=sa["key"],
                    defaults={
                        "order": sa["order"],
                        "prompt": sa["prompt"],
                        "sample_answer": sa["sample_answer"],
                        "keywords": sa["keywords"],
                        "min_keywords": sa["min_keywords"],
                        "image_url": "",
                    },
                )
                if created:
                    created_sa += 1
                else:
                    updated_sa += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Questions: {created_q} created, {updated_q} updated. "
            f"Short answers: {created_sa} created, {updated_sa} updated."
        ))
