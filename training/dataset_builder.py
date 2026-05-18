"""
Amma Sewana — fine-tuning dataset builder

Generates Alpaca-style JSONL for Unsloth fine-tuning of Gemma 4 E2B.

Sources (read in full):
  - Sri Lanka National Guidelines for Maternal Care Vol I, Ministry of Health 2013
  - NICE NG133 — Hypertension in pregnancy (2019, amended 2023)
  - NICE NG3 — Diabetes in pregnancy (2015, amended 2020)
  - NICE NG201 — Antenatal care (2021)
  - RCOG GTG 52 — Prevention and Management of Postpartum Haemorrhage (2016)
  - RCOG GTG 47 — Blood Transfusion in Obstetrics (covers anaemia + iron)
  - RCOG GTG 57 — Reduced Fetal Movements (2026 update)

Output: dataset.jsonl
Each line: {"instruction": "...", "output": "...", "topic": "...", "lang": "..."}
Languages: en (English), si (Sinhala), ta (Tamil)
"""

import json
from pathlib import Path

SYSTEM_HINT = (
    "You are Amma Sewana, an AI assistant for Sri Lanka Public Health Midwives. "
    "Reply concisely with the risk level (LOW/MEDIUM/HIGH/URGENT), the immediate action, "
    "and the source citation. Reply in the same language as the question."
)

# ============================================================
# SECTION 1: HYPERTENSION / PRE-ECLAMPSIA / ECLAMPSIA (English)
# Source: Sri Lanka MOH 2013 §H, §I + RCOG GTG 10a
# ============================================================

HYPERTENSION_EN = [
    # --- Definitions & screening ---
    (
        "What blood pressure values define gestational hypertension in pregnancy?",
        "Gestational hypertension = BP >= 140/90 mmHg developing after 20 weeks, without proteinuria, resolving within 42 days postpartum. Source: Sri Lanka MOH 2013 §H.2."
    ),
    (
        "How do you diagnose pre-eclampsia?",
        "Pre-eclampsia = gestational hypertension (BP >= 140/90 after 20 weeks) PLUS significant proteinuria (>= 300mg/24hr, or dipstick 2+, or protein:creatinine ratio >= 30mg/mmol). Source: MOH 2013 §H.2 / NICE NG133."
    ),
    (
        "What BP values define severe hypertension in pregnancy?",
        "Severe hypertension = systolic >= 160 mmHg AND/OR diastolic >= 110 mmHg. This level requires urgent treatment to prevent maternal cerebral haemorrhage. Source: MOH 2013 §H.2."
    ),
    (
        "What are the features of severe pre-eclampsia beyond high BP and proteinuria?",
        "Severe pre-eclampsia features: severe headache, visual disturbance (blurring/flashing/scotomas), epigastric or RUQ pain, nausea/vomiting, clonus >= 3 beats, papilloedema, liver tenderness, oliguria (<400ml/day or <0.5ml/kg/hr over 4hr), platelets <100,000/L, AST/ALT >70 IU/L, HELLP syndrome. Source: MOH 2013 §H.2."
    ),
    (
        "How often should blood pressure be checked in antenatal visits?",
        "BP must be measured at every antenatal clinic visit by a medical officer, results recorded and plotted in the pregnancy record. Proteinuria must be tested at every visit too. Refer for specialist care if BP > 140/90 on two occasions at least 2 hours apart. Source: MOH 2013 §H.3."
    ),
    # --- Risk stratification / prevention ---
    (
        "Which pregnant women should start aspirin 75mg for pre-eclampsia prevention?",
        "Start aspirin 75mg daily from 12 weeks until delivery if ANY ONE high-risk factor: previous hypertensive pregnancy, chronic kidney disease, autoimmune disease (SLE/APS), type 1 or 2 diabetes, chronic hypertension, multiple pregnancy. OR if TWO+ moderate-risk: first pregnancy, age >= 40, pregnancy interval > 10 years, BMI >= 35 at first visit, family history of pre-eclampsia. Source: MOH 2013 §H.4 / NICE NG133."
    ),
    (
        "What is the recommended calcium supplementation for pre-eclampsia prevention in Sri Lanka?",
        "Women with risk factors should aim for daily calcium intake >= 1000mg. Given typical Sri Lankan dietary intake, the recommended supplementation is 600mg/day. Source: MOH 2013 §H.4."
    ),
    # --- Clinical scenarios ---
    (
        "32-year-old G3P2, 34 weeks, BP 162/108, proteinuria 2+, severe headache. What is the immediate action?",
        "URGENT — this is severe pre-eclampsia with imminent eclampsia signs (severe headache + severe BP). Actions: (1) Establish IV access. (2) MgSO4 4g IV loading dose over 10 min, then 1g/hr infusion to prevent eclampsia. (3) Labetalol 20mg IV over 2 min (or oral nifedipine 10mg if no IV access) — target BP < 160/110. (4) Urgent referral to specialist obstetric unit. (5) Monitor reflexes, RR, urine output. Source: MOH 2013 §H.6.2.1, §6.2.2."
    ),
    (
        "Pregnant woman at 28 weeks with BP 145/92, no proteinuria, no symptoms. What do I do?",
        "MEDIUM — gestational hypertension. Action: (1) Recheck BP after rest in left-lateral position. (2) Dipstick urine for protein. (3) If confirmed BP 140-159/90-109 without proteinuria and asymptomatic, refer to specialist clinic for shared care. (4) Schedule weekly BP and urine checks. (5) Teach mother the danger signs (severe headache, visual disturbance, epigastric pain, reduced fetal movement). Source: MOH 2013 §H.3, §5."
    ),
    (
        "Pregnant woman with BP 178/115, no other symptoms. Specialist hospital is 2 hours away. What do I do before transfer?",
        "URGENT — severe hypertension. Pre-transfer actions: (1) IV access. (2) Oral nifedipine 10mg (repeat every 20 min, max 40mg) to bring BP < 160/110. (3) MgSO4 4g IV (or IM 5g each buttock) loading dose to prevent eclampsia during transit. (4) Insert Foley catheter and monitor urine output. (5) Call receiving hospital and brief them. (6) Send accompanied by a staff member with emergency drugs. Source: MOH 2013 §H.6.2.4."
    ),
    # --- Drug doses ---
    (
        "What is the dose of labetalol for severe hypertension in pregnancy?",
        "Labetalol options: (a) Oral 200mg stat, repeat hourly up to 4 hours (only if BP < 180/110). (b) IV 20mg over 2 min — recheck BP at 10 min; if still high give 40mg IV; max single doses 20, 40, 80 mg. (c) IV infusion 40mg/hr, double every 30 min up to max 160 mg/hr. AVOID in asthma. Source: MOH 2013 §H.6.2.1.1."
    ),
    (
        "How do I give IV hydralazine for severe hypertension in pregnancy?",
        "Hydralazine 5-10mg IV bolus over 2 min, accompanied by a fluid bolus of 5ml/kg of 0.9% NaCl or Ringer lactate over 30 min started at the same time (prevents drastic hypotension). Recheck BP at 15 min. Repeat 5-10mg IV every 15 min up to max 20mg total. If no lasting effect, infusion 2 mg/hr increasing by 0.5 mg/hr (range 2-20 mg/hr). DO NOT give the fluid bolus if pulmonary oedema present. Source: MOH 2013 §H.6.2.1.2."
    ),
    (
        "Oral nifedipine for hypertension in pregnancy — dose?",
        "Oral nifedipine 10mg stat (use only if BP < 180/110 and patient asymptomatic). Repeat at 20-min intervals up to max 40mg total. If no response, escalate to IV labetalol or hydralazine. Source: MOH 2013 §H.6.2.1.3."
    ),
    # --- MgSO4 protocol ---
    (
        "What is the Pritchard regimen for magnesium sulphate in eclampsia?",
        "Loading dose: 4g IV over 10 min (diluted to 20ml with 0.9% NaCl) PLUS 5g IM into each buttock with 1ml of 2% lignocaine in the same syringe (total 14g). Maintenance: 5g IM every 4 hours, alternating buttocks, with lignocaine. Continue for 24 hours after delivery or last fit, whichever is later. Source: MOH 2013 §H.6.2.2."
    ),
    (
        "What is the Zuspan regimen for magnesium sulphate?",
        "Loading dose: 4g IV over 10 min, diluted to 20ml with 0.9% NaCl (via pump) or 80ml via burette. Maintenance: 1g/hr IV infusion. Continue for 24 hours after delivery or last fit. Source: MOH 2013 §H.6.2.2."
    ),
    (
        "What monitoring is required for a woman receiving magnesium sulphate?",
        "Monitor and record every 30 min: (1) Hourly urine output (target >= 30 ml/hr). (2) Respiratory rate (target > 16/min). (3) Oxygen saturation (target > 90%). (4) Presence of patellar reflexes. Stop MgSO4 if RR < 12, absent reflexes, or oliguria. Source: MOH 2013 §H.6.2.2."
    ),
    (
        "Signs of magnesium sulphate toxicity and the antidote?",
        "Toxicity signs: respiratory depression (RR < 12), loss of patellar reflexes, oliguria, drowsiness. Antidote: calcium gluconate 1g IV (10ml of 10% solution) over 10 min. STOP MgSO4 infusion immediately. Source: MOH 2013 §H.6.2.2."
    ),
    # --- Eclampsia ---
    (
        "A woman has just had a generalized seizure at 33 weeks with BP 168/112. Immediate action?",
        "URGENT — eclampsia. During seizure: (1) Turn to LEFT lateral position. (2) Clear airway, suction secretions, O2 by face mask 8-10 L/min. (3) Protect from injury. After seizure: (4) IV access — bloods for FBC, LFT, U&E, coagulation, cross-match. (5) MgSO4 4g IV bolus over 10 min, then 1g/hr infusion. (6) Control BP < 160/110 with labetalol/hydralazine. (7) Insert Foley catheter, restrict fluids to 80 ml/hr. (8) Plan delivery once stable. Source: MOH 2013 §I.6."
    ),
    (
        "What do I do if a woman has a second seizure while on magnesium sulphate?",
        "About 10% of women on MgSO4 will have a second seizure. Give additional MgSO4 2g IV (diluted to 10ml with NaCl, over 5 min) AND increase the infusion to 2g/hr. Monitor closely. If further seizures, call neurology/medical team, consider second-line anticonvulsants in ICU. Source: MOH 2013 §I.6.4."
    ),
    (
        "Total fluid intake limit for a woman with severe pre-eclampsia or eclampsia?",
        "Restrict total fluids to 80 ml/hr to prevent pulmonary oedema. Accurate fluid balance is essential. Use infusion pumps. Account for all drug volumes. Avoid NSAIDs until fluid status recovers. Source: MOH 2013 §H.6.2.3."
    ),
    (
        "Is eclampsia an indication for caesarean section?",
        "NO — eclampsia itself is not an indication for CS. Decision depends on cervix and fetal/maternal condition. If cervix is unfavourable (Bishop < 7) and the woman is not in labour, CS may be appropriate. If in labour or favourable cervix, vaginal delivery is preferred. Stabilise the mother first; never deliver an unstable mother for fetal reasons. Source: MOH 2013 §I.7."
    ),
    (
        "Is ergometrine safe to give for the third stage of labour in severe pre-eclampsia?",
        "NO. Ergometrine is contraindicated in severe pre-eclampsia/eclampsia — it causes acute rises in BP that can precipitate stroke. Use oxytocin 10 IU IM (or 5 IU IV) instead for active management of the third stage. Source: MOH 2013 §H.6.2.5."
    ),
    # --- HELLP & complications ---
    (
        "What is HELLP syndrome and how is it diagnosed?",
        "HELLP = Haemolysis, Elevated Liver enzymes, Low Platelets — a severe pre-eclampsia variant. Diagnosis: AST or ALT > 70 IU/L AND platelets < 100,000/L AND evidence of haemolysis (raised LDH, low haptoglobin, schistocytes on blood film). Action: treat as severe pre-eclampsia, plan delivery once stable. Source: MOH 2013 §H.2."
    ),
    # --- Postpartum follow-up ---
    (
        "When should magnesium sulphate be discontinued postpartum?",
        "Continue MgSO4 for at least 24 hours AFTER delivery, or 24 hours after the last seizure — whichever is later. Source: MOH 2013 §H.6.2.6."
    ),
    (
        "A woman had severe pre-eclampsia in this pregnancy. What is her risk in a future pregnancy?",
        "Counselling: risk of gestational hypertension ~53% (1 in 2); risk of pre-eclampsia ~16% (1 in 6). If she had severe hypertension/HELLP/eclampsia OR delivered before 34 weeks, recurrence risk of pre-eclampsia is ~25%; if delivered before 28 weeks, ~55%. Source: MOH 2013 §H.6.2.7."
    ),
    (
        "Which antihypertensive should be avoided postpartum?",
        "Methyldopa — its tendency to cause depression makes it best avoided postpartum. Switch to another agent (e.g. labetalol, nifedipine) on discharge. Source: MOH 2013 §H.6.2.6."
    ),
    # --- Subtle / scenario ---
    (
        "Mother on antihypertensive medication is planning pregnancy. Which drugs must I stop?",
        "Stop ACE inhibitors (e.g. enalapril, captopril), ARBs (e.g. losartan), and statins BEFORE conception — they are teratogenic. Switch to labetalol, methyldopa, or nifedipine. Source: MOH 2013 §H.5 / RCOG."
    ),
    (
        "What is the upper limit of normal BP at 12 weeks gestation if she has a history of chronic hypertension?",
        "In chronic hypertension, target BP during pregnancy is around 130-140/90-100. The same severe-hypertension threshold applies: treat aggressively if BP >= 160/110 or symptoms. Anticipate superimposed pre-eclampsia. Source: MOH 2013 §H.5."
    ),
]

# ============================================================
# SECTION 2: PPH (English)
# Source: MOH 2013 §K + RCOG GTG 52
# ============================================================

PPH_EN = [
    (
        "What is the definition of primary postpartum haemorrhage?",
        "Primary PPH = blood loss >= 500 ml from the genital tract within 24 hours of birth. Major PPH = blood loss >= 1000 ml. Regardless of volume, any cardiovascular instability (tachycardia + hypotension) signifies major obstetric haemorrhage. Source: MOH 2013 §K.2."
    ),
    (
        "How do I estimate blood volume in a 60 kg pregnant woman?",
        "Blood volume = body weight (kg) / 12. So 60 kg / 12 = 5 litres. Loss of >= 40% of blood volume (~2400 ml in a 60 kg woman) is a massive obstetric haemorrhage. Source: MOH 2013 §K.2."
    ),
    (
        "List the risk factors for PPH that I should look for during antenatal care.",
        "PPH risk factors: grand multiparity, previous PPH, fibroids, anaemia, pre-existing bleeding disorders, anticoagulant use, obesity, pre-eclampsia/gestational hypertension, uterine over-distension (twins, polyhydramnios), large baby (>4 kg), chorioamnionitis, dengue infection. Women with risk factors should deliver in a specialist obstetric unit with IV access secured (14-16 G) and blood group known. Source: MOH 2013 §K.4."
    ),
    (
        "What are the steps of active management of the third stage of labour?",
        "Active management of third stage: (1) Oxytocin 5 IU IV slowly OR 10 IU IM right after delivery of the baby. (2) Delayed cord clamping for 2 min (unless baby compromised, Rh-iso, or maternal bleeding). (3) Controlled cord traction with counter-traction above symphysis pubis. (4) Uterine massage after delivery of placenta. Source: MOH 2013 §A.3.2.3."
    ),
    (
        "After delivery, the uterus feels soft and there is continuing fresh bleeding. What is the first step?",
        "Atonic PPH. Steps in order: (1) Call for help. (2) Rub up the fundus (uterine massage). (3) Clear cervix and vagina of clots by VE. (4) Ergometrine 0.5mg slow IV (or methylergometrine 0.2mg) OR oxytocin 5 IU IV + start infusion 40 IU in 500 ml Hartmann at 125 ml/hr. (5) Bimanual compression. (6) If still bleeding after 10 min, repeat ergometrine. (7) Misoprostol 800 micrograms PR or SL. (8) Tranexamic acid 1g IV over 10 min (repeat at 30 min if needed). (9) Balloon tamponade. (10) Inform Consultant. Source: MOH 2013 §K.5.2.2."
    ),
    (
        "How do I do a uterine balloon tamponade with a Foley catheter and condom?",
        "Condom catheter tamponade: (1) Size 22 Foley catheter, sterile condom, No. 0/1 suture, warm saline. (2) Tie the condom firmly over the catheter 2 cm from the open end. (3) Test with saline to confirm watertight. (4) Insert the catheter through the cervix into the uterus. (5) Fill with 400-500 ml warm saline by gravity until bleeding stops or the balloon bulges out of the cervix. (6) Pack the vagina with moist ribbon gauze around the catheter. (7) Insert Foley catheter into bladder. (8) Give tranexamic acid 1g IV + antibiotic prophylaxis. (9) Keep for 12-18 hours. (10) Deflate half the volume, observe 30 min, then deflate fully and remove. Source: MOH 2013 §K Appendix 1."
    ),
    (
        "When is hysterectomy indicated in PPH?",
        "Hysterectomy is indicated when all conservative measures fail — uterine atony unresponsive to drugs + balloon tamponade + brace sutures + uterine devascularisation. KEY MESSAGE: too little, too late kills women. Do not delay hysterectomy once it is clear the uterus cannot be salvaged. Source: MOH 2013 §K.5.2.2."
    ),
    (
        "Is misoprostol licensed for PPH in Sri Lanka?",
        "Misoprostol is not formally licensed in Sri Lanka for induction or PPH at the time of the MOH 2013 guideline, but it is recommended for use in PPH (800 mcg PR or SL) when ergometrine and oxytocin have failed — its effectiveness in this setting is well-established. Source: MOH 2013 §K.5.2.2."
    ),
    (
        "Tranexamic acid dose for PPH?",
        "Tranexamic acid 1g IV slowly over 10 min. May be repeated after 30 min if bleeding continues. WOMAN trial evidence: most effective if given within 3 hours of bleeding onset. Source: MOH 2013 §K.5.2.2 / WOMAN trial."
    ),
    (
        "I see continuing fresh bleeding but the uterus is well contracted. What do I do?",
        "Suspect traumatic PPH — genital tract trauma. Action: (1) Place in lithotomy under good light and analgesia. (2) Inspect upper vagina and cervix systematically with Green-Armytage forceps. (3) Examine for paravaginal and broad ligament haematoma by combined PV and PR exam. (4) Repair tears starting above the apex. (5) For haematoma > 5 cm, surgical evacuation. (6) If multiple oozing tears, consider balloon catheter in vagina or moistened vaginal pack. Source: MOH 2013 §K.5.2.3."
    ),
    (
        "A woman delivered 30 min ago, BP 80/50, pulse 130, pale, sweaty, fundus high above umbilicus. Diagnosis?",
        "URGENT — concealed PPH (probably uterine atony with clot retention) OR uterine rupture. Action: (1) Two large-bore IVs (14-16 G). (2) Cross-match 4 units, full bloods + coagulation. (3) Fluid resuscitation — warm crystalloid up to 2L + colloid up to 1-2L until blood arrives. (4) Rub up fundus, clear clots from cervix. (5) Oxytocin infusion + ergometrine + tranexamic acid. (6) Call Consultant immediately — laparotomy may be needed if rupture. Keep her flat and warm. Source: MOH 2013 §K.5.2.4."
    ),
    (
        "Should I give Hartmann's solution or normal saline for PPH resuscitation?",
        "Either is acceptable. MOH recommends warmed crystalloid up to 2 litres + colloid up to 1-2 litres (max 3.5 L combined) until blood is available. Hartmann's (Ringer lactate) is often preferred over normal saline to avoid hyperchloraemic acidosis. Keep fluids warm — hypothermia worsens coagulopathy. Source: MOH 2013 §K.6."
    ),
    (
        "How do I prevent hypothermia during a PPH?",
        "Pay attention to temperature of labour/theatre room, IV fluids, blood products, and lavage fluids — all should be warmed. Cover the woman with warm blankets. Hypothermia promotes coagulopathy and worsens outcome. Source: MOH 2013 §K.5.1."
    ),
    (
        "What is delayed third stage of labour and how do I manage it?",
        "Delayed third stage = placenta not delivered within 30 min of active management. Action: (1) Intraumbilical vein oxytocin 50 IU in 30 ml of 0.9% NaCl. (2) Wait 30 min, attempt controlled cord traction again. (3) If still not delivered, proceed to manual removal of placenta under anaesthesia. Source: MOH 2013 §A.3.2.3.2."
    ),
    (
        "When should blood transfusion start in PPH?",
        "Transfuse warm blood as soon as available for blood loss > 1000 ml or earlier if cardiovascular instability. Until blood is available, give warm crystalloid up to 2L + colloid up to 1-2L. Group-specific blood is acceptable until cross-matched is ready. If neither, give O Rhesus D negative. For >= 3 units of blood, transfuse fresh frozen plasma in equal amount. Source: MOH 2013 §K.6."
    ),
    (
        "What is a B-Lynch suture and when is it indicated?",
        "B-Lynch (brace) suture is a uterine compression suture for atonic PPH unresponsive to medical management. A No. 2 absorbable suture is passed antero-posteriorly through the uterus on each side, tied over the fundus while an assistant compresses the uterus manually. May be combined with a balloon tamponade ('sandwich technique'). Source: MOH 2013 §K Appendix 2."
    ),
    (
        "What is acute uterine inversion and how do I recognize it?",
        "Acute puerperal inversion = the uterine fundus turns inside out into the cavity, usually due to cord traction on a relaxed uterus. RED FLAGS: shock out of proportion to visible blood loss, sudden severe lower abdominal pain in 3rd stage, fundus absent or 'cupped' on abdominal palpation, vaginal mass visible/palpable. PV exam shows mass with cervical ring around its base. Source: MOH 2013 §G.6."
    ),
    (
        "Immediate management of acute uterine inversion?",
        "URGENT — life-threatening. (1) Call for help, treat shock aggressively (note neurogenic component). (2) Do NOT remove the placenta if still attached. (3) Reposition uterus IMMEDIATELY (sooner is easier) — Johnson manoeuvre: hand inside vagina, lift fundus above umbilicus to dilate the cervical ring. (4) Hold in place after reduction; give oxytocin 5-10 IU IV + infusion. (5) If unable in labour room, GA and theatre. (6) Hydrostatic O'Sullivan reduction with warm saline if manual fails. Source: MOH 2013 §G.7."
    ),
]

# ============================================================
# SECTION 3: DIABETES IN PREGNANCY (English)
# Source: MOH 2013 §J + NICE NG3
# ============================================================

DIABETES_EN = [
    (
        "When should pregnant women be screened for diabetes in Sri Lanka?",
        "Universal screening of ALL Sri Lankan pregnant women is recommended at the first visit (ideally < 12 weeks) and again at 24-28 weeks if first test negative. Sri Lankans are at high risk (South Asian + pregnant). Already-known diabetics are not re-screened — start glycaemic control immediately. Source: MOH 2013 §J.2.1."
    ),
    (
        "What is the DIPSI test and how do I do it?",
        "DIPSI = Diabetes in Pregnancy Study Group of India test — a non-fasting 75g OGCT. Give 75g glucose dissolved in 300ml water (with lime juice for taste) regardless of fasting status, over 3-5 min. Measure plasma glucose at 2 hours. A 2-hr value > 140 mg/dl (7.8 mmol/L) confirms GDM. Advantage: no fasting required, single sample, universal applicability. Source: MOH 2013 §J.2.2."
    ),
    (
        "What is the diagnostic threshold for pre-existing diabetes in pregnancy?",
        "Pre-existing diabetes if ANY one of: FBS >= 126 mg/dl (7.0 mmol/L), random BG > 200 mg/dl (11.1 mmol/L), or HbA1c > 6.1%. Source: MOH 2013 §J.2.1."
    ),
    (
        "Which tests should NOT be used to screen for GDM?",
        "Do NOT use: fasting blood glucose, random blood glucose, 50g glucose challenge test, HbA1c, or urinalysis for reducing substances — these are NOT validated for GDM screening in pregnancy. Source: MOH 2013 §J.2.1."
    ),
    (
        "Target blood glucose values for pregnant women with diabetes?",
        "Targets (venous plasma): fasting/pre-meal 70-90 mg/dl (3.9-5.0 mmol/L); 2-hr post-meal < 120 mg/dl (6.7 mmol/L). Capillary equivalents: fasting 80-103 mg/dl, post-meal < 118 mg/dl. Aim for these without causing hypoglycaemia. Source: MOH 2013 §J.4.1."
    ),
    (
        "Pre-pregnancy HbA1c target for known diabetic women planning pregnancy?",
        "Target HbA1c < 6.1% before conception. Women with HbA1c > 10% should be strongly advised against conception until control improves — risk of congenital malformations rises sharply. Source: MOH 2013 §J.3.1."
    ),
    (
        "Folic acid dose for women with diabetes planning pregnancy?",
        "5mg folic acid daily when trying to conceive, continuing until 12 weeks gestation. After 12 weeks, reduce to 1mg daily. Higher dose is to reduce neural tube defect risk, which is elevated in diabetes. Source: MOH 2013 §J.3.1, §J.3.2."
    ),
    (
        "Which diabetes drugs are safe in pregnancy?",
        "Safe in pregnancy: insulin (all preparations), metformin. STOP before/during pregnancy: ACE inhibitors, ARBs, statins (teratogenic). Other oral hypoglycaemics — not used; switch to insulin or metformin. Source: MOH 2013 §J.3.1, §J.4.1."
    ),
    (
        "Insulin regimen for a newly-diagnosed GDM woman not controlled on diet?",
        "Two main options: (1) Three pre-meal short-acting + bedtime basal insulin (best control for moderate-severe hyperglycaemia). (2) Twice-daily pre-mixed 30:70 insulin (high compliance, adequate for most cases). If twice-daily insufficient, add metformin or a soluble insulin to cover lunch. Source: MOH 2013 §J.4.1."
    ),
    (
        "How should I monitor fetal growth in a diabetic pregnancy?",
        "Ultrasound abdominal circumference (AC) at 28, 32, 36 weeks. If AC > 90th centile at any stage, intensify insulin to target 2-hr PPBS < 100 mg/dl (avoiding hypoglycaemia). If AC < 10th centile or crossing centiles down, do amniotic fluid index and refer for obstetric review. Source: MOH 2013 §J.4.2."
    ),
    (
        "Why is HbA1c unreliable in late pregnancy?",
        "HbA1c is NOT reliable in the second and third trimesters because of increased red cell turnover and the dilutional effect of pregnancy. Rely on self-monitored blood glucose (SMBG) or regular 6-point profiles instead. Source: MOH 2013 §J.4.2."
    ),
    (
        "When should a woman with diabetes deliver?",
        "Pre-existing diabetes or insulin-treated GDM: schedule delivery at 38-39 weeks (obstetrician review at 36-37 weeks). Diet-controlled GDM with optimal glycaemia and normally-grown baby: insufficient evidence for a specific timing — individualize. Diabetes alone is NOT an indication for caesarean section. Source: MOH 2013 §J.5.1."
    ),
    (
        "Blood glucose target during labour in a diabetic woman?",
        "Maintain capillary blood glucose between 4 and 7 mmol/L (72-126 mg/dl) during labour. Check 1-2 hourly. Record on the partogram. Start Hartmann's/saline if low; insulin-dextrose-potassium (GIK) infusion if high. Source: MOH 2013 §J.5.2."
    ),
    (
        "Newborn of a diabetic mother — when do I check blood sugar?",
        "Check newborn capillary blood glucose 2-4 hours after birth. Action threshold: < 36 mg/dl (2 mmol/L). Initiate breastfeeding within 30-60 min to prevent hypoglycaemia. Watch for polycythaemia, hyperbilirubinaemia, hypocalcaemia, hypomagnesaemia in clinical signs. Source: MOH 2013 §J.6.1.a."
    ),
    (
        "When should a woman who had GDM be re-tested for diabetes after delivery?",
        "At 6-8 weeks postpartum, repeat 75g OGTT (ideal) or fasting BG. If negative, lifestyle advice + annual FBS thereafter. Encourage breastfeeding (contributes to weight loss and reduces type 2 DM risk). Aim for normal BMI. Source: MOH 2013 §J.6.3."
    ),
    (
        "Which contraceptive should be avoided in a postnatal woman with BMI > 25 and GDM?",
        "Avoid DMPA (Depot Medroxy Progesterone Acetate) — associated with weight gain in women already overweight. All other reliable methods (COCP, POP, IUD, condoms) are acceptable based on individual needs. Women with type 2 DM should be advised to complete their family within 5-10 years of diagnosis. Source: MOH 2013 §J.7."
    ),
]

# ============================================================
# SECTION 4: LABOUR MANAGEMENT (English)
# Source: MOH 2013 §A, §B, §C, §D, §E
# ============================================================

LABOUR_EN = [
    (
        "How do I diagnose labour?",
        "Labour = regular, painful intermittent contractions of increasing frequency, duration, and intensity, leading to progressive cervical effacement and dilatation. For practical purposes, also diagnose labour with painful contractions occurring at >= 2 in 10 minutes. If uncertain, observe and reassess in 4 hours. Source: MOH 2013 §A.2."
    ),
    (
        "What is the latent phase of labour?",
        "Latent phase = from commencement of labour to cervical dilatation of 4 cm. There are painful contractions and some cervical changes including effacement and dilatation up to 4 cm. This phase is best managed in the antenatal ward, not the labour room. Source: MOH 2013 §A.2, §A.3.2.1.1."
    ),
    (
        "When is the latent phase considered prolonged?",
        "Latent phase is prolonged when it lasts > 12 hours in a primigravida OR > 8 hours in a multigravida. In these cases, an experienced medical officer must reassess with a view to augmentation. Source: MOH 2013 §A.3.2.1.1."
    ),
    (
        "What defines delayed progress in the active phase of first stage?",
        "Delayed progress = cervical dilatation of < 2 cm in 4 hours, OR slowing of progress in a woman previously progressing satisfactorily. This MUST be assessed by an experienced medical officer. Consider: uterine contractions, descent and position of fetal head, signs of obstruction (caput, moulding), and fetal condition. Source: MOH 2013 §A.3.2.1.3."
    ),
    (
        "Time limit for the active second stage of labour?",
        "Primigravida: birth expected within 2 hours of start of active second stage; diagnose delay at 1 hour and seek advice from a trained operator. Multigravida: birth expected within 1 hour; diagnose delay at 30 min. Add 1 hour to each if epidural in situ. Delay in a multipara raises strong suspicion of disproportion or malposition. Source: MOH 2013 §A.3.2.2.2."
    ),
    (
        "When should I do continuous electronic fetal monitoring rather than intermittent auscultation?",
        "Continuous EFM (CTG) is indicated for: significant meconium staining of amniotic fluid; abnormal FHR by intermittent auscultation (< 110 or > 160 bpm, decelerations after contractions); fresh vaginal bleeding; maternal pyrexia; oxytocin use for augmentation/induction; scarred uterus; epidural analgesia; growth-restricted baby. Source: MOH 2013 §A.3.2.1.2, §D."
    ),
    (
        "What is a normal FHR baseline in a term fetus?",
        "Normal FHR baseline: 110-160 bpm. Auscultate immediately after a contraction for at least 1 full minute. Always palpate the maternal pulse to differentiate from fetal heart rate. Source: MOH 2013 §D."
    ),
    (
        "Classify a CTG with baseline 165 bpm, variability 8 bpm, no decelerations, accelerations present.",
        "REASSURING in 3/4 features; baseline 161-180 is non-reassuring. Overall classification: SUSPICIOUS (one non-reassuring feature). Action: continue EFM, review by experienced medical officer, look for reversible causes (maternal fever, dehydration, recent drugs). If features evolve or persist > 90 min, escalate. Source: MOH 2013 §D Table 1, Table 2."
    ),
    (
        "Define pathological CTG.",
        "Pathological CTG = two or more non-reassuring features OR one or more abnormal features. Abnormal features: baseline < 100 or > 180, sinusoidal pattern >= 10 min, variability < 5 for 90 min, atypical variable decelerations affecting > 50% of contractions for > 30 min, or late decelerations for > 30 min. Action: urgent obstetric review, prepare for delivery. Source: MOH 2013 §D Table 1, Table 2."
    ),
    (
        "What is the partogram alert line and action line?",
        "Alert line: drawn at 1 cm per hour starting from 4 cm dilatation. Action line: parallel to the alert line, 4 hours to the right. Crossing the alert line prompts reassessment; crossing the action line mandates active intervention (augmentation, surgical decision). Source: MOH 2013 §F (partogram)."
    ),
    (
        "When is amniotomy contraindicated?",
        "Amniotomy is contraindicated when the head is high and poorly applied to the cervix (cord prolapse risk), and in cases of suspected vasa praevia or placenta praevia. Only do amniotomy when committed to delivery within 24 hours, when the cervix is ripe, and after assessment by an experienced clinician. Source: MOH 2013 §B.6.2."
    ),
    (
        "Indications for induction of labour at 41 weeks in a low-risk pregnancy?",
        "Induction is recommended for low-risk women with confirmed gestation at 41 weeks. Around 40 weeks, assess fetal wellbeing (biometry — at least AC — and amniotic fluid index; lower cut-off AFI 7 cm) to select those for conservative management until 41 weeks. Source: MOH 2013 §B.4.1."
    ),
    (
        "How do I induce labour with intrauterine death?",
        "Intrauterine death is a traumatic event — most women want delivery soon and their wishes should be respected. Prostaglandins are preferred. Amniotomy and repeated VEs should be AVOIDED to reduce infection risk. (Misoprostol is highly effective in mid-trimester IUD; mifepristone helps but neither is currently licensed in Sri Lanka.) Amniotomy preferred only with abruption placentae. Source: MOH 2013 §B.4.4."
    ),
    (
        "What is the recommended oxytocin starting infusion rate?",
        "Standard mix: 5 IU oxytocin in 500 ml of 0.9% NaCl. Start at 15 drops/min (~7.5 mU/min), increase by 15 drops/min every 30 min, max 60 drops/min (~30 mU/min). Aim for a contraction-free interval of 2 minutes. Use an infusion pump where available. Source: MOH 2013 §C."
    ),
    (
        "Definition of uterine hyperstimulation?",
        "Hyperstimulation = contraction-free interval < 60 seconds OR contractions lasting > 90 seconds. Action: STOP oxytocin (or remove PGE2 tablet from vagina) immediately, rapid 0.9% NaCl bolus via fresh giving set, consider tocolytic (terbutaline 250 mcg IV/SC; salbutamol inhaler if terbutaline unavailable). Source: MOH 2013 §B.8.1, §C."
    ),
    (
        "When is oxytocin combined use with prostaglandins acceptable?",
        "Combined use is DANGEROUS — risk of hyperstimulation, uterine rupture. Allow at least 6 hours between the last vaginal PGE2 dose and starting oxytocin. Source: MOH 2013 §B.6.3.2."
    ),
    (
        "Pethidine dose for pain relief in labour?",
        "Pethidine 1-1.5 mg/kg IM, may repeat after 4-6 hours. Third dose only with senior agreement. Avoid if delivery anticipated within 4 hours. Co-administer with metoclopramide 5mg IV or 10mg IM to reduce nausea and gastric stasis. Naloxone 100 mcg/kg IV available for neonatal respiratory depression. Source: MOH 2013 §E.1.2.2.A."
    ),
    (
        "What is the routine episiotomy policy?",
        "Routine episiotomy should NOT be carried out during spontaneous vaginal birth. Episiotomy is selective — for instrumental birth, suspected fetal compromise, or imminent severe perineal tearing. When indicated, perform mediolateral episiotomy at 45-60 degrees to the right, beginning at the fourchette, at the time of crowning, after infiltration with up to 20ml of 1% lignocaine. Source: MOH 2013 §A.3.2.2.5."
    ),
    (
        "How do I classify perineal tears?",
        "First degree: skin only. Second degree: perineal muscles, not anal sphincter. Third degree: involves anal sphincter complex. Fourth degree: involves anal sphincter complex AND anal epithelium. Source: MOH 2013 §A.5."
    ),
    (
        "Preferred suture material for perineal repair?",
        "Rapidly absorbable polyglactin acid (e.g. Vicryl Rapide). Repair under tested effective analgesia — infiltration with up to 20ml of 1% lignocaine or by topping up an epidural. Always do a rectal examination after repair to ensure no sutures through rectal mucosa. Source: MOH 2013 §A.5."
    ),
    (
        "When should breastfeeding be initiated?",
        "Initiate breastfeeding within 30 minutes of birth (ideally within 1 hour). Deliver baby onto mother's abdomen, dry, skin-to-skin, then put baby between mother's breasts for skin-to-skin care. Source: MOH 2013 §A.4."
    ),
    (
        "Should I always do a vaginal examination on admission to labour room?",
        "VE should be OFFERED, not mandatory. Before VE: ensure valid indication, consent, privacy, dignity, comfort; explain procedure and findings sensitively. VE is invasive and can be distressing — only do it if it will add to decision-making. Source: MOH 2013 §A.3.2.1.2a."
    ),
    (
        "What food and drink is allowed in labour?",
        "Clear non-fizzy liquids are encouraged throughout labour (oral rehydration fluid or king coconut water are better than plain water — isotonic). In the LATENT phase, light solids like biscuits and fruits are also acceptable. No solids in active phase due to risk if GA needed. Source: MOH 2013 §A.3.1.5."
    ),
]


# ============================================================
# SECTION 5: ANTENATAL CARE & DANGER SIGNS (English)
# Source: WHO ANC recommendations + RCOG/NICE
# ============================================================

ANC_EN = [
    (
        "What is the recommended antenatal visit schedule for a low-risk Sri Lankan pregnancy?",
        "Sri Lanka uses a tailored schedule (PHM-led): booking visit before 12 weeks, then ~4-weekly until 28 weeks, 2-weekly from 28-36 weeks, weekly from 36 weeks until delivery. High-risk pregnancies have additional visits. Total minimum 8 contacts per WHO 2016 ANC recommendation. Source: WHO ANC 2016 / Sri Lanka Family Health Bureau."
    ),
    (
        "Which danger signs should every pregnant mother be taught to recognize?",
        "Teach all mothers to come to hospital immediately for: severe headache, blurred vision or seeing spots, swelling of face/hands, severe upper abdominal (RUQ) pain, convulsions, vaginal bleeding any amount, watery discharge before term (PROM), reduced or absent fetal movement, severe vomiting, fever, painful urination, breathlessness at rest. Source: WHO ANC / RCOG / MOH PHM training materials."
    ),
    (
        "When should fetal movement counting begin and what is the threshold?",
        "Fetal movement awareness from 28 weeks. No single 'count' is mandated by latest RCOG — mothers should be alert to changes in their baby's usual pattern. Reduced fetal movement = come for assessment SAME DAY. Absent fetal movement > 12 hours = URGENT. Source: RCOG GTG 57 / MOH."
    ),
    (
        "When should anti-D be given to an Rh-negative pregnant woman?",
        "Anti-D Ig 1500 IU IM at 28-30 weeks (single dose) OR 500 IU IM at 28 and 34 weeks (two-dose regimen). Additionally for sensitizing events (bleeding, ECV, amniocentesis, miscarriage, abdominal trauma). Postpartum: within 72 hours if baby is Rh-positive. Source: RCOG GTG 22."
    ),
    (
        "How much iron and folate should a pregnant woman receive routinely in Sri Lanka?",
        "Sri Lanka Family Health Bureau standard: ferrous sulphate 200mg (containing 60mg elemental iron) + folic acid 400 mcg daily, started from first ANC contact, continued until 6 weeks postpartum. Calcium 600mg daily for high-risk women. Source: Sri Lanka FHB Maternal Nutrition Policy."
    ),
    (
        "Which infections should every pregnant woman in Sri Lanka be screened for?",
        "Routine screening at booking: HIV (with informed consent), syphilis (VDRL or RPR), Hepatitis B surface antigen, rubella IgG (if not previously immune), urine for asymptomatic bacteriuria (mid-stream culture). Plus FBC for anaemia and Hb electrophoresis if thalassaemia suspected (high prevalence in Sri Lanka). Source: Sri Lanka FHB ANC guideline."
    ),
    (
        "When should tetanus toxoid be given in pregnancy?",
        "Sri Lanka policy: 2 doses of Td (tetanus + diphtheria) in the first pregnancy, given 4 weeks apart, with second dose at least 4 weeks before delivery. Booster in subsequent pregnancies. Protects mother and prevents neonatal tetanus. Source: Sri Lanka FHB EPI schedule."
    ),
    (
        "Which ultrasound scans are recommended in pregnancy?",
        "Dating scan 7-13 weeks (best at 11-13+6 weeks with NT measurement). Anomaly scan at 18-20+6 weeks. Growth scan at 28 weeks (selective) and 36 weeks (selective). For high-risk: serial growth scans 2-4 weekly. Source: RCOG/NICE."
    ),
    (
        "Reduced fetal movement at 32 weeks — what do I do?",
        "Reduced fetal movement at >= 28 weeks: (1) Maternal palpation of abdomen and uterus. (2) Auscultation/CTG for 20 min minimum. (3) Same-day USS if persistent reduced movements, growth assessment, amniotic fluid volume, biophysical profile. (4) Refer for senior review. NEVER reassure on intermittent auscultation alone after 28 weeks. Source: RCOG GTG 57."
    ),
    (
        "Bleeding in second/third trimester — what do I check first?",
        "Antepartum haemorrhage. (1) NEVER do a digital VE before excluding placenta praevia (USS first). (2) Vital signs, fetal heart, fundal height. (3) Speculum exam to localize bleeding (cervix vs higher). (4) USS — placental site, fluid, abruption signs. (5) Cross-match, FBC, coagulation, Kleihauer if Rh-negative. (6) Refer urgently. Source: RCOG GTG 63."
    ),
]


# ============================================================
# SECTION 6: ANAEMIA IN PREGNANCY (English)
# Source: WHO + RCOG GTG 47 + Sri Lanka iron policy
# ============================================================

ANAEMIA_EN = [
    (
        "What Hb defines anaemia in pregnancy in Sri Lanka?",
        "Hb < 11 g/dL in the first trimester (and >= 28 weeks) OR Hb < 10.5 g/dL in the second trimester. WHO classification: 9-10.9 mild, 7-8.9 moderate, < 7 severe. (Sri Lanka MOH uses < 8 for severe/URGENT). Source: WHO + MOH 2013."
    ),
    (
        "What is the iron dose for treating iron deficiency anaemia in pregnancy?",
        "Therapeutic dose: oral elemental iron 100-200 mg/day (e.g. ferrous sulphate 200mg tid). Take between meals with vitamin C (orange juice) for absorption. Avoid taking with tea/coffee/calcium. Recheck Hb in 2 weeks — rise of 1 g/dL expected. Source: RCOG GTG 47 / Sri Lanka FHB."
    ),
    (
        "When should I consider IV iron in pregnancy?",
        "IV iron (iron sucrose or ferric carboxymaltose) is indicated when: oral iron not tolerated (severe GI side effects), absorption impaired, non-compliance demonstrated, Hb < 9 g/dL after 34 weeks (no time for oral to work), or non-response after 2-4 weeks of oral therapy. Source: RCOG GTG 47."
    ),
    (
        "When should I transfuse blood for anaemia in pregnancy?",
        "Transfusion thresholds (no active bleeding): Hb < 7 g/dL with cardiac/respiratory symptoms, Hb < 6 g/dL generally, or symptomatic Hb 6-8 g/dL near term. Avoid transfusion if oral/IV iron will work in time. Always document indication and obtain informed consent. Source: RCOG GTG 47."
    ),
    (
        "What is the role of thalassaemia screening in Sri Lankan pregnancy?",
        "Sri Lanka has high prevalence of thalassaemia (~2% beta-thalassaemia trait). Screen all women at booking with FBC + Hb electrophoresis if MCV/MCH low or family history. If mother is carrier, test partner. If both carriers, refer for prenatal diagnosis counselling. Source: Sri Lanka National Thalassaemia Programme."
    ),
    (
        "Pregnant woman with Hb 7.5 g/dL at 32 weeks, no symptoms, no bleeding. Plan?",
        "MODERATE anaemia — urgent action without transfusion. (1) Confirm iron deficiency: low ferritin, low MCV, low MCH; rule out thalassaemia. (2) Start oral elemental iron 200 mg/day + folic acid 5 mg + vitamin C. (3) If poor tolerance or < 4 weeks to delivery, start IV iron sucrose. (4) Re-check Hb in 2 weeks. (5) Refer to specialist for IV iron + delivery planning. Source: RCOG GTG 47 + MOH."
    ),
    (
        "Hb < 8 g/dL in a pregnant woman — risk level?",
        "URGENT — severe anaemia. High risk of decompensation in labour and PPH. Action: same-day specialist referral, IV iron or transfusion based on gestation, repeat Hb 48 hours, plan delivery in tertiary facility with blood available. Source: MOH 2013 / RCOG GTG 47."
    ),
]


# ============================================================
# SECTION 7: MISC — BREECH, TWINS, VBAC, INFECTIONS (English)
# Source: RCOG Green-top guidelines
# ============================================================

MISC_EN = [
    (
        "Breech presentation at 36 weeks — what do I do?",
        "(1) Confirm by USS. (2) Counsel mother about external cephalic version (ECV) — success rate 50-60% in nulliparas, higher in multiparas. (3) Offer ECV at 36-37 weeks. (4) Contraindications to ECV: placenta praevia, ruptured membranes, abnormal CTG, multiple pregnancy, recent APH, scarred uterus (relative). (5) If ECV fails or declined: discuss planned CS vs vaginal breech birth (CS recommended in most settings). Source: RCOG GTG 20a, 20b."
    ),
    (
        "VBAC — what are the success rates and major risks?",
        "Vaginal birth after caesarean: success rate ~72-75% overall. Major risk: uterine scar rupture ~0.5% with one previous CS, increases with multiple previous CS or short inter-pregnancy interval. Counselling required. Suitable if: one previous lower-segment CS, no other CS indication this pregnancy, no contraindication to vaginal birth. Continuous CTG in labour. Avoid prostaglandins for IOL. Source: RCOG GTG 45."
    ),
    (
        "Group B Strep screening policy?",
        "Sri Lanka does not have universal GBS screening. Use risk-based approach: intrapartum IV penicillin if previous baby with GBS disease, GBS bacteriuria this pregnancy, preterm labour < 37 weeks, prolonged ROM > 18 hours, intrapartum fever >= 38 C. Source: RCOG GTG 36 (risk-based) / UK NICE."
    ),
    (
        "Twin pregnancy — what extra care is needed?",
        "(1) Confirm chorionicity at first scan (11-13+6 weeks) — best by lambda/T sign. (2) DCDA: scans every 4 weeks from 20 weeks. MCDA: 2-weekly scans from 16 weeks (TTTS surveillance). MCMA: weekly from 24 weeks. (3) Aspirin 75-150 mg from 12 weeks (pre-eclampsia prevention). (4) Iron and folate routine. (5) Plan delivery: uncomplicated DCDA 37+0-37+6, MCDA 36+0-36+6, MCMA 32-34 weeks by CS. Source: RCOG/NICE NG137."
    ),
    (
        "Suspected chorioamnionitis in labour — action?",
        "Maternal fever >= 38 C, fetal tachycardia, uterine tenderness, foul-smelling liquor. (1) IV broad-spectrum antibiotics — typically ampicillin 2g IV q6h + gentamicin 5mg/kg IV od (cover GBS, E. coli, anaerobes). (2) Continuous fetal monitoring. (3) Plan delivery — do not delay. (4) Alert neonatal team. Source: RCOG / Sri Lanka MOH antibiotic policy."
    ),
    (
        "Dengue in pregnancy — special considerations?",
        "Dengue is common in Sri Lanka and a PPH risk factor. (1) Daily FBC during febrile phase — thrombocytopenia and haemoconcentration. (2) Watch for warning signs of DHF (severe abdominal pain, persistent vomiting, restlessness, bleeding). (3) Fluid management critical — avoid both over and under-resuscitation. (4) Delivery during shock phase is high risk — try to defer until recovery if possible. (5) Cross-match blood early. Source: Sri Lanka MOH Dengue Guidelines + WHO."
    ),
    (
        "Premature rupture of membranes at term (after 37 weeks) — management?",
        "Term PROM. In absence of fetal or maternal compromise: (1) Watchful expectant management for up to 24 hours. (2) If no spontaneous labour in 24 hours, induce — either oxytocin infusion or prostaglandin. (3) Avoid digital VE to reduce ascending infection. (4) Speculum exam if needed. (5) Monitor for chorioamnionitis. Source: MOH 2013 §B.4.2 / RCOG GTG 44."
    ),
    (
        "Preterm PROM at 32 weeks — management?",
        "PPROM at 32 weeks: (1) Speculum to confirm. (2) Avoid digital VE. (3) Vaginal/cervical swab. (4) Antibiotics — erythromycin 250mg qid for 10 days (prolongs latency). (5) Corticosteroids: dexamethasone 6mg IM q12h x 4 doses or betamethasone 12mg IM q24h x 2 doses (fetal lung maturity). (6) MgSO4 if delivery imminent < 32 weeks (neuroprotection). (7) Plan delivery after 34 weeks if no other indication earlier. Source: MOH 2013 §B.4.3 + RCOG GTG 73."
    ),
]


# ============================================================
# SECTION 8: NICE NG133 (Hypertension in pregnancy) — direct from PDF
# ============================================================

NICE_NG133_EN = [
    (
        "What aspirin dose does NICE NG133 recommend for women at high risk of pre-eclampsia?",
        "Aspirin 75 mg to 150 mg once daily from 12 weeks until birth of the baby. Note: dose was updated upward from the 2010 guideline (75 mg) — current NICE recommendation accepts up to 150 mg. Source: NICE NG133 §1.1.2."
    ),
    (
        "Symptoms that NICE NG133 says require IMMEDIATE review for pre-eclampsia?",
        "Severe headache; problems with vision (blurring, flashing); severe pain just below the ribs (epigastric); vomiting; sudden swelling of the face, hands or feet. Advise every pregnant woman to see a healthcare professional immediately if any of these appear. Source: NICE NG133 §1.1.1."
    ),
    (
        "Should I order a 24-hour urine collection to quantify proteinuria in a pregnant woman?",
        "No. NICE NG133 §1.2.5 says: do not routinely use 24-hour urine collection to quantify proteinuria. Use protein:creatinine ratio or albumin:creatinine ratio on a spot sample instead (threshold 30 mg/mmol for PCR; 8 mg/mmol for ACR). Source: NICE NG133 §1.2.4–1.2.7."
    ),
    (
        "Target BP when treating chronic or gestational hypertension or pre-eclampsia per NICE 2019?",
        "Aim for BP of 135/85 mmHg or less on antihypertensive treatment, for chronic hypertension, gestational hypertension AND pre-eclampsia. Source: NICE NG133 §1.3.9, Table 1, Table 2."
    ),
    (
        "First-line antihypertensive in pregnancy per NICE NG133?",
        "Labetalol — first choice in chronic hypertension, gestational hypertension and pre-eclampsia. If labetalol unsuitable, use nifedipine. If both unsuitable, use methyldopa. Source: NICE NG133 §1.3.10, §1.4.5, §1.5.6."
    ),
    (
        "When should methyldopa be stopped postpartum per NICE?",
        "Stop methyldopa within 2 days after birth and change to an alternative antihypertensive (methyldopa is associated with postnatal depression). Source: NICE NG133 §1.3.19, §1.4.12, §1.5.18."
    ),
    (
        "Per NICE NG133, BP monitoring frequency for inpatient with severe hypertension?",
        "Every 15 to 30 minutes until BP is less than 160/110 mmHg, then at least 4 times daily while the woman is an inpatient. Source: NICE NG133 Table 2."
    ),
    (
        "When does NICE recommend planned early birth in chronic or gestational hypertension?",
        "Do not offer planned early birth before 37 weeks for women whose BP is below 160/110 mmHg unless other medical indications. Beyond 37 weeks, timing should be jointly agreed with the senior obstetrician. Source: NICE NG133 §1.3.14, §1.4.7."
    ),
    (
        "What is PLGF-based testing and when is it indicated per NICE?",
        "Placental growth factor (PLGF)-based testing helps rule out pre-eclampsia in women with suspected pre-eclampsia (e.g., gestational hypertension) between 20 weeks and 36 weeks + 6 days. Carry out PLGF-based testing on 1 occasion. Source: NICE NG133 §1.4.4, NICE DG23/DG49."
    ),
    (
        "When should IV magnesium sulfate be given to women with severe pre-eclampsia per NICE?",
        "Consider IV magnesium sulfate for women with severe pre-eclampsia who are in a critical care setting, if birth is planned within 24 hours. Loading dose 4 g IV over 5 to 15 min, then maintenance infusion 1 g per hour for 24 hours. If eclamptic fit recurs, give further 2-4 g IV over 5 min. Source: NICE NG133 §1.8.2, §1.8.4."
    ),
    (
        "Per NICE NG133, BP target after the birth in women who had hypertension in pregnancy?",
        "Aim to keep BP lower than 140/90 mmHg. Reduce antihypertensive treatment if BP falls below 130/80 mmHg. Offer review 2 weeks after birth and again 6 to 8 weeks postpartum. Source: NICE NG133 §1.3.18, §1.4.11–1.4.16."
    ),
    (
        "Which antihypertensives are recommended for postnatal use including breastfeeding per NICE?",
        "Enalapril (with renal monitoring) is first choice; if of Black African or Caribbean family origin, nifedipine (or amlodipine if previously used) is preferred; for combined choice, consider nifedipine OR amlodipine combined with enalapril. Atenolol or labetalol may be added or used to replace 1 of the agents. Avoid diuretics or angiotensin receptor blockers while breastfeeding. Source: NICE NG133 §1.9."
    ),
    (
        "Which moderate risk factors trigger aspirin per NICE NG133?",
        "Two or more moderate risk factors: nulliparity, age 40 or older, pregnancy interval > 10 years, BMI ≥ 35 kg/m² at booking, family history of pre-eclampsia, multi-fetal pregnancy. Start aspirin 75–150 mg from 12 weeks. Source: NICE NG133 §1.1.3."
    ),
    (
        "Should bed rest in hospital be offered as treatment for gestational hypertension per NICE?",
        "No. NICE NG133 §1.4.6 explicitly says: do not offer bed rest in hospital as a treatment for gestational hypertension. Source: NICE NG133 §1.4.6."
    ),
    (
        "What does NICE say about salt restriction to prevent pre-eclampsia?",
        "Do not recommend salt restriction during pregnancy solely to prevent gestational hypertension or pre-eclampsia. Source: NICE NG133 §1.1.6."
    ),
]

# ============================================================
# SECTION 9: NICE NG3 (Diabetes in pregnancy) — direct from PDF
# ============================================================

NICE_NG3_EN = [
    (
        "Diagnostic threshold for gestational diabetes per NICE NG3 (75g OGTT)?",
        "Diagnose GDM if fasting plasma glucose ≥ 5.6 mmol/L OR 2-hour plasma glucose ≥ 7.8 mmol/L on 75 g OGTT. Test at 24–28 weeks (or sooner for previous GDM). Source: NICE NG3 §1.2.5, §1.2.8."
    ),
    (
        "Capillary plasma glucose targets in pregnant women with any form of diabetes per NICE NG3?",
        "Fasting: below 5.3 mmol/L; 1 hour after meals: below 7.8 mmol/L (or 2 hours after meals: below 6.4 mmol/L). Women on insulin should keep glucose above 4 mmol/L to avoid hypoglycaemia. Source: NICE NG3 §1.3.5, §1.3.6."
    ),
    (
        "Preconception HbA1c targets and contraindications to conception per NICE NG3?",
        "Aim for HbA1c below 48 mmol/mol (6.5%) before conception, if achievable without disabling hypoglycaemia. Strongly advise against conception if HbA1c above 86 mmol/mol (10%). Folic acid 5 mg/day until 12 weeks. Source: NICE NG3 §1.1.18–1.1.20, §1.1.11."
    ),
    (
        "Which diabetes drugs can be used in pregnancy per NICE NG3?",
        "Allowed: insulin (all preparations including rapid-acting analogues aspart and lispro), metformin (off-label but recommended as adjunct or alternative to insulin), isophane (NPH) as first-choice long-acting insulin. Stop before/at conception: all other oral hypoglycaemic agents, ACE inhibitors, ARBs, statins. Source: NICE NG3 §1.1.21–1.1.25."
    ),
    (
        "First-line treatment if GDM glucose targets not met with diet and exercise after 1-2 weeks?",
        "Offer metformin. If contraindicated or unacceptable, offer insulin. If targets still not met on metformin + lifestyle, add insulin. Source: NICE NG3 §1.2.19–1.2.21."
    ),
    (
        "Per NICE NG3, when should women with GDM and fasting glucose ≥ 7.0 mmol/L start insulin?",
        "Offer immediate treatment with insulin, with or without metformin, plus diet and exercise changes. For fasting 6.0–6.9 mmol/L with complications (macrosomia or hydramnios) consider immediate insulin. Source: NICE NG3 §1.2.22, §1.2.23."
    ),
    (
        "Timing of birth in women with type 1 or 2 diabetes per NICE NG3?",
        "Elective birth by induction (or CS if indicated) between 37+0 and 38+6 weeks. Consider earlier if metabolic or maternal/fetal complications. Source: NICE NG3 §1.4.2, §1.4.3."
    ),
    (
        "Timing of birth in uncomplicated gestational diabetes per NICE NG3?",
        "Give birth no later than 40+6 weeks. Offer elective birth by induction (or CS if indicated) if not given birth by then. Source: NICE NG3 §1.4.4."
    ),
    (
        "Intrapartum capillary plasma glucose target for women with diabetes per NICE NG3?",
        "Maintain capillary plasma glucose between 4 mmol/L and 7 mmol/L during labour and birth. Monitor every hour. Use IV dextrose-insulin infusion if glucose falls outside this range. Source: NICE NG3 §1.4.10–1.4.12."
    ),
    (
        "What neonatal blood glucose monitoring is required for babies of diabetic mothers per NICE NG3?",
        "Blood glucose test 2 to 4 hours after birth. Feed within 30 minutes of birth, then every 2–3 hours until pre-feed glucose is maintained ≥ 2.0 mmol/L. Additional intervention (tube feeding or IV dextrose) only if glucose < 2.0 mmol/L on 2 consecutive readings despite feeding, abnormal clinical signs, or unable to feed. Source: NICE NG3 §1.5.3, §1.5.9, §1.5.10."
    ),
    (
        "Postnatal diabetes testing for women who had GDM per NICE NG3?",
        "Test glucose before transfer to community care. Offer fasting plasma glucose 6–13 weeks after birth (or HbA1c after 13 weeks if FPG missed). Do not routinely offer 75g 2-hour OGTT postnatally. Annual HbA1c thereafter if negative. Source: NICE NG3 §1.6.11–1.6.14."
    ),
    (
        "Per NICE NG3, when is rtCGM offered to pregnant women with type 1 diabetes?",
        "Offer real-time continuous glucose monitoring (rtCGM) to ALL pregnant women with type 1 diabetes — proven to improve target achievement and neonatal outcomes. Offer isCGM ('flash') if rtCGM cannot be used or preferred. Source: NICE NG3 §1.3.17, §1.3.18."
    ),
    (
        "When should women with type 1 diabetes test for ketonaemia per NICE NG3?",
        "If they become hyperglycaemic or unwell, test for ketonaemia urgently and seek medical advice. Offer ketone testing strips and meter. Admit immediately for level 2 critical care if DKA suspected. Source: NICE NG3 §1.3.21–1.3.24."
    ),
    (
        "Retinal assessment schedule for women with pre-existing diabetes during pregnancy per NICE NG3?",
        "Retinal assessment by digital imaging at first antenatal clinic visit (if none in last 3 months). If diabetic retinopathy, repeat at 16–20 weeks. Repeat for all at 28 weeks. Source: NICE NG3 §1.3.25."
    ),
]

# ============================================================
# SECTION 10: RCOG GTG 52 (PPH) + GTG 47 (Blood Transfusion) — from PDFs
# ============================================================

RCOG_PPH_TRANSFUSION_EN = [
    (
        "RCOG GTG 52 prophylactic uterotonic recommendation for vaginal birth?",
        "Oxytocin 10 IU by intramuscular injection is the regimen of choice for active management of the third stage in women without PPH risk factors. Higher doses (40 or 80 IU) are not more effective. Source: RCOG GTG 52 §4.1."
    ),
    (
        "Prophylactic uterotonic for caesarean section per RCOG GTG 52?",
        "Oxytocin 5 IU by slow intravenous injection. Higher rapid IV doses cause hypotension. Consider IV tranexamic acid 0.5–1.0 g additionally at CS for women at increased risk of PPH. Source: RCOG GTG 52 §4.1, §4.2."
    ),
    (
        "When is ergometrine–oxytocin (Syntometrine) used per RCOG GTG 52?",
        "Ergometrine–oxytocin may be used in absence of hypertension in women at increased risk of PPH. It reduces blood loss by ~80 ml compared with oxytocin alone but causes 5-fold more nausea, vomiting and BP elevation. CONTRAINDICATED in hypertension or pre-eclampsia. Source: RCOG GTG 52 §4.1."
    ),
    (
        "Order of pharmacological treatment of uterine atony per RCOG GTG 52?",
        "Sequential drugs for atonic PPH: (1) oxytocin 5 IU slow IV (may repeat); (2) ergometrine 0.5 mg slow IV/IM — CI in HTN/PE; (3) oxytocin infusion 40 IU in 500 ml crystalloid at 125 ml/hr; (4) carboprost 0.25 mg IM, repeat at intervals ≥ 15 min, max 8 doses; (5) misoprostol 800 micrograms sublingually. Source: RCOG GTG 52 §5.3.3."
    ),
    (
        "When should tranexamic acid be used in established PPH per WOMAN trial / RCOG?",
        "Tranexamic acid 1 g IV over 10 min as soon as bleeding is recognised, repeat after 30 min if bleeding continues. WOMAN trial: most effective when given within 3 hours of onset; reduces death from bleeding by ~31% if given early. Source: RCOG GTG 52 §5.3.4 / WOMAN trial 2017."
    ),
    (
        "First-line surgical intervention for uterine atony unresponsive to drugs per RCOG GTG 52?",
        "Intrauterine balloon tamponade — appropriate first-line 'surgical' intervention for most women in whom uterine atony is the cause of haemorrhage. Conservative surgical interventions (B-Lynch brace, uterine artery ligation) come second. Hysterectomy 'sooner rather than later' if placenta accreta or rupture. Source: RCOG GTG 52 §7.3."
    ),
    (
        "RCOG GTG 47 definition of anaemia in pregnancy?",
        "First trimester Hb < 110 g/L; second/third trimester Hb < 105 g/L; postpartum Hb < 100 g/L. (BCSH thresholds adopted by RCOG.) Source: RCOG GTG 47 §4.1.1."
    ),
    (
        "When should pregnant women be screened for anaemia per RCOG GTG 47?",
        "At booking and at 28 weeks. Women with multiple pregnancies have an additional FBC at 20–24 weeks. Source: RCOG GTG 47 §4.1.1."
    ),
    (
        "Approach to suspected iron deficiency anaemia in pregnancy per RCOG GTG 47?",
        "For normocytic or microcytic anaemia, trial oral iron first. Check Hb at 2 weeks — if no rise AND compliance confirmed, perform further tests (ferritin, haemoglobinopathy screen). Vitamin C improves absorption; tea/coffee inhibit. Source: RCOG GTG 47 §4.1.1, §4.1.2."
    ),
    (
        "Indications for parenteral (IV) iron in pregnancy per RCOG GTG 47?",
        "Oral iron not tolerated, not absorbed, compliance in doubt, OR approaching term with insufficient time for oral therapy. Administer only where staff trained for anaphylaxis are available. Source: RCOG GTG 47 §4.1.2."
    ),
    (
        "Red cell transfusion trigger for non-bleeding pregnant/postpartum women per RCOG GTG 47?",
        "No firm criteria — decision is clinical. If Hb < 70 g/L with no active bleeding, consider transfusion (especially with cardiac/respiratory symptoms). Below 60 g/L, transfusion generally indicated. Always document indication and consent. Source: RCOG GTG 47 §7.2.1, §11."
    ),
    (
        "Platelet transfusion trigger in major obstetric haemorrhage per RCOG GTG 47?",
        "75 × 10⁹/L during ongoing haemorrhage. Maintain a margin of safety to allow for further fall. Source: RCOG GTG 47 §7.2.4."
    ),
    (
        "Emergency blood for catastrophic haemorrhage when group unknown?",
        "Group O RhD-negative AND K (Kell)-negative red cells should be available for immediate issue. Switch to group-specific or cross-matched units as soon as feasible. Source: RCOG GTG 47 §5.3."
    ),
]

# ============================================================
# SECTION 11: RCOG GTG 57 (Reduced Fetal Movements) — from PDF
# ============================================================

RCOG_RFM_EN = [
    (
        "What advice should be given to women about fetal movements per RCOG GTG 57?",
        "Advise women to report any decrease or cessation of fetal movements to their maternity provider. There is INSUFFICIENT evidence to recommend formal kick-counting using specified numbers (e.g., 'count to 10'). Encourage awareness of the pattern, not a number. Source: RCOG GTG 57 Recommendations 1–2."
    ),
    (
        "Why is reduced fetal movement clinically significant per RCOG GTG 57?",
        "Meta-analysis of 39 studies: women with RFM had increased odds of stillbirth (OR 3.44, 95% CI 2.02–5.88) and SGA infant. Association is also with fetal growth restriction, infection, and feto-maternal haemorrhage. Source: RCOG GTG 57 §3."
    ),
    (
        "Initial assessment of a woman presenting with RFM in community per RCOG GTG 57?",
        "(1) Auscultate the fetal heart. (2) Take history. (3) Symphysis-fundal height measurement to assess size. (4) Arrange computerised CTG if ≥ 26+0 weeks to exclude acute compromise. (5) USS within 24 hours if RFM persists despite normal CTG, has risk factors for FGR/stillbirth, or no USS in preceding 2 weeks. Source: RCOG GTG 57 Recommendations."
    ),
    (
        "RFM before 24 weeks — what to do per RCOG GTG 57?",
        "Confirm fetal heartbeat by handheld Doppler. RFM is much less commonly perceptible before 24 weeks; reassurance + 24-hr follow-up if heartbeat present. Source: RCOG GTG 57 §Recommendations."
    ),
    (
        "Recurrent RFM management per RCOG GTG 57?",
        "Review case to exclude predisposing causes (FGR, placental insufficiency, infection, smoking, obesity, anterior placenta, polyhydramnios). Re-assess CTG and USS at each presentation. After 39+0 weeks with recurrent RFM, expediting birth does not appear to add risk. Source: RCOG GTG 57 §Recommendations."
    ),
    (
        "Should I attribute reduced fetal movements to maternal obesity or anterior placenta?",
        "No — RFM should not be attributed to these factors. Obese women and those with anterior placenta may genuinely have reduced perception, but treating their RFM as 'normal for them' risks missing fetal compromise. Always investigate. Source: RCOG GTG 57."
    ),
    (
        "When in multiple pregnancy does RFM warrant investigation per RCOG GTG 57?",
        "Always — investigations should include CTG (for each fetus where possible), assessment of fetal growth, liquor volume, and umbilical artery Doppler. Source: RCOG GTG 57 §Recommendations."
    ),
]

# ============================================================
# SECTION 12: NICE NG201 (Antenatal Care) — direct from PDF
# ============================================================

NICE_NG201_EN = [
    (
        "When should the first antenatal (booking) appointment take place per NICE NG201?",
        "By 10+0 weeks of pregnancy. If a woman contacts maternity services after 9+0 weeks, the booking appointment should take place within 2 weeks. Source: NICE NG201 §1.1.4–1.1.6."
    ),
    (
        "How many antenatal appointments does NICE NG201 plan for nulliparous and parous women?",
        "10 routine appointments for nulliparous women, 7 for parous women. Additional or longer appointments offered based on need. Source: NICE NG201 §1.1.7–1.1.10."
    ),
    (
        "When should symphysis-fundal height be measured per NICE NG201?",
        "At each antenatal appointment after 24+0 weeks. If concerns about small or large for gestational age, refer for assessment. Source: NICE NG201 §1.2.30."
    ),
    (
        "What does NICE NG201 advise about maternal sleep position?",
        "After 28 weeks, advise women to avoid going to sleep on their back. Use pillows to maintain side-lying position. Evidence links supine sleep position to increased stillbirth risk in late pregnancy. Source: NICE NG201 §1.3.25–1.3.26."
    ),
    (
        "First-line treatment for nausea and vomiting in pregnancy per NICE NG201?",
        "Reassure that mild-moderate nausea and vomiting are common and resolve by 16–20 weeks. Non-pharmacological: ginger. If pharmacological treatment chosen, offer an antiemetic (cyclizine, promethazine, prochlorperazine, ondansetron). IV fluids for moderate-severe nausea (preferably outpatient). Source: NICE NG201 §1.4.1–1.4.7."
    ),
    (
        "When is anti-D immunoglobulin offered for vaginal bleeding after 13 weeks per NICE NG201?",
        "Offer anti-D Ig to women who present with vaginal bleeding after 13 weeks if they are rhesus D-negative AND at risk of isoimmunisation. Also refer to secondary care for review. Source: NICE NG201 §1.4.16–1.4.17."
    ),
    (
        "Heartburn in pregnancy first-line treatment per NICE NG201?",
        "Lifestyle and dietary advice first. Then trial of an antacid or alginate. H2-receptor antagonists / PPIs only if simple measures fail. Source: NICE NG201 §1.4.8–1.4.9."
    ),
    (
        "Treatment of suspected vaginal candidiasis in pregnancy per NICE NG201?",
        "Offer vaginal imidazole (such as clotrimazole or econazole). Oral azoles (e.g., fluconazole) generally avoided in pregnancy. Source: NICE NG201 §1.4.13."
    ),
    (
        "Pelvic girdle pain in pregnancy — NICE NG201 advice?",
        "Consider referral to physiotherapy services for exercise advice and/or a non-rigid lumbopelvic belt. Source: NICE NG201 §1.4.15."
    ),
]


# ============================================================
# SECTION 13: SINHALA (සිංහල) — critical content for PHMs and mothers
# USER MUST VERIFY EACH PAIR — Sinhala generated by AI from English source
# Highest-value subset: danger signs, vital interpretation, urgent actions
# ============================================================

SINHALA_SI = [
    # --- Danger signs (mother-facing) ---
    (
        "ගර්භණී මවකගේ බරපතල අනතුරු ලකුණු මොනවාද?",
        "වහාම රෝහලට යන්න: දැඩි හිසරදය, දර්ශන පැහැදිලි නැති වීම හෝ ආලෝකය දැකීම, මුහුණ සහ අත් ඉදිමීම, බඩේ ඉහළ දකුණු පැත්තේ දරුණු වේදනාව, ඕනෑම යෝනි මාර්ගයෙන් ලේ ගැලීම, දිනකට වඩා දරුවාගේ චලනය නැති වීම, ඉහළ උණ, මුත්‍රා කිරීමේදී වේදනාව, විවේකයේදී හුස්ම ගැනීමේ අපහසුව. මූලාශ්‍රය: WHO ANC / RCOG / PHM පුහුණු."
    ),
    (
        "මගේ රුධිර පීඩනය 162/108 සහ බඩේ ඉහළ දකුණේ වේදනාව තිබේ. මගේ ස්ථානය කුමක්ද?",
        "හදිසි - මේ දරුණු ප්‍රාක්-ඉක්ලැම්ප්සියාව (severe pre-eclampsia) විය හැක. වහාම රෝහලට යන්න. රුධිර පීඩනය 160/110ට වඩා ඉහළ සහ බඩේ වේදනාව ස්නායු හදිසි ස්ථානයක ලකුණු වේ. ප්‍රමාද නොකරන්න. මූලාශ්‍රය: NICE NG133 / MOH 2013."
    ),
    (
        "ගර්භණී වෙලා මාස 7යි. දරුවාගේ සෙලවීම අඩුයි කියලා හිතෙනවා. මොකද කරන්නේ?",
        "අද වහාම සායනයට හෝ රෝහලට යන්න. දරුවාගේ සෙලවීම අඩු වීම සැකකටයුත් ලකුණක්. CTG සහ අල්ට්‍රා සවුන්ඩ් අවශ්‍යයි. දරුවාගේ සෙලවීම් සංඛ්‍යාවක් ගණන් කරන්න අවශ්‍ය නැත - වෙනස හඳුනා ගැනීම වැදගත්. මූලාශ්‍රය: RCOG GTG 57."
    ),
    (
        "පේවී වැගිරෙන ලේ වැගිරීමක් තිබේ සහ මම සති 32ක ගර්භණී. කුමක් කරන්නද?",
        "හදිසි - වහාම රෝහලට යන්න. ගර්භණී දෙවෙනි හෝ තුන්වෙනි ත්‍රෛමාසිකයේ ලේ ගැලීම placenta praevia හෝ placental abruption විය හැක. නිවසේදී කිසිම පරීක්ෂණයක් කරන්න එපා. රෝහලට යන්නේ වැතිර වැතිර. මූලාශ්‍රය: RCOG GTG 63."
    ),
    (
        "ගර්භණී කාලයේ දරුවාගේ සෙලවීම ගණන් කරන්න ඕනේද?",
        "අවශ්‍ය නැත. නවතම RCOG මාර්ගෝපදේශය අනුව නිශ්චිත සෙලවීම් සංඛ්‍යාවක් (උදා: 'දහයක් ගණන් කරන්න') නිර්දේශ කරන්නේ නැත. දරුවාගේ සාමාන්‍ය චලන රටාවට ඔබ පුරුදු වන්න. රටාව වෙනස් වුවහොත් එම දිනය සායනයට යන්න. මූලාශ්‍රය: RCOG GTG 57."
    ),
    # --- Vitals interpretation ---
    (
        "ගර්භණී කාලයේ සාමාන්‍ය රුධිර පීඩනය කොච්චරද?",
        "සාමාන්‍ය: 140/90ට වඩා පහළ. 140-159/90-109 - පරෙස්සමින් (gestational hypertension). 160/110 හෝ ඊට වැඩි - හදිසි (severe hypertension), වහාම පත්‍ය. ප්‍රෝටීන් මුත්‍රාවේ ඇත්නම් pre-eclampsia. මූලාශ්‍රය: NICE NG133 / MOH 2013."
    ),
    (
        "හිමොග්ලොබින් අගය 7.5 g/dL. තත්වය කුමක්ද?",
        "මධ්‍යම රක්තහීනතාව (moderate anaemia). ඛනිජ දෘශ්‍ය යකඩ දිනකට 200mg + ෆෝලික් අම්ලය 5mg + විටමින් C ආරම්භ කරන්න. සති 2ක දී Hb නැවත පරීක්ෂා කරන්න. දරුවා බෝ වීමට අඩු කාලයක් තිබේ නම් IV iron sucrose අවශ්‍ය විය හැක. රෝහල් සායනයට යොමු කරන්න. මූලාශ්‍රය: RCOG GTG 47."
    ),
    (
        "හිමොග්ලොබින් 8ට අඩුයි. මේක කොච්චර අන්තරායේ ද?",
        "හදිසි - දරුණු රක්තහීනතාව. දරු ප්‍රසූතියේදී decompensation සහ PPH අවදානම ඉහළයි. එදිනම විශේෂඥ සායනයට යොමු කරන්න. ගර්භණී කාලය මත IV iron හෝ රුධිර පැකේජ අවශ්‍යයි. තෘතීයික පහසුකම් ඇති රෝහලක ප්‍රසූතිය සැලසුම් කරන්න. මූලාශ්‍රය: MOH 2013 / RCOG GTG 47."
    ),
    (
        "Fundal height කොච්චරද සති ගණනට සමානවද?",
        "Symphysis-fundal height (SFH) ගර්භණී සතිවලට ±3cm ඇතුළත සාමාන්‍ය. උදා: 32 සති ගර්භණී - SFH ~32cm (29-35cm අතර සාමාන්‍ය). 24 සතියෙන් පසු එක් එක් සායනයේදී මැනීම. දෙපැත්තටම පිට වුවහොත් අල්ට්‍රාසවුන්ඩ් කරන්න. මූලාශ්‍රය: NICE NG201."
    ),
    # --- ANC routine ---
    (
        "පළමු ගර්භණී සායනය කවදා පැමිණිය යුතුද?",
        "හැකි ඉක්මනින් - සති 10ට කලින්. ප්‍රමාද වුවොත් සති 2ක් තුළ සායනය ලබා ගත යුතුය. පළමු ගර්භණී කාන්තාවන්ට 10ක්, දෙවෙනි හෝ ඊට වැඩි දරුවන්ට 7ක්. අවදානම් ඇත්නම් වැඩි සංඛ්‍යාවක්. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ශ්‍රී ලංකාවේ ගර්භණී කාන්තාවන් සඳහා නිතිපතා පරීක්ෂණ මොනවාද?",
        "පරිඝණනයේදී: HIV, VDRL (syphilis), Hepatitis B, rubella IgG, මුත්‍රා කල්චර්, FBC, Hb electrophoresis (තැලසීමියා සඳහා - ශ්‍රී ලංකාවේ ඉහළයි). සති 24-28: ඔරල් ග්ලූකෝස් 75g (GDM). සති 28: anti-D (Rh-නෙගටිව්), Hb නැවත. මූලාශ්‍රය: Sri Lanka FHB ANC."
    ),
    (
        "ගර්භණී කාලයේ යකඩ සහ ෆෝලික් අම්ලය ලබා ගත යුත්තේ කොච්චරද?",
        "Ferrous sulphate 200mg (පූලකයේ යකඩ 60mg) + ෆෝලික් අම්ලය 400 micrograms දිනපතා. ප්‍රථම ANC සිට ප්‍රසූතියෙන් සති 6 දක්වා. දියවැඩියාව හෝ සිංහල ඇඩෝ-නාඩි දෝෂ ඉතිහාසය නම් ෆෝලික් 5mg. මූලාශ්‍රය: Sri Lanka FHB."
    ),
    (
        "ටෙටනස් එන්නත් කිට්ටට කවදා දෙන්නේ?",
        "ශ්‍රී ලංකා ප්‍රතිපත්තිය: ප්‍රථම ගර්භණී කාලයේදී Td මාස්පත්වරුන් 2ක්, මුල් එක ANC හි, දෙවෙනි එක සති 4ක් අන්තරින්, ප්‍රසූතියට අවම සති 4කට කලින්. නැවත ගර්භණී වුවොත් booster doses. මූලාශ්‍රය: Sri Lanka EPI."
    ),
    # --- Diabetes ---
    (
        "Gestational diabetes රෝග විනිශ්චය කරන්නේ කොහොමද?",
        "75g OGTT පරීක්ෂණය. ආශ්‍රිත රුධිර ග්ලූකෝස් ≥ 5.6 mmol/L (100 mg/dL) හෝ පැය 2 පසු ≥ 7.8 mmol/L (140 mg/dL) ඕනෑම අගයක් ඉහළ නම් GDM. සති 24-28දී කරන්න (පෙර GDM තිබුණොත් වැඩි ඉක්මනින්). මූලාශ්‍රය: NICE NG3."
    ),
    (
        "GDM ඇති මව සඳහා රුධිර සීනි ඉලක්ක?",
        "කැපිලරි ග්ලූකෝස් ඉලක්ක (mmol/L / mg/dL): ආශ්‍රිත 5.3ට පහළ / 95ට පහළ. ආහාරයට පැය 1 පසු 7.8ට පහළ / 140ට පහළ. ආහාරයට පැය 2 පසු 6.4ට පහළ / 115ට පහළ. ඉන්සියුලින් භාවිතා කරන විට 4ට වඩා ඉහළ පවත්වා ගන්න (hypoglycaemia වළක්වන්න). මූලාශ්‍රය: NICE NG3."
    ),
    # --- PPH ---
    (
        "ප්‍රසූතියෙන් පසු ලේ ගැලීම නවත්වන්නේ කොහොමද?",
        "Atonic PPH ක්‍රියා: (1) පිහාටුව ස්පර්ශ කරන්න (uterine massage). (2) Oxytocin 10IU IM (හෝ 5IU IV slow). (3) Ergometrine 0.5mg IV/IM (BP නම් අත්හරින්න). (4) Oxytocin infusion 40IU 500ml මට්ටමක 125ml/පැයට. (5) Tranexamic acid 1g IV 10 මිනිත්තුවකින්. (6) Bimanual compression. (7) Misoprostol 800mcg sublingual. (8) Foley කන්ඩම් balloon. (9) කිසිම ප්‍රමාදයක් කිරීමට පෙර consultant. මූලාශ්‍රය: MOH 2013 / RCOG GTG 52."
    ),
    (
        "PPH වළක්වන්න මොකද කරන්න ඕනේ?",
        "ක්‍රියාකාරී තුන්වෙනි අවධිය (active management): (1) Oxytocin 10IU IM දරුවා උපතේදී. (2) කෝඩ් කලින් මිනිත්තු 2 ක් සඳහා ඉඩ දෙන්න. (3) Controlled cord traction. (4) Placenta පසුව uterine massage. අවදානම් කරුණු (පෙර PPH, anaemia, twins, polyhydramnios, dengue) ඇත්නම් විශේෂඥ සායනය. මූලාශ්‍රය: MOH 2013."
    ),
    # --- General ---
    (
        "ගර්භණී කාලයේ ASA (aspirin) ගන්න ඕනේ කවදාද?",
        "Pre-eclampsia අවදානම ඇත්නම් Aspirin 75-150mg දිනපතා සති 12 සිට දරු ප්‍රසූතිය දක්වා. ඉහළ අවදානම් (පෙර hypertensive pregnancy, CKD, autoimmune, diabetes, chronic HTN): ඕනෑම එකක් 1 ක් - aspirin ආරම්භ කරන්න. මධ්‍යම අවදානම් 2ක් ඇත්නම් - ආරම්භ කරන්න. මූලාශ්‍රය: NICE NG133."
    ),
    (
        "ගර්භණී කාලයේ සෝපානයේ සැතපීම ආරක්ෂිතද?",
        "සති 28 සිට පසු මව්වරුන් කරපිට (ස්පින්) සැතපීම වළක්වන්න උපදෙස්. පැත්තකට (පවුකරයේ) සැතපීමට කොට්ට යොදන්න. කරපිට සැතපීම පසු ගර්භණී කාලයේ stillbirth අවදානම සමඟ සම්බන්ධ වේ. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "මට ගර්භණී වමනය බොහෝ ඇත. කුමක් කරන්නේ?",
        "මෘදු සිට මධ්‍යම මාතෘ වමනය ස්වාභාවික සති 16-20දී නිවැරැදි වේ. ඉඟුරු උත්සාහ කරන්න. දරුණු නම් ඇන්ටිමෙටික් (cyclizine, promethazine, prochlorperazine, ondansetron). ඕන්නම් IV ද්‍රව. Hyperemesis gravidarum (අඛණ්ඩ වමනය, බර අඩුවීම, dehydration) නම් රෝහල් ප්‍රවේශය. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ පේවී ඇතිරෝමා ඇතිවුවොත් කුමක් කරන්නේ?",
        "Imidazole ඔසු යෝනි මාර්ගයේ (clotrimazole හෝ econazole). ගර්භණී කාලයේ ඔරල් azoles (උදා: fluconazole) පොදුවේ වළක්වනු ලැබේ. රෝග ලක්ෂණ: කැක්කුම, වේදනා මුත්‍රා කිරීමේදී, දුර්ගන්ධය - පරීක්ෂණයකට යවන්න. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ දරුවාට අහිතකර ඔසු මොනවාද?",
        "වළක්වන්න: ACE inhibitors (enalapril, captopril), ARBs (losartan), statins, NSAIDs (පසු ත්‍රෛමාසිකයේ), warfarin, retinoids (Vit A), ටෙට්‍රාසයික්ලින්, ergometrine (severe pre-eclampsia හි). සැබෑ අවශ්‍ය ඔසු දොස්තර සමඟ සාකච්ඡා. මූලාශ්‍රය: MOH 2013 / RCOG."
    ),
    (
        "Rh-නෙගටිව් මව සති 28ක දරුවා පුළුවන් කරයි. ඊළඟට මොකද?",
        "Anti-D Ig 1500 IU IM 28-30 සතිවලදී (single dose) හෝ 500 IU 28 සහ 34 සතිවලදී (two-dose). Sensitising events (ලේ වැගිරීම, ECV, miscarriage, amniocentesis, abdominal trauma) ඕනෑම අවස්ථාවකදී එකතු වශයෙන්. ප්‍රසූතියෙන් පසු දරුවා Rh+ වුවොත් පැය 72ක් ඇතුළත. මූලාශ්‍රය: RCOG GTG 22."
    ),
    # --- Eclampsia / Severe ---
    (
        "ගර්භණී කාන්තාවක් වැටී කැක්කුමක් (seizure) ඇතිවුවොත් මොකද කරන්න?",
        "Eclampsia - හදිසි. (1) පැත්තකට හරවන්න (වම් පැත්ත). (2) වාතය මාර්ගය පිරිසිදු කරන්න, O2 8-10 L/min. (3) තුවාල වළක්වන්න. (4) IV access - bloods FBC/LFT/U&E/coagulation/cross-match. (5) MgSO4 4g IV 10 මිනිත්තුවකින් loading, ඉන්පසු 1g/පැයට infusion. (6) BP <160/110 - labetalol/hydralazine. (7) Foley catheter, ද්‍රව 80ml/පැයට සීමා. (8) ස්ථාවර කර දරු ප්‍රසූතිය. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "MgSO4 (magnesium sulphate) භාවිතා කරන විට මොකවද බලන්න ඕනේ?",
        "පැය හැම මිනිත්තු 30කටම මතක තබා ගන්න: (1) මුත්‍රා පිටවීම ≥30ml/පැය. (2) ශ්වසනය ≥16/min. (3) O2 saturation ≥90%. (4) Patellar (දන්) reflex. RR<12, reflex නැති නම්, oliguria - MgSO4 නවත්වන්න. Toxicity නම් antidote: Calcium gluconate 1g IV (10ml 10%). මූලාශ්‍රය: MOH 2013."
    ),
    # --- Pre-existing diabetes ---
    (
        "Type 1 diabetes ඇති කාන්තාවක් ගර්භණී වීමට පෙර HbA1c ඉලක්කය?",
        "HbA1c <48 mmol/mol (6.5%) ගර්භණී ලබා ගැනීමට පෙර. 86 mmol/mol (10%) ට වැඩි නම් ඔසු සාර්ථක වන තෙක් ගර්භණී වෙන්න ශක්තිමත් ලෙස වළක්වන්න (congenital malformation අවදානම ඉහළයි). ෆෝලික් අම්ලය 5mg දිනපතා සති 12 දක්වා. මූලාශ්‍රය: NICE NG3."
    ),
    (
        "Type 1/2 diabetes ඇති මව සඳහා දරු ප්‍රසූතිය කවදාද?",
        "Elective birth induction (හෝ අවශ්‍ය නම් CS) සති 37+0 සිට 38+6 අතර. Metabolic හෝ ක්ෂේත්‍ර/ෆීටල් සංකුලතා නම් ඊටත් කලින්. GDM (සංකූල නැති): සති 40+6 කරන්නේ නැත. මූලාශ්‍රය: NICE NG3."
    ),
    (
        "ප්‍රසූතියේදී දියවැඩි මව සඳහා ග්ලූකෝස් ඉලක්කය?",
        "කැපිලරි ග්ලූකෝස් 4-7 mmol/L (72-126 mg/dL) අතර. පැයකට වරක් මැනන්න. Partogram හි සටහන් කරන්න. ග්ලූකෝස් අගය මෙම අතර නොමැති නම් - dextrose-insulin infusion. T1DM නම් labour ආරම්භයේ සිට infusion සලකා බලන්න. මූලාශ්‍රය: NICE NG3."
    ),
    # --- Labour ---
    (
        "ශ්‍රමයේ ක්‍රියාකාරී අවධියේ delayed progress කොච්චරද?",
        "Active first stage: cervical dilatation < 2cm 4 පැයක දී. නැතහොත් කලින් සාර්ථකව සාර්ථක වූ කාන්තාවකගේ ප්‍රගතිය වේගය අඩුවීම. Senior medical officer විසින් සමාලෝචනය - contractions, descent, position, obstruction (caput, moulding), fetal condition පරීක්ෂා. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "ශ්‍රමයේදී කන්නේ බොන්නේ මොනවාද කරන්න පුළුවන්?",
        "පැහැදිලි ද්‍රව (පැලෑටි දොසු, kiri leaves, isotonic) - සියලුම ශ්‍රමයේ. ලාටන්ට් අවධියේ සැහැල්ලු ආහාර (බිස්කට්, පල) පිළිගත හැක. Active අවධියේ ඝන ආහාර වළක්වන්න - GA අවශ්‍ය වුවොත් වමන අවදානම. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "Routine episiotomy කරන්න ඕනේද?",
        "නැත. ස්වාභාවික දරු ප්‍රසූතියේදී සකස් කරන episiotomy නොකරන්න. Selective: instrumental delivery, fetal compromise, imminent severe tear අවස්ථාවලදී පමණක්. Mediolateral කෝණ 45-60° දකුණට, fourchette සිට, ඔටුණු වෙලාවේදී, 1% lignocaine 20ml යටතේ. මූලාශ්‍රය: MOH 2013."
    ),
    # --- Breastfeeding & newborn ---
    (
        "මව්කිරි පෝෂණය ආරම්භ කරන්නේ කවදාද?",
        "දරු ප්‍රසූතියෙන් මිනිත්තු 30ක් ඇතුළත (ආදර්ශය: පැය 1 ඇතුළත). දරුවා මවගේ බඩ මත තැබුවාට පසු, වියළා, skin-to-skin, ඉන්පසු කිරි කාටරයේ දේ. දියවැඩි මව්වරුන්ගේ දරුවන් - විශේෂයෙන් hypoglycaemia වැළැක්වීමට. මූලාශ්‍රය: MOH 2013."
    ),
    # --- Breech & malposition ---
    (
        "සති 36ට පසු දරුවා පතල්පත්කොට හිස් වෙනුවට - මොකද කරන්න?",
        "(1) USS නිවැරදි කිරීම. (2) ECV (external cephalic version) ගැන කතා කිරීම - 50-60% සාර්ථකත්ව (multipara වැඩි). (3) සති 36-37දී ECV පිරිනමන්න. ECV contraindications: placenta praevia, ROM, abnormal CTG, multiple, recent APH, scarred uterus. (4) ECV සාර්ථක නැතහොත් - planned CS හෝ vaginal breech (CS වඩාත් යෝග්‍ය). මූලාශ්‍රය: RCOG GTG 20a/b."
    ),
    # --- Twin pregnancy ---
    (
        "Twin ගර්භණී කාලයේ වෙනස් සත්කාර මොනවාද?",
        "(1) Chorionicity සති 11-13+6 දී USS මගින්. (2) DCDA: සති 20 සිට හැම සති 4ක්. MCDA: සති 16 සිට හැම සති 2 (TTTS). MCMA: සති 24 සිට හැම සති. (3) Aspirin 75-150mg සති 12 සිට. (4) Iron + folate. (5) ප්‍රසූතිය: DCDA 37+0-37+6, MCDA 36+0-36+6, MCMA 32-34 CS. මූලාශ්‍රය: NICE NG137."
    ),
    # --- Dengue ---
    (
        "ශ්‍රී ලංකාවේ ගර්භණී කාන්තාවක් dengue වැළැඳුණොත් සමාජ සැලකිලි?",
        "ශ්‍රී ලංකාවේ dengue PPH අවදානම් කරුණක්. (1) Febrile අවධියේ දිනපතා FBC - thrombocytopenia, haemoconcentration. (2) DHF අනතුරු ලකුණු - බඩේ දරුණු වේදනාව, අවික්‍රමශීලී වමනය, restlessness, ලේ වැගිරීම. (3) ද්‍රව සැලකිලිමත්ව - over/under resuscitation වළක්වන්න. (4) Shock අවධියේ ප්‍රසූතිය අන්තරායයි - හැකි නම් කල් දමන්න. (5) Cross-match ලේ කලින්. මූලාශ්‍රය: Sri Lanka MOH Dengue."
    ),
    (
        "ශ්‍රී ලංකාවේ තැලසීමියා පරීක්ෂණ මව්වරුන්ට වැදගත්ද?",
        "ඔව්. ශ්‍රී ලංකාවේ thalassaemia ව්‍යාප්තිය ඉහළයි (~2% beta-thalassaemia trait). සියලුම ගර්භණී කාන්තාවන්ට පරිඝණනයේදී FBC + Hb electrophoresis (MCV/MCH අඩු හෝ පවුල් ඉතිහාසය ඇත්නම්). මව carrier නම් සහකරු පරීක්ෂා. දෙදෙනාම carrier නම් prenatal diagnosis. මූලාශ්‍රය: Sri Lanka National Thalassaemia."
    ),
    # --- Newborn warning signs ---
    (
        "අලුත උපන් දරුවාගේ අනතුරු ලකුණු මොනවාද?",
        "වහාම සැකකරන්න: (1) කිරි පානය නොකරයි / මව්කිරි පානයට අසමර්ථයි. (2) අධිකව හිස් පැද්දේ / දෙයි. (3) උෂ්ණත්වය ඉහළ (>38°C) හෝ පහළ (<35.5°C). (4) කහ පැහැ පැය 24ක් ඇතුළත. (5) ශ්වසනය වේගවත්/දුෂ්කර. (6) බර පහත වැටීම >7% පළමු සති 1 තුළ. (7) Convulsion. (8) බෙල්ල / කරපිට වයසට අසාමාන්‍ය ලෙස පවතී. රෝහලට යන්න. මූලාශ්‍රය: Sri Lanka MOH Newborn Care."
    ),
    # --- Postnatal ---
    (
        "ප්‍රසූතියෙන් පසු ලේ ගැලීම සති ගණනක් දිගටම පවතී. සාමාන්‍යද?",
        "Lochia (postpartum bleeding) සාමාන්‍ය - පළමු දින 3-4 රතු (lochia rubra), ඉන්පසු දෙහි පැහැ (lochia serosa), ඉන්පසු සුදු/කහ (lochia alba) සති 6 දක්වා. ඕනෑම අවස්ථාවකදී දරුණු ලේ ගැලීම, ලොකු ලේ පොකුරු, දුර්ගන්ධය, උණ - වහාම පත්‍ය. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "ප්‍රසූතියෙන් පසු බර අඩු කරගැනීමට ආහාර වේලක්ද ඕනේ?",
        "මව්කිරි පෝෂණය බර අඩු වීමට උපකාර කරයි. දිනකට අතිරේක 500 kcal අවශ්‍යයි. සමබර ආහාර, ප්‍රෝටීන් (මාළු, බිත්තර, parippu), කොළ එළවළු, පල. දරුණු කැලරි සීමා කිරීම මව්කිරි පෝෂණයට බාධාකර. දියවැඩි මව්වරුන් DMPA contraception (බර වැඩිවීම) වළක්වන්න. මූලාශ්‍රය: Sri Lanka FHB."
    ),
    # --- HIV / infections ---
    (
        "PMTCT (HIV) ශ්‍රී ලංකාවේ?",
        "පරිඝණනයේදී සියලුම ගර්භණී කාන්තාවන්ට HIV පරීක්ෂණය (informed consent). HIV+ නම් - ART එකම ආරම්භ කරන්න. ප්‍රසූතියේ ක්‍රමය විශේෂඥයා සමඟ සාකච්ඡා (vaginal vs CS). දරුවාට ART prophylaxis සහ formula feeding (BFHI Sri Lanka guidelines). මූලාශ්‍රය: STD/AIDS Control Programme."
    ),
    (
        "ශ්‍රී ලංකාවේ GBS පරීක්ෂණ ප්‍රතිපත්තිය?",
        "Universal GBS screening නැත. Risk-based: පෙර දරුවාට GBS, මේ ගර්භණී කාලයේ GBS bacteriuria, preterm <37 සති, ROM >18 පැය, intrapartum fever ≥38°C. IV penicillin intrapartum. මූලාශ්‍රය: RCOG GTG 36."
    ),
    # --- General severe risk ---
    (
        "PPH වළක්වන්න සහ වහාම මෙන්ම ප්‍රසූතියට පෙර කරන්න ඕනේ දේවල්?",
        "(1) ANC හි අවදානම් කරුණු හඳුනා ගන්න: grand multipara, පෙර PPH, fibroids, anaemia, anticoagulant, obesity, pre-eclampsia, twins, polyhydramnios, large baby, dengue. (2) Hb optimize කරන්න. (3) අවදානම් කාන්තාවන්ට specialist unit. (4) IV access 14-16G කලින්. (5) Blood group, cross-match තබා ගන්න. (6) Active management 3rd stage සියලුම මව්වරුන්ට. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "හදිසි ආපදාවට පෙර කලට පෙර ප්‍රවාහනයේ සැලකිලිමත් කොච්චරද?",
        "Severe hypertension/eclampsia transfer: (1) IV access. (2) Oral nifedipine 10mg හෝ IV labetalol (BP<160/110). (3) MgSO4 4g IV/IM loading. (4) Foley catheter. (5) Receiving hospital call. (6) Staff member emergency drugs සමඟ. PPH transfer: warm IV fluids, tranexamic acid 1g IV, balloon tamponade if available. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "ගර්භණී කාලයේ වැඩිකරන්න සහ වළක්වන්න ආහාර මොනවාද?",
        "වැඩි කරන්න: කොළ එළවළු (folate), රතු මස්/මාළු (haem iron), විටමින් C පල (orange, ඉඳු), කිරි/yoghurt (calcium), parippu/දුන්න/නිම් (protein). වළක්වන්න: අමු මස්/මාළු (toxoplasmosis), unpasteurised කිරි, අතිමාත්‍ර වයස ලෙස මුද්ද (vitamin A), කෝපි/තේ (iron absorption අඩු), ඇල්කොහොල්. මූලාශ්‍රය: Sri Lanka FHB Maternal Nutrition."
    ),
    # --- More clinical vignettes ---
    (
        "ගර්භණී වයස සති 30. BP 145/92. ප්‍රෝටීන් මුත්‍රාවේ නැත. ලකුණු කිසිවක් නැත. මොකද කරන්නේ?",
        "මධ්‍යම අවදානම් - gestational hypertension. (1) වම් පැත්ත සැතපීමෙන් පසු BP නැවත මැනන්න. (2) Dipstick මුත්‍රා ප්‍රෝටීන් සඳහා. (3) 140-159/90-109 සහ ප්‍රෝටීන් නැත, ලකුණු නැත නම් විශේෂඥ සායනයට යොමු කරන්න. (4) සතිකට BP සහ මුත්‍රා පරීක්ෂණ. (5) අනතුරු ලකුණු දරුවාගේ සෙලවීම අඩුවීම, හිසරදය, දර්ශන වෙනස්, බඩේ වේදනාව මව හදුනන්න උගන්වන්න. මූලාශ්‍රය: NICE NG133 / MOH 2013."
    ),
    (
        "ගර්භණී කාන්තාවක් සති 36ක යි, දරුවාගේ චලනය නැහැ පැය 14ක්. මොකද කරන්නේ?",
        "හදිසි. ඊයේ රාත්‍රී සිට චලනය නැත නම් අත්‍යවශ්‍ය. (1) Fetal heart auscultate. (2) CTG අවම පැය 1ක්. (3) USS - amniotic fluid, growth, biophysical profile. (4) අසාමාන්‍ය නම් - delivery තීරණය senior විසින්. (5) සාමාන්‍ය නම් - 24 පැය ඇතුළත follow-up සහ වර්ග හැදී වැඩි ආලෝචනය. මූලාශ්‍රය: RCOG GTG 57."
    ),
    (
        "ගර්භණී වයස සති 24. Symphysis fundal height 19cm. මොකද?",
        "Small for gestational age සැකය. SFH 24 සතියට ±3 cm (21-27cm) අතර සාමාන්‍ය. 19cm ඉතා අඩු. (1) USS කරන්න - growth, amniotic fluid index. (2) Risk factors පරීක්ෂා - hypertension, smoking, infections. (3) IUGR තහවුරු වුවොත් සති 2කට වරක් growth scans + Doppler. (4) Severe IUGR + abnormal Doppler නම් hospital admission. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ගර්භණී වයස සති 38, ශුද්ධ දියර වැගිරෙයි. වේදනා නැත. මොකද කරන්නේ?",
        "Term PROM (premature rupture of membranes). (1) Speculum පරීක්ෂණය - liquor confirmation. (2) Digital VE වළක්වන්න - infection අවදානම අඩු කරයි. (3) Vital signs, fetal heart, මව්ගේ උෂ්ණත්වය. (4) Watchful expectant 24 පැයකට. (5) Spontaneous labour නැතහොත් induce කරන්න - oxytocin හෝ prostaglandin. (6) Chorioamnionitis ලකුණු - උණ, මන්ද ගඳ - ඇත්නම් වහාම delivery. මූලාශ්‍රය: MOH 2013 §B.4.2."
    ),
    (
        "Preterm PROM 32 සතියේ. මොකද කරන්නේ?",
        "PPROM. (1) Speculum confirm. (2) Digital VE වළක්වන්න. (3) Vaginal/cervical swab. (4) ඇන්ටිබයෝටික - erythromycin 250mg qid 10 දින (latency දිගු කරයි). (5) Corticosteroids - dexamethasone 6mg IM q12h × 4 doses (fetal lung). (6) <32 weeks immediate delivery නම් MgSO4 (neuroprotection). (7) 34 සතියට පෙර අනෙක් සැක නැත්නම් expectant management. (8) Delivery 34-37 සතියේදී. මූලාශ්‍රය: MOH 2013 §B.4.3."
    ),
    (
        "ගර්භණී කාන්තාවක් (G2P1) BP 168/110, severe headache, visual blurring සමඟ. මොකද කරන්නේ?",
        "හදිසි - severe pre-eclampsia / impending eclampsia. (1) IV access. (2) MgSO4 4g IV 10 මිනිත්තුවකින් loading + 1g/පැයට infusion. (3) Labetalol 20mg IV (BP <160/110), repeat 40mg, 80mg max. නැතිනම් oral nifedipine 10mg q20min max 40mg. (4) Foley catheter, fluids 80ml/පැය. (5) Bloods - FBC, LFT, U&E, coagulation. (6) Senior obstetrician + plan delivery once stable. (7) Magnesium toxicity බලන්න - RR, reflexes, urine. මූලාශ්‍රය: MOH 2013 §H.6.2."
    ),
    # --- Postnatal more detailed ---
    (
        "ප්‍රසූතියෙන් පසු මව සහ දරුවාගේ පරීක්ෂණ කවදාද?",
        "Postnatal visits Sri Lanka: (1) Hospital discharge පෙර වෛද්‍ය පරීක්ෂණය. (2) PHM home visit දින 1-3. (3) PHM follow-up දින 7-10. (4) 6 සති postnatal check (BP, contraception, mood). (5) දරුවා - immunisations, weight gain බලන්න. දරුවා කහ පැහැ පැය 24 ඉස්සෙල්ලා, මව්කිරි පානය නැතහොත් - වහාම සැකකරන්න. මූලාශ්‍රය: Sri Lanka FHB Postnatal."
    ),
    (
        "ප්‍රසූතියෙන් පසු මන්ද්‍රතාව (postnatal depression) ලකුණු මොනවාද?",
        "Postnatal blues (දින 3-10) සහ depression වෙනස. Depression ලකුණු: 2 සතියට වඩා දුක, අතාර්ථ ලීලාව, නින්ද/අඅංගය, බර වෙනස, දරුවාට අතරිංගතාව, මරණ සිතුවිලි. Mother-baby bonding අඩුවීම. EPDS screening 6 සති postnatal visit-දී. Severe නම් (suicidal ideation, psychosis) - වහාම mental health referral. මූලාශ්‍රය: NICE CG192 / FHB."
    ),
    (
        "ප්‍රසූතියෙන් පසු DVT අවදානම් මොනවාද?",
        "VTE prophylaxis: high-risk (CS, BMI≥30, age>35, parity≥3, smoker, varicose, twins, pre-eclampsia, immobility) - LMWH (enoxaparin 40mg SC daily) 10 දින හෝ 6 සති. ඕනෑම මව්වරුන් 6 සති ඉඳීම අඩු, hydration. Acute DVT ලකුණු - calf pain, swelling, redness - වහාම Doppler. Pulmonary embolism (chest pain, breathlessness) - emergency. මූලාශ්‍රය: RCOG GTG 37a."
    ),
    # --- Family planning ---
    (
        "ප්‍රසූතියෙන් පසු කවදා නැවත ගර්භණී වෙන්න පුළුවන්?",
        "Birth spacing: WHO recommends අවම 24 මාසයක (අවුරුදු 2) interpregnancy interval (last birth සිට next conception). 18 මාසයට කලින් ගර්භණී වුවොත් - preterm, low birth weight, maternal anaemia අවදානම. Breastfeeding (LAM) පළමු 6 මාසට - exclusive නම් effective. ඉන් පසු contraception. CS න් පසු 18-24 මාස spacing. මූලාශ්‍රය: WHO Birth Spacing / Sri Lanka FHB."
    ),
    (
        "ප්‍රසූතියෙන් පසු contraception options?",
        "Sri Lanka options: (1) LAM - exclusive breastfeeding, amenorrhoea, <6 months. (2) Mini-pill (POP) - safe in breastfeeding. (3) DMPA (Depo-Provera) - safe but බර වැඩිවීම. (4) IUD - postpartum insertion <48h හෝ 4 සති පසු. (5) Implant (Implanon) - safe. (6) COCP - 6 මාසයට පෙර breastfeeding ඇත්නම් වළක්වන්න. (7) Tubectomy - permanent. (8) Condoms. නැති: GDM/T2DM ඇත්නම් DMPA වළක්වන්න (බර වැඩිවීම). මූලාශ්‍රය: Sri Lanka FHB FP."
    ),
    # --- Newborn care ---
    (
        "අලුත උපන් දරුවාට මව්කිරි එනකම් මොකද කරන්නේ?",
        "පළමු දින 2-3 දී colostrum (පළමු කිරි) - බෝතල කරන්න එපා. දරුවාට පැයකට වරක් මව්කිරි දෙන්න (8-12 වර දිනකට). Demand-led. Formula විකල්පයක් නොවේ - milk supply අඩු කරයි. Wet nappies පැහැදිලි දිනකට 6+ සහ green/yellow stool දිනකට 3+ adequate intake. ශරීර බර 7-10% දින 4-5දී කුඩා සෘජු වැටීම සාමාන්‍ය. මූලාශ්‍රය: BFHI Sri Lanka."
    ),
    (
        "අලුත උපන් දරුවාට කහ පැහැ ඇතිවුවොත්?",
        "Physiological jaundice: දින 2-3 ආරම්භ, දින 5-7 ඉහළම, දින 10-14 අඩු වේ. රෝග ලක්ෂණ: ඇස් සහ සමේ කහ, මෘදු කෑම. Pathological warning: <24 පැය ආරම්භ, 14 දිනට වඩා වැඩි, palms/soles විසරිත, pale stool, dark urine. Phototherapy threshold මව බර, ගර්භණී වයස, දින අනුව. ABO/Rh incompatibility test. මූලාශ්‍රය: Sri Lanka MOH Newborn."
    ),
    (
        "අලුත උපන් දරුවාට ලොව BCG, Hep B දෙන්නේ කවදාද?",
        "Sri Lanka EPI: BCG + Hepatitis B උපතේදී (within 24h). 2 මාස: Pentavalent (DTP+HepB+Hib), OPV, IPV. 4 මාස, 6 මාස booster. 9 මාස MR (measles-rubella). 18 මාස DPT booster, MR. 3 අවුරුදු MR2. 5 අවුරුදු DT, OPV. 11 අවුරුදු adult Td. Premature dose schedule adjustments PHM consultation. මූලාශ්‍රය: Sri Lanka EPI."
    ),
    # --- Common mother questions ---
    (
        "ගර්භණී කාලයේ ව්‍යායාම කරන්න පුළුවන්ද?",
        "ඔව්. මධ්‍යම ව්‍යායාම නිර්දේශ - දිනකට 30 මිනිත්තු, සතියට 5-7 දින. ඇවිදීම, swimming, yoga (prenatal), Kegel exercises. වළක්වන්න - contact sports (basketball, soccer), abdominal injury අවදානම් (horse riding), scuba diving, hot tubs. රෝග ලක්ෂණ - ව්‍යායාම නවත්වන්න: chest pain, dizziness, fluid leak, contractions, vaginal bleeding. මූලාශ්‍රය: ACOG / NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ ලිංගික සම්බන්ධතා කරන්න පුළුවන්ද?",
        "හැකි, low-risk pregnancy නම් මුළු ගර්භණී කාලය. වළක්වන්න: placenta praevia, threatened miscarriage, preterm labour අවදානම, ROM, ලේ වැගිරීම. තුන්වෙනි ත්‍රෛමාසිකයේ පැත්ත (side-lying) යෝග්‍ය. Cramping, bleeding ඇත්නම් වහාම සායනය. මූලාශ්‍රය: ACOG / NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ දත් වෛද්‍යවරයා බැලෙන්න පුළුවන්ද?",
        "ඔව්. දන්ත ආරක්ෂාව වැදගත් - gingivitis, dental caries ගර්භණී කාලයේ වැඩි. Routine cleaning ආරක්ෂිත. Local anaesthesia (lignocaine) ආරක්ෂිත. X-rays - lead apron උපකරණයක් යටතේ. දෙවෙනි ත්‍රෛමාසිකය වඩාත් ආරක්ෂිත. දරුණු pain killer වළක්වන්න - paracetamol පමණක්. NSAIDs (ibuprofen) පසු ගර්භණී කාලයේ වළක්වන්න. මූලාශ්‍රය: ACOG."
    ),
    (
        "ගර්භණී කාලයේ ගමන් කිරීම - ආරක්ෂිතද?",
        "Low-risk pregnancy නම් සති 36 දක්වා flight ආරක්ෂිත (airlines policy වෙනස් වේ). Long flights: DVT අවදානම - hydration, ඇවිදීම, compression stockings, aisle seat. Vaccination: Yellow fever, Typhoid (live) වළක්වන්න. Malaria, Zika ප්‍රදේශ - avoid. Health insurance pregnancy කවර කරයිද බලන්න. ANC schedule preserve කරන්න. මූලාශ්‍රය: ACOG / RCOG."
    ),
    # --- Common concerns ---
    (
        "ගර්භණී කාලයේ ඉදුරා දිය වැගිරෙන්න පුළුවන්ද?",
        "Discharge වර්ග: (1) Leucorrhoea - සුදු/පැහැදිලි, ගඳ නැති - සාමාන්‍ය. (2) Candidiasis - ඝන, සුදු, කැක්කුම - clotrimazole vaginal. (3) BV - thin, grey, fishy odour - metronidazole. (4) Amniotic fluid - watery, gush, continuous - PROM සැකකරන්න, වහාම සායනය. (5) Mucus plug - thick, blood-tinged - labour ආරම්භ වීමේ ලකුණ. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ පපුවේ පැන්නැම් ඇතිවුවොත්?",
        "Heartburn ගර්භණී කාලයේ සාමාන්‍ය - progesterone හේතුව. ක්‍රියා: (1) කුඩා ආහාර වාර වැඩි කරන්න. (2) ආහාරයට පසු වහාම ස්පින් සැතපීම වළක්වන්න. (3) Spicy, fatty, citrus වළක්වන්න. (4) උගුර ඉහළට ඇතිරිමෙන් සැතපීම. (5) Antacid (calcium-based) trial. (6) Severe නම් - alginate (Gaviscon), H2 blockers (ranitidine), PPI (omeprazole) safe. මූලාශ්‍රය: NICE NG201."
    ),
    (
        "ගර්භණී කාලයේ පාද ඉදිමීම සාමාන්‍යද?",
        "මෘදු pedal oedema (පාද සහ ankles) පසු ගර්භණී කාලයේ සාමාන්‍ය - venous compression හේතුව. ඉහළට පාද තබන්න, compression stockings, hydration, salt අඩු. අනතුරු ලකුණු: මුහුණ + අත් ඉදිමීම, ඒකපාර්ශවික ඉදිමීම (DVT), වහාම ආරම්භ වූ ඉදිමීම + headache + visual changes = pre-eclampsia - වහාම BP මැනන්න. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "ගර්භණී කාලයේ සෙම්ප්‍රතිශ්‍යාව ආශ්වාද කරන්න පුළුවන්ද?",
        "ඔව්. Paracetamol 500-1000mg q6h safe. වළක්වන්න: aspirin (3rd trimester), ibuprofen (3rd trimester), pseudoephedrine. Nasal congestion: saline nasal spray, steam, humidifier. Cough: warm fluids, honey + lemon, paracetamol. ඉල්ලුමක්: උණ >38°C 3 දින පවතී, breathlessness, chest pain, productive cough sputum colored, ear pain - වහාම සායනය. ගර්භණී කාලයේ COVID, influenza - severe. මූලාශ්‍රය: BUMPS UK."
    ),
    # --- Specific drugs ---
    (
        "Paracetamol ගර්භණී කාලයේ ආරක්ෂිතද?",
        "ඔව්. Paracetamol (acetaminophen) ගර්භණී කාලයේ first-line analgesic + antipyretic. Dose 500-1000mg q4-6h, max 4g/day. දිගු කාලයක් අධික dose භාවිතය වළක්වන්න. Ibuprofen 32 සතියට පසු වළක්වන්න (premature closure of ductus arteriosus, oligohydramnios). Aspirin (low-dose 75-150mg) pre-eclampsia prevention safe. Opioids - constipation, neonatal withdrawal - පමණක් සැබෑ අවශ්‍ය. මූලාශ්‍රය: BUMPS / RCOG."
    ),
    (
        "Antibiotic ආරක්ෂිත මොනවාද?",
        "ආරක්ෂිත: penicillins (amoxicillin, flucloxacillin), cephalosporins (cefuroxime, ceftriaxone), erythromycin (estolate වළක්වන්න), azithromycin, clindamycin, nitrofurantoin (3rd trimester වළක්වන්න), metronidazole (1st trimester තහනම ඉවත් කර ඇත). වළක්වන්න: tetracyclines (teeth, bone), fluoroquinolones (ciprofloxacin), trimethoprim (1st trimester), sulphonamides (3rd trimester - kernicterus). මූලාශ්‍රය: BNF / NICE."
    ),
    # --- Labour signs ---
    (
        "ශ්‍රමයේ ආරම්භක ලකුණු මොනවාද?",
        "ශ්‍රමය ආරම්භ ලකුණු: (1) Regular contractions - වැඩි වන frequency සහ intensity. (2) 'Show' - mucus plug discharge, ඇතැම් විට ලේ අඩු සුළු. (3) Water break (ROM) - clear, watery liquor gush හෝ trickle. (4) Lower back pain, pelvic pressure. (5) Cervical change (VE මගින් - effacement, dilatation 4cm). Reasons සායනයට යන්න: contractions 5 මිනිත්තු වරකට, ලේ වැගිරීම, dilation සහ ROM. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "'Show' (පොකරා) ලේ වැගිරීම සාමාන්‍යද?",
        "Bloody show - cervical effacement + dilatation හේතුව. සුළු pink/red discharge, mucus සමඟ, ශ්‍රමය 24-72 පැය තුළ ආරම්භ වීමේ ලකුණක්. සාමාන්‍ය, භීතියට හේතුවක් නැත. නමුත් heavy bleeding, clots, persistent flow - placental abruption හෝ praevia සැක - වහාම සායනය. මූලාශ්‍රය: MOH 2013."
    ),
    # --- Pre-existing conditions ---
    (
        "Asthma ඇති ගර්භණී කාන්තාවට මොකද කරන්නේ?",
        "Asthma ඇති මව්වරුන් 1/3 worse, 1/3 better, 1/3 same. Controllers (inhaled corticosteroids - budesonide) safe. Salbutamol safe. Severe attacks - hypoxia fetal compromise - aggressively treat. Avoid: aspirin (if aspirin-sensitive asthma), β-blockers (also avoid in HTN-asthma combo - use nifedipine/methyldopa). Magnesium sulphate safe. Labour - epidural OK, intramuscular ergometrine avoid. මූලාශ්‍රය: BTS / SIGN."
    ),
    (
        "Hypothyroidism ගර්භණී කාලයේ සත්කාරය?",
        "Hypothyroidism untreated - miscarriage, IUGR, pre-eclampsia, neonatal cognitive deficit අවදානම. Pre-conception thyroid optimised - TSH <2.5 mIU/L. ගර්භණී වුවොත් Levothyroxine වහාම 25-50% වැඩි කරන්න (need increases 30-50%). TSH 4-6 සතිකට වරක්. Iodine - adequate intake (250mcg/day). Iodised salt + supplement if needed. මූලාශ්‍රය: ATA Pregnancy Guidelines."
    ),
    (
        "Epilepsy ගර්භණී කාලයේ සත්කාරය?",
        "Pre-conception planning - drug review (sodium valproate teratogenic - avoid; lamotrigine, levetiracetam preferred). Folic acid 5mg daily pre-conception + first trimester. Drugs continue - seizures harmful to fetus. Vitamin K 10mg PO daily last 4 weeks (some anti-epileptics enzyme inducers). Newborn vitamin K injection. Labour - seizure precautions. Breastfeeding OK with most AEDs. මූලාශ්‍රය: NICE CG137."
    ),
    # --- Practical guidance ---
    (
        "ANC සායනයේදී මව්වරුන්ට කියන්න ඕනේ ප්‍රධාන කරුණු මොනවාද?",
        "හැම ANC visit-දී: (1) අනතුරු ලකුණු recap - severe headache, vision, swelling face/hands, RUQ pain, bleeding, ROM, fetal movement, convulsions, severe vomiting, fever. (2) BP, weight, fundal height, urinalysis. (3) Iron, folic acid, calcium adherence. (4) Diet, exercise, no alcohol/smoking. (5) Birth preparedness - hospital, transport, money. (6) Family planning postpartum discussion (later visits). මූලාශ්‍රය: WHO ANC / Sri Lanka FHB."
    ),
    (
        "මව්වරුන්ට හදිසි අවස්ථාවක දී (emergency action plan) කොහොමද උගන්වන්නේ?",
        "Birth preparedness + complication readiness: (1) Where - delivery facility පෙර තෝරන්න. (2) Who - blood donor නෑදෑයා හඳුනා ගන්න. (3) Transport - ambulance number (1990 - Suwa Seriya), backup vehicle. (4) Money - emergency funds. (5) Birth companion - decide. (6) Items - clothes, documents, money packed by 36 weeks. (7) Danger signs - family දැනුම ලබා දෙන්න (not just mother). (8) PHM, MOH contact numbers. මූලාශ්‍රය: Sri Lanka MCH."
    ),
    (
        "PHM ලෙස මගේ වගකීම් මොනවාද?",
        "Sri Lanka PHM key duties: (1) Domiciliary care - antenatal home visits, postnatal home visits. (2) ANC clinic - vital signs, fundal height, education. (3) Risk identification - refer high-risk to MOH/specialist. (4) Iron, folic acid, calcium distribution. (5) Family planning counselling and method provision. (6) Newborn check, immunisation, growth monitoring. (7) Maternal nutrition education. (8) Birth preparedness counselling. (9) Postnatal mental health screening. (10) Health record (CHN form) maintenance. මූලාශ්‍රය: Sri Lanka FHB PHM."
    ),
    # --- Hypertension drug doses ---
    (
        "Labetalol oral dose pregnancy hypertension සඳහා?",
        "Oral labetalol: (a) Initial 100-200mg bd. (b) Increase by 100mg per dose every 2-3 days, max 800mg tds (2.4g/day). (c) Target BP 135/85. IV (severe HTN): 20mg over 2 min, recheck 10 min; if BP high - 40mg, then 80mg (max single doses). Or infusion 40mg/hr, double every 30 min up to 160mg/hr. Asthma වළක්වන්න. මූලාශ්‍රය: NICE NG133 / MOH 2013."
    ),
    (
        "Methyldopa dose pregnancy?",
        "Methyldopa oral: 250-500mg tds (max 3g/day). Onset 4-6 hours - acute control නැත. Side effects: drowsiness, dry mouth, postural hypotension, depression. Postnatal දින 2 ඇතුළත නවත්වන්න (depression risk). Third-line choice (after labetalol, nifedipine). මූලාශ්‍රය: NICE NG133."
    ),
    (
        "Nifedipine oral dose pregnancy?",
        "Nifedipine oral: (a) Modified-release tablets 20-30mg bd-tds, max 90mg/day. (b) Acute severe HTN: immediate-release 10mg stat (BP <180/110 සහ ලකුණු රහිත), q20min max 40mg total. Note: some brands contraindicate pregnancy use - check SPC. Side effects: headache, flushing, oedema. මූලාශ්‍රය: NICE NG133."
    ),
    # --- Special situations ---
    (
        "Twin pregnancy delivery - vaginal හෝ CS?",
        "DCDA twins uncomplicated - vaginal birth pure cephalic-cephalic OK; first breech CS නිර්දේශ. MCDA twins - vaginal birth OK if cephalic-cephalic. MCMA twins - CS නිර්දේශ (cord entanglement). Consider CS: previous CS, malpresentation first twin, IUGR, growth discordance, monoamniotic. Continuous CTG twin labour. Second twin delivery within 30 min of first. Active management 3rd stage - increased PPH risk. මූලාශ්‍රය: RCOG / NICE NG137."
    ),
    (
        "Cord prolapse - immediate action?",
        "හදිසි - වහාම C-section preparation. (1) Push presenting part off cord - hand in vagina elevating fetal head. (2) Position: knee-chest position හෝ Trendelenburg / left lateral with hips elevated. (3) Foley catheter - 500ml saline bladder fill to elevate presenting part. (4) Oxytocin නවත්වන්න. (5) Tocolysis - terbutaline 250mcg SC. (6) Theatre emergency - CS if not immediately deliverable vaginally. (7) Don't remove hand until baby delivered. මූලාශ්‍රය: RCOG GTG 50."
    ),
    (
        "Shoulder dystocia - HELPERR mnemonic?",
        "Shoulder dystocia management - HELPERR: H - Help (call senior, paeds, anaesthetist). E - Evaluate for episiotomy. L - Legs - McRoberts manoeuvre (knees to chest, flexion-abduction). P - Suprapubic pressure (Mazzanti or Rubin I). E - Enter - internal manoeuvres (Rubin II, Woods screw, reverse Woods). R - Remove posterior arm. R - Roll over (all-fours, Gaskin manoeuvre). Last resort - Zavanelli (cephalic replacement, CS), symphysiotomy. AVOID fundal pressure. මූලාශ්‍රය: RCOG GTG 42."
    ),
    # --- Vaccinations ---
    (
        "ගර්භණී කාලයේ COVID vaccination ආරක්ෂිතද?",
        "ඔව්. WHO/RCOG/ACOG recommend COVID vaccination ගර්භණී කාලයේ - mRNA preferred. Trimester ඕනෑ එකේදී දෙන්න පුළුවන්. Benefits: severe COVID, hospitalisation, ICU admission, preterm birth අවදානම අඩු කරයි. Booster doses also recommended. Influenza vaccine සහ Tdap (28-32 weeks) - safe and recommended. Live vaccines (MMR, varicella, yellow fever) වළක්වන්න. මූලාශ්‍රය: WHO / RCOG / CDC."
    ),
    # --- Documentation ---
    (
        "Pregnancy record (CHN form) - වැදගත් කරුණු?",
        "Sri Lanka CHN (Child Health Card) - mother retains, every visit update: (1) Demographics, parity, LMP, EDD. (2) Vital signs each visit. (3) Symphysis-fundal height, fetal heart. (4) Investigations + results. (5) Risk factors flagged. (6) Iron/folate adherence. (7) Immunisations. (8) Birth preparedness plan. (9) Postnatal contacts. (10) Newborn weight, immunisation. Mother attends ALL visits with card. Card lost - replacement immediate from MOH. මූලාශ්‍රය: Sri Lanka FHB."
    ),
    # --- Mental health / GBV ---
    (
        "ගර්භණී කාලයේ ගෘහස්ථ ප්‍රචණ්ඩත්වය (DV) - PHM දැකගත් වුවොත්?",
        "Pregnancy = DV onset/escalation peak. Private opportunity provide සහ direct ask කරන්න (HARK questions). Document carefully (legal protection). Safety plan - safe house, emergency contacts, escape kit. Refer: Mithuru Piyasa (govt centre), Women in Need (1938), 119 (police), social services. Antenatal increased visits, mental health screening. DV සහ PPH, preterm, mental illness, fetal injury සම්බන්ධයි. Confidentiality + woman's autonomy. මූලාශ්‍රය: WHO / Sri Lanka FHB."
    ),
    (
        "ගර්භණී කාලයේ stress සහ mental health සත්කාරය?",
        "ANC routine mental health screen: 4Q (Whooley + GAD-2). Risk factors: previous mental illness, single, young, GBV, no support, GDM/HTN, IUFD history. Mild: counselling, peer support, mindfulness. Moderate: CBT, group therapy. Severe: psychiatric referral, medication consideration (SSRIs - sertraline preferred breastfeeding). Suicidal ideation - urgent psychiatric, never leave alone. PHM 6-week postnatal EPDS screening. මූලාශ්‍රය: NICE CG192."
    ),
    # --- More vignettes ---
    (
        "ගර්භණී කාන්තාවක් රු. 25 BMI, age 41, first pregnancy. අවදානම් මොනවාද?",
        "Multiple moderate risk factors: nulliparity, age ≥40, BMI 25 (not high but combined). Risks: pre-eclampsia (start aspirin 75-150mg from 12 weeks), GDM (early OGTT consider), chromosomal abnormality (NIPT/combined test), stillbirth, IUGR (serial growth scans). Additional ANC visits. Birth - consider induction by 41 weeks. Continuous monitoring labour. මූලාශ්‍රය: NICE NG133, NG201."
    ),
    (
        "First pregnancy, BMI 36, gestation 12 weeks. ක්‍රියා?",
        "Obesity (BMI ≥30): (1) Aspirin 75-150mg from 12 weeks (PE prevention). (2) Folic acid 5mg daily (NTD increased risk). (3) Vitamin D supplementation. (4) GDM screen at 24-28 weeks (early if other risks). (5) Anomaly scan technical difficulties counsel. (6) Anaesthetic referral 3rd trimester. (7) Birth at consultant-led unit. (8) VTE assessment - LMWH antenatal if high risk. (9) Refer dietitian. (10) Postnatal weight management. මූලාශ්‍රය: RCOG / NICE."
    ),
    (
        "ගර්භණී කාන්තාවක් pre-existing HTN, captopril 25mg ගන්න. දැන් කරන්නේ?",
        "ACE inhibitor teratogenic - stop immediately, switch within 2 working days. Alternatives: (1) Labetalol (first choice). (2) Nifedipine. (3) Methyldopa. Target BP 135/85. Aspirin 75-150mg from 12 weeks (chronic HTN = high-risk for PE). PLGF testing 20-36+6 weeks if PE suspected. Increased ANC visits. Renal function baseline. Birth: typically 37-39 weeks unless BP ≥ 160/110 or fetal indication. මූලාශ්‍රය: NICE NG133."
    ),
    # --- More postnatal ---
    (
        "Mastitis - ක්‍රියා?",
        "Breast pain, redness, fever, flu-like symptoms - mastitis. (1) Continue breastfeeding (more frequent on affected side). (2) Effective milk removal - good latch, massage. (3) Warm compress before feeds, cold after. (4) Paracetamol/ibuprofen pain. (5) Rest, hydration. (6) Antibiotics if symptoms persist 12-24h, fever ≥38.5, severe - flucloxacillin 500mg qid 10-14 days (or erythromycin if penicillin-allergic). (7) Abscess (fluctuant mass) - USS, drainage. මූලාශ්‍රය: BFHI / RCOG."
    ),
    (
        "ප්‍රසූතියෙන් පසු urine leak වෙයි. සාමාන්‍යද?",
        "Postpartum stress urinary incontinence - pelvic floor injury හේතුව. 6 සති පමණ සාමාන්‍ය. ක්‍රියා: (1) Pelvic floor exercises (Kegel) - පැය හැම පැයකම 10 contractions × 10 seconds, 3 sets/day. (2) Bladder training. (3) 6 සති පසු - physiotherapy referral. (4) Severe (continuous leak, fistula) - urological referral. CS women too can have leak. Persistent >6 months - specialist evaluation. මූලාශ්‍රය: NICE."
    ),
    (
        "ප්‍රසූතියෙන් පසු constipation සහ haemorrhoids?",
        "Postpartum common - opioid analgesia, dehydration, fear of pain. ක්‍රියා: (1) Fluids 2-3L/day. (2) Fiber - papaya, fruits, vegetables. (3) Lactulose 10-15ml bd safe in breastfeeding. (4) Avoid straining - perineal pain worse. (5) Haemorrhoids - topical anaesthetic (lignocaine), warm sitz baths, witch hazel pads, ice packs. (6) Persistent (>6 weeks), bleeding heavy, prolapsed - surgical referral. මූලාශ්‍රය: NICE postnatal."
    ),
    # --- Triage decisions ---
    (
        "Mother calls in night: contractions 10 minutes apart, gestation 39 weeks. Advice?",
        "Latent phase likely. (1) Stay home if comfortable, rest, eat light, hydrate. (2) Come to hospital when: contractions 5 min apart for 1 hour AND lasting 60 sec each, OR ROM, OR bleeding more than show, OR reduced fetal movements, OR severe pain. (3) Always come if anxious or worried. (4) High risk (HTN, GDM, scar) - lower threshold to come in. (5) Bring CHN card, supplies. මූලාශ්‍රය: MOH 2013."
    ),
    (
        "PHM home visit: postnatal day 5, mother BP 155/100, severe headache. Action?",
        "හදිසි - postpartum pre-eclampsia (eclampsia 28 days postpartum possible). (1) BP recheck after 10 min rest. (2) Urine dipstick protein. (3) Symptoms: headache, vision, RUQ pain. (4) වහාම transport - hospital - ambulance call 1990. (5) Do NOT give methyldopa (depression). (6) Hospital: IV access, MgSO4 consideration, antihypertensives. (7) Bloods - FBC, LFT, U&E. Postnatal PE accounts for ~40% of severe maternal morbidity. මූලාශ්‍රය: NICE NG133 / MBRRACE."
    ),
    # --- Mother queries about app ---
    (
        "Amma Sewana app මොකද්ද?",
        "Amma Sewana = Sri Lanka PHM-සහාය AI app. (1) Offline operation - internet නැතිවද වැඩ කරයි, gemma-4 model දුරකථනයේ. (2) Sinhala, Tamil, English ආකාර. (3) Vitals interpretation - BP, Hb, FH ඇතුළත් කර risk level. (4) Danger signs reference. (5) Sri Lanka MOH 2013 + RCOG + NICE guidelines knowledge. (6) Not a replacement for medical doctor - decision support tool. (7) Patient data device හැර වෙනත් කිසිම තැනකට යවන්නේ නැත - privacy ආරක්ෂිතයි. මූලාශ්‍රය: Amma Sewana."
    ),
]

# ============================================================
# SECTION 14: TAMIL (தமிழ்) — Sri Lankan Tamil for PHMs and mothers
# Focused on critical content. Sources cross-verified with English originals.
# ============================================================

TAMIL_TA = [
    # --- Danger signs ---
    (
        "கர்ப்பிணித் தாயின் ஆபத்து அறிகுறிகள் என்னென்ன?",
        "உடனடியாக மருத்துவமனைக்குச் செல்லவும்: கடுமையான தலைவலி, பார்வை மங்கல் அல்லது மினுமினுப்பு, முகம் மற்றும் கைகள் வீக்கம், வயிற்றின் மேல் வலதுபுறம் கடுமையான வலி, யோனி வழியாக இரத்தப்போக்கு, ஒரு நாளுக்கு மேலாக குழந்தையின் அசைவு இல்லாமை, அதிக காய்ச்சல், சிறுநீர் கழிக்கையில் வலி, ஓய்வில் மூச்சுத் திணறல். மூலம்: WHO ANC / RCOG / PHM பயிற்சி."
    ),
    (
        "எனது இரத்த அழுத்தம் 162/108. வயிற்றின் மேல் வலதுபுறம் வலி உள்ளது. என் நிலை என்ன?",
        "அவசரம் - இது கடுமையான பிரீ-எக்லாம்ப்சியா (severe pre-eclampsia) ஆக இருக்கலாம். உடனடியாக மருத்துவமனைக்குச் செல்லவும். BP 160/110-ஐ விட அதிகம் + வயிற்று வலி நரம்பியல் அவசர நிலையின் அறிகுறி. தாமதிக்க வேண்டாம். மூலம்: NICE NG133 / MOH 2013."
    ),
    (
        "நான் 7வது மாதம் கர்ப்பம். குழந்தையின் அசைவு குறைவாக உள்ளது. என்ன செய்வது?",
        "இன்றே மருத்துவமனைக்குச் செல்லவும். குழந்தையின் அசைவு குறைவு கவலைக்குரிய அறிகுறி. CTG மற்றும் ultrasound தேவை. குழந்தையின் அசைவுகளை எண்ண தேவை இல்லை - வழக்கமான முறையில் மாற்றத்தை அறிந்துகொள்வது முக்கியம். மூலம்: RCOG GTG 57."
    ),
    (
        "32 வாரம் கர்ப்பம். தற்போது இரத்தப்போக்கு உள்ளது. என்ன செய்வது?",
        "அவசரம் - உடனடியாக மருத்துவமனைக்குச் செல்லவும். கர்ப்பத்தின் இரண்டாம்/மூன்றாம் மூன்று மாதங்களில் இரத்தப்போக்கு placenta praevia அல்லது placental abruption-ஆக இருக்கலாம். வீட்டில் எந்த பரிசோதனையும் செய்ய வேண்டாம். படுக்கையில் மருத்துவமனைக்குச் செல்லவும். மூலம்: RCOG GTG 63."
    ),
    # --- Vitals ---
    (
        "கர்ப்ப காலத்தில் சாதாரண இரத்த அழுத்தம் என்ன?",
        "சாதாரண: 140/90-க்கு கீழே. 140-159/90-109 - கவனிக்க வேண்டியது (gestational hypertension). 160/110 அல்லது அதற்கு மேல் - அவசரம் (severe hypertension), உடனடி சிகிச்சை. சிறுநீரில் புரதம் உள்ளது என்றால் pre-eclampsia. மூலம்: NICE NG133 / MOH 2013."
    ),
    (
        "ஹீமோகுளோபின் 7.5 g/dL. நிலை என்ன?",
        "மிதமான இரத்த சோகை (moderate anaemia). வாய்வழி இரும்பு (elemental iron) 200mg/நாள் + folic acid 5mg + vitamin C ஆரம்பிக்கவும். 2 வாரங்களில் Hb மீண்டும் சரிபார்க்கவும். பிரசவத்திற்கு குறைந்த காலம் என்றால் IV iron sucrose தேவைப்படலாம். விசேட மருத்துவ மனையைக் குறிப்பிடவும். மூலம்: RCOG GTG 47."
    ),
    (
        "ஹீமோகுளோபின் 8-க்கு குறைவு. இது எவ்வளவு ஆபத்தானது?",
        "அவசரம் - கடுமையான இரத்த சோகை. பிரசவத்தின்போது decompensation மற்றும் PPH ஆபத்து அதிகம். அதே நாளில் சிறப்பு மருத்துவ ஆலோசனை. கர்ப்ப காலத்தை பொறுத்து IV iron அல்லது இரத்தம் ஏற்றுதல். மூன்றாம் நிலை மருத்துவமனையில் பிரசவம் திட்டமிட வேண்டும். மூலம்: MOH 2013 / RCOG GTG 47."
    ),
    # --- ANC ---
    (
        "முதல் ANC சந்திப்பு எப்போது நடக்க வேண்டும்?",
        "முடிந்தவரை விரைவில் - 10 வாரத்திற்குள். தாமதமானால் 2 வாரங்களில் நடக்க வேண்டும். முதன்முதலாக கர்ப்பிணி தாய்களுக்கு 10 சந்திப்புகள், இரண்டாவது அல்லது அதற்கு மேற்பட்ட பிள்ளைகள் இருந்தால் 7. ஆபத்து இருந்தால் அதிக எண்ணிக்கை. மூலம்: NICE NG201."
    ),
    (
        "இலங்கையில் கர்ப்பிணி பெண்களுக்கு வழக்கமான பரிசோதனைகள் என்ன?",
        "பதிவுசெய்தலில்: HIV, VDRL (syphilis), Hepatitis B, rubella IgG, சிறுநீர் கல்ச்சர், FBC, Hb electrophoresis (thalassaemia - இலங்கையில் அதிகம்). 24-28 வாரம்: 75g OGTT (GDM). 28 வாரம்: anti-D (Rh-negative), Hb மீண்டும். மூலம்: Sri Lanka FHB ANC."
    ),
    (
        "கர்ப்ப காலத்தில் இரும்பு மற்றும் folic acid எவ்வளவு?",
        "Ferrous sulphate 200mg (60mg elemental iron) + folic acid 400 micrograms நாள்தோறும். முதல் ANC முதல் பிரசவத்திற்குப் பிறகு 6 வாரம் வரை. நீரிழிவு அல்லது நரம்புக் குழாய் குறைபாடு வரலாறு என்றால் folic 5mg. மூலம்: Sri Lanka FHB."
    ),
    # --- GDM ---
    (
        "Gestational diabetes எப்படி கண்டறியப்படுகிறது?",
        "75g OGTT பரிசோதனை. உண்ணாமல் இரத்த குளுக்கோஸ் ≥ 5.6 mmol/L (100 mg/dL) அல்லது 2 மணி நேரத்திற்குப் பிறகு ≥ 7.8 mmol/L (140 mg/dL) - இரண்டில் ஏதேனும் ஒன்று உயர்ந்தால் GDM. 24-28 வாரத்தில் செய்யவும் (முந்தைய GDM இருந்தால் முன்பே). மூலம்: NICE NG3."
    ),
    (
        "GDM உள்ள தாய்க்கு இரத்த சர்க்கரை இலக்கு?",
        "Capillary glucose targets (mmol/L / mg/dL): உண்ணா நிலை 5.3-க்கு கீழ் / 95-க்கு கீழ். உணவுக்கு 1 மணி நேரம் பின் 7.8-க்கு கீழ் / 140-க்கு கீழ். உணவுக்கு 2 மணி நேரம் பின் 6.4-க்கு கீழ் / 115-க்கு கீழ். Insulin பயன்படுத்தும்போது 4-க்கு மேல் வைத்திருக்க வேண்டும் (hypoglycaemia தவிர்க்க). மூலம்: NICE NG3."
    ),
    # --- PPH ---
    (
        "பிரசவத்திற்குப் பிறகு இரத்தப்போக்கை எப்படி நிறுத்துவது?",
        "Atonic PPH நடவடிக்கைகள்: (1) கருப்பையை அழுத்துதல் (uterine massage). (2) Oxytocin 10IU IM (அல்லது 5IU IV slow). (3) Ergometrine 0.5mg IV/IM (HTN என்றால் தவிர்). (4) Oxytocin infusion 40IU 500ml-இல் 125ml/மணிக்கு. (5) Tranexamic acid 1g IV 10 நிமிடம். (6) Bimanual compression. (7) Misoprostol 800mcg sublingual. (8) Foley condom balloon. (9) Consultant உடனடியாக. மூலம்: MOH 2013 / RCOG GTG 52."
    ),
    (
        "PPH தடுக்க என்ன செய்ய வேண்டும்?",
        "செயல்படும் மூன்றாம் கட்ட நிர்வாகம் (active management): (1) குழந்தை பிறந்த உடனே Oxytocin 10IU IM. (2) தொப்புள்கொடியை 2 நிமிடம் காத்திருக்க அனுமதிக்கவும். (3) Controlled cord traction. (4) Placenta வெளியில் வந்தபின் uterine massage. ஆபத்து காரணிகள் (முந்தைய PPH, anaemia, twins, polyhydramnios, dengue) இருந்தால் சிறப்பு மருத்துவ மனை. மூலம்: MOH 2013."
    ),
    # --- Eclampsia ---
    (
        "கர்ப்பிணி தாய் வலிப்பு (seizure) வந்தால் என்ன செய்வது?",
        "Eclampsia - அவசரம். (1) இடது பக்கம் திருப்பவும். (2) காற்றுப்பாதையை சுத்தம் செய்யவும், O2 8-10 L/min. (3) காயம் தடுக்கவும். (4) IV access - bloods FBC/LFT/U&E/coagulation/cross-match. (5) MgSO4 4g IV 10 நிமிடம் loading, பிறகு 1g/மணிக்கு infusion. (6) BP <160/110 - labetalol/hydralazine. (7) Foley catheter, fluids 80ml/மணிக்கு கட்டுப்பாடு. (8) நிலைப்படுத்திய பின் பிரசவம். மூலம்: MOH 2013."
    ),
    (
        "MgSO4 (magnesium sulphate) பயன்படுத்தும்போது என்ன கவனிக்க வேண்டும்?",
        "ஒவ்வொரு 30 நிமிடத்திற்கும் பதிவு செய்யவும்: (1) சிறுநீர் வெளியேற்றம் ≥30ml/மணி. (2) சுவாசம் ≥16/நிமிடம். (3) O2 saturation ≥90%. (4) Patellar reflex. RR<12, reflex இல்லை, oliguria - MgSO4 நிறுத்தவும். Toxicity-க்கு antidote: Calcium gluconate 1g IV (10ml 10%). மூலம்: MOH 2013."
    ),
    # --- Aspirin ---
    (
        "கர்ப்ப காலத்தில் aspirin எப்போது தேவை?",
        "Pre-eclampsia ஆபத்து இருந்தால் Aspirin 75-150mg நாள்தோறும் 12 வாரத்திலிருந்து பிரசவம் வரை. அதிக ஆபத்து (முந்தைய hypertensive pregnancy, CKD, autoimmune, diabetes, chronic HTN): ஏதேனும் 1 - aspirin ஆரம்பிக்க. நடுத்தர ஆபத்து 2 இருந்தால் - ஆரம்பிக்க. மூலம்: NICE NG133."
    ),
    # --- Sleep ---
    (
        "கர்ப்ப காலத்தில் முதுகில் படுப்பது பாதுகாப்பானதா?",
        "28 வாரத்திற்குப் பிறகு தாய்மார்கள் முதுகில் (supine) படுப்பதைத் தவிர்க்க வேண்டும். பக்கவாட்டில் படுக்க தலையணைகளைப் பயன்படுத்தவும். முதுகில் படுப்பது late pregnancy stillbirth ஆபத்துடன் இணைக்கப்பட்டுள்ளது. மூலம்: NICE NG201."
    ),
    # --- Nausea ---
    (
        "எனக்கு கர்ப்பகால வாந்தி அதிகம். என்ன செய்வது?",
        "மிதமான வாந்தி இயற்கையானது 16-20 வாரத்தில் சரியாகும். இஞ்சி (ginger) முயற்சிக்கவும். கடுமையானால் antiemetic (cyclizine, promethazine, prochlorperazine, ondansetron). தேவைப்பட்டால் IV fluids. Hyperemesis gravidarum (தொடர் வாந்தி, எடை இழப்பு, dehydration) - மருத்துவமனை சேர்க்கை. மூலம்: NICE NG201."
    ),
    # --- Anti-D ---
    (
        "Rh-negative தாய் 28 வாரம் அடைகிறார். அடுத்து என்ன?",
        "Anti-D Ig 1500 IU IM 28-30 வாரத்தில் (single dose) அல்லது 500 IU 28 மற்றும் 34 வாரத்தில் (two-dose). Sensitising நிகழ்வுகள் (இரத்தப்போக்கு, ECV, miscarriage, amniocentesis, abdominal trauma) எப்போது வேண்டுமானாலும் கூடுதலாக. பிரசவத்திற்குப் பிறகு குழந்தை Rh+ என்றால் 72 மணி நேரத்திற்குள். மூலம்: RCOG GTG 22."
    ),
    # --- Thalassaemia ---
    (
        "இலங்கையில் thalassaemia பரிசோதனை தாய்மார்களுக்கு முக்கியமா?",
        "ஆம். இலங்கையில் thalassaemia பரவல் அதிகம் (~2% beta-thalassaemia trait). எல்லா கர்ப்பிணி பெண்களுக்கும் பதிவில் FBC + Hb electrophoresis (MCV/MCH குறைவாக அல்லது குடும்ப வரலாறு இருந்தால்). தாய் carrier என்றால் கணவரை பரிசோதிக்கவும். இருவரும் carrier என்றால் prenatal diagnosis. மூலம்: Sri Lanka National Thalassaemia."
    ),
    # --- Dengue ---
    (
        "இலங்கையில் கர்ப்பிணி டெங்கு வந்தால் சிறப்பு கவனிப்பு?",
        "இலங்கையில் டெங்கு PPH ஆபத்து காரணி. (1) காய்ச்சல் காலத்தில் தினமும் FBC. (2) DHF எச்சரிக்கை - வயிற்று கடுமையான வலி, தொடர் வாந்தி, restlessness, இரத்தப்போக்கு. (3) fluids கவனமாக - over/under இரண்டையும் தவிர்க்க. (4) Shock காலத்தில் பிரசவம் ஆபத்து - முடிந்தால் தாமதிக்க. (5) Cross-match இரத்தம் முன்பே. மூலம்: Sri Lanka MOH Dengue."
    ),
    # --- TT ---
    (
        "Tetanus எதிர்த்த தடுப்பூசி எப்போது?",
        "இலங்கை கொள்கை: முதல் கர்ப்பத்தில் Td 2 doses, 4 வாரம் இடைவெளியில், இரண்டாவது dose பிரசவத்திற்கு குறைந்தது 4 வாரம் முன். அடுத்த கர்ப்பத்தில் booster. தாய் மற்றும் குழந்தை neonatal tetanus தடுப்பு. மூலம்: Sri Lanka EPI."
    ),
    # --- Breastfeeding ---
    (
        "தாய்ப்பால் கொடுப்பதை எப்போது தொடங்க வேண்டும்?",
        "பிரசவத்திலிருந்து 30 நிமிடத்திற்குள் (இலட்சியம்: 1 மணி நேரத்திற்குள்). குழந்தையை தாயின் வயிற்றில் வைத்து, உலர்த்தி, skin-to-skin, பிறகு மார்பின் இடையே. நீரிழிவு தாய்களின் குழந்தைகளுக்கு குறிப்பாக - hypoglycaemia தடுக்க. மூலம்: MOH 2013."
    ),
    # --- Bleeding postpartum ---
    (
        "பிரசவத்திற்குப் பிறகு இரத்தப்போக்கு பல வாரங்கள் தொடர்கிறது. சாதாரணமா?",
        "Lochia (postpartum bleeding) சாதாரணம் - முதல் 3-4 நாட்கள் சிவப்பு (lochia rubra), பிறகு pinkish (lochia serosa), பிறகு வெள்ளை/மஞ்சள் (lochia alba) 6 வாரம் வரை. கடுமையான இரத்தப்போக்கு, பெரிய clots, துர்நாற்றம், காய்ச்சல் - உடனடியாக மருத்துவ மனை. மூலம்: MOH 2013."
    ),
    # --- Birth timing for diabetes ---
    (
        "Type 1/2 diabetes உள்ள தாய்க்கு பிரசவம் எப்போது?",
        "Elective birth induction (அல்லது தேவையானால் CS) 37+0 முதல் 38+6 வாரம் வரை. Metabolic அல்லது maternal/fetal complications இருந்தால் முன்னதாகவே. GDM (சாதாரண): 40+6 வாரம் தாண்டக்கூடாது. மூலம்: NICE NG3."
    ),
    # --- Newborn warning ---
    (
        "புதிதாகப் பிறந்த குழந்தையின் ஆபத்து அறிகுறிகள் என்ன?",
        "உடனடியாக கவனிக்க: (1) பால் அருந்த மாட்டார். (2) அதிக நிசத்தம் / பிடிப்பு. (3) வெப்பநிலை அதிகம் (>38°C) அல்லது குறைவு (<35.5°C). (4) 24 மணி நேரத்திற்குள் மஞ்சள் காமாலை. (5) வேகமான / கடினமான சுவாசம். (6) எடை குறைவு >7% முதல் வாரத்தில். (7) Convulsion. (8) மென்மையான / விறைப்பான கழுத்து. மருத்துவமனைக்குச் செல்லவும். மூலம்: Sri Lanka MOH Newborn."
    ),
    # --- Iron / Folate ---
    (
        "கர்ப்ப காலத்தில் இரும்பு ஏற்றுக்கொள்ள உதவும் / தடுக்கும் உணவுகள்?",
        "உதவும்: சிவப்பு இறைச்சி/மீன்/கோழி (haem iron), சாறு பழங்கள் (vitamin C), பச்சை இலை காய்கறிகள், gingelly seeds (எள்), கைப்பழம். தடுக்கும்: தேநீர், காப்பி (உணவுடன் தவிர்க்க), பால் / yoghurt (இரும்புடன் சேர்க்க வேண்டாம்). Iron-தாமிரம் இரட்டை ஏற்பாட்டில் எடுத்துக்கொள்ளவும். மூலம்: Sri Lanka FHB."
    ),
    # --- Drugs to avoid ---
    (
        "கர்ப்ப காலத்தில் தவிர்க்க வேண்டிய மருந்துகள்?",
        "தவிர்க்க: ACE inhibitors (enalapril, captopril), ARBs (losartan), statins, NSAIDs (மூன்றாம் trimester), warfarin, retinoids (Vit A), tetracyclines, ergometrine (severe pre-eclampsia-இல்). தேவையான மருந்துகளை மருத்துவருடன் ஆலோசிக்கவும். மூலம்: MOH 2013 / RCOG."
    ),
    # --- Refer ---
    (
        "எந்த நிலையில் கர்ப்பிணியை உடனடியாக மருத்துவமனைக்கு அனுப்ப வேண்டும்?",
        "உடனடி refer: BP ≥160/110 அல்லது pre-eclampsia அறிகுறிகள்; eclampsia/seizure; யோனி இரத்தப்போக்கு (எந்த அளவாக இருந்தாலும்); fetal movement இல்லை / குறைவு; severe headache + visual disturbance; செக்வென்ஸ் hyperglycaemia + DKA அறிகுறிகள் (வாந்தி, மூச்சு நாற்றம், மோசமான நிலை); preterm labour <37 weeks; ROM >18 பாக்டீரியா ரோக அறிகுறிகளுடன்; கடுமையான இரத்த சோகை (Hb<8); உயிர் அபாயம் சந்தேகம். மூலம்: MOH 2013."
    ),
    # --- Diet ---
    (
        "கர்ப்ப காலத்தில் சேர்க்க / தவிர்க்க வேண்டிய உணவுகள்?",
        "சேர்க்க: பச்சை இலைக் காய்கறிகள் (folate), சிவப்பு இறைச்சி/மீன் (iron), vitamin C பழங்கள் (orange, அன்னாசி), பால்/yoghurt (calcium), parippu/பருப்பு/நிலக்கடலை (protein). தவிர்க்க: பச்சை இறைச்சி/மீன் (toxoplasmosis), unpasteurised பால், அதிக vitamin A, காப்பி/தேநீர் (iron absorption குறையும்), மது. மூலம்: Sri Lanka FHB Maternal Nutrition."
    ),
    # --- Tablets / supplements ---
    (
        "கர்ப்பிணி தாய்கள் தினமும் எடுத்துக்கொள்ள வேண்டிய மாத்திரைகள்?",
        "(1) Folic acid 400mcg (நீரிழிவு அல்லது நரம்பு குறைபாடு வரலாறு என்றால் 5mg) - முதல் 12 வாரம் வரை. (2) Ferrous sulphate 200mg (60mg elemental iron) - முதல் ANC முதல் பிரசவத்திற்குப் பிறகு 6 வாரம் வரை. (3) Calcium 600mg (ஆபத்து குழுவில்). (4) Vitamin D தேவையானால். கர்ப்பத்திற்கு முன் folic acid 3 மாதம் முன் தொடங்க பரிந்துரை. மூலம்: Sri Lanka FHB."
    ),
    # --- Severe anaemia ---
    (
        "Hb 7.5 g/dL, 32 வாரம் கர்ப்பிணி. திட்டம்?",
        "மிதமான இரத்த சோகை - இரத்தம் ஏற்றுதல் இல்லாமல் அவசர நடவடிக்கை. (1) Iron deficiency உறுதி: low ferritin, low MCV, low MCH; thalassaemia நீக்கம். (2) வாய்வழி elemental iron 200mg/நாள் + folic acid 5mg + vitamin C. (3) சகிக்க முடியாதது அல்லது <4 வாரம் பிரசவத்திற்கு என்றால் IV iron sucrose. (4) 2 வாரத்தில் Hb மீண்டும். (5) IV iron + பிரசவ திட்டத்திற்கு specialist. மூலம்: RCOG GTG 47."
    ),
    # --- Severe HTN treatment ---
    (
        "BP 178/115. மருத்துவமனை 2 மணி நேரம் தூரம். அனுப்புவதற்கு முன் என்ன செய்வது?",
        "அவசரம் - severe hypertension. அனுப்புதலுக்கு முன்: (1) IV access. (2) Oral nifedipine 10mg (20 நிமிடத்திற்கு repeat, max 40mg) - BP <160/110 ஆக்க. (3) MgSO4 4g IV (or 5g IM each buttock) loading - transit-இல் eclampsia தடுக்க. (4) Foley catheter, urine output கண்காணிக்க. (5) பெறும் மருத்துவ மனைக்கு அழைப்பு. (6) Staff member emergency drugs உடன் அனுப்ப. மூலம்: MOH 2013."
    ),
    # --- VBAC ---
    (
        "VBAC (previous CS பிறகு vaginal birth) - வெற்றி வீதம் மற்றும் ஆபத்து?",
        "வெற்றி வீதம் ~72-75%. ஆபத்து: uterine scar rupture ~0.5% (ஒரு முந்தைய CS-உடன்), பல CS-களுடன் கூடுதலாக. தேர்வுக்கான பொருத்தம்: ஒரு முந்தைய lower segment CS, இந்த கர்ப்பத்தில் CS-க்கான வேறு indication இல்லை, vaginal birth-க்கு வேறு contraindication இல்லை. Labour-இல் continuous CTG. Induction-இல் prostaglandins தவிர்க்க. மூலம்: RCOG GTG 45."
    ),
    # --- Twins ---
    (
        "Twin கர்ப்பத்தில் கூடுதல் கவனிப்பு என்ன?",
        "(1) Chorionicity முதல் scan-இல் (11-13+6 வாரம்) - lambda/T sign. (2) DCDA: 20 வாரத்திலிருந்து 4 வாரத்திற்கு ஒரு scan. MCDA: 16 வாரத்திலிருந்து 2 வாரத்திற்கு (TTTS). MCMA: 24 வாரத்திலிருந்து வாரம். (3) Aspirin 75-150mg 12 வாரத்திலிருந்து. (4) Iron + folate. (5) பிரசவ திட்டம்: DCDA 37+0-37+6, MCDA 36+0-36+6, MCMA 32-34 CS. மூலம்: NICE NG137."
    ),
    # --- HIV ---
    (
        "PMTCT (HIV) இலங்கை?",
        "பதிவில் எல்லா கர்ப்பிணி பெண்களுக்கும் HIV பரிசோதனை (informed consent). HIV+ என்றால் - ART உடனடியாக. பிரசவ முறை specialist-உடன் ஆலோசனை (vaginal vs CS). குழந்தைக்கு ART prophylaxis மற்றும் formula feeding (BFHI Sri Lanka guidelines). மூலம்: STD/AIDS Control Programme."
    ),
    # --- Iron oral dosing ---
    (
        "Iron deficiency anaemia-க்கு வாய்வழி iron எவ்வளவு?",
        "Therapeutic dose: oral elemental iron 100-200 mg/நாள் (e.g., ferrous sulphate 200mg tid). உணவுக்கு இடையில் vitamin C-உடன் (orange juice) absorption-க்கு. தேநீர்/காப்பி/calcium-உடன் சேர்க்க வேண்டாம். 2 வாரத்தில் Hb மீண்டும் - 1 g/dL உயர்வு எதிர்பார்க்கப்படுகிறது. மூலம்: RCOG GTG 47 / Sri Lanka FHB."
    ),
]


def build_dataset(output_path: Path):
    """Write all pairs to JSONL."""
    all_pairs = []
    sections = [
        ("hypertension", HYPERTENSION_EN),
        ("pph", PPH_EN),
        ("diabetes", DIABETES_EN),
        ("labour", LABOUR_EN),
        ("anc", ANC_EN),
        ("anaemia", ANAEMIA_EN),
        ("misc", MISC_EN),
        ("nice_ng133", NICE_NG133_EN),
        ("nice_ng3", NICE_NG3_EN),
        ("rcog_gtg52_47", RCOG_PPH_TRANSFUSION_EN),
        ("rcog_gtg57", RCOG_RFM_EN),
        ("nice_ng201", NICE_NG201_EN),
    ]
    sinhala_sections = [("mixed", SINHALA_SI)]
    tamil_sections = [("mixed", TAMIL_TA)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for topic, pairs in sections:
            for q, a in pairs:
                record = {"instruction": q, "output": a, "topic": topic, "lang": "en"}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                all_pairs.append(record)
        for topic, pairs in sinhala_sections:
            for q, a in pairs:
                record = {"instruction": q, "output": a, "topic": topic, "lang": "si"}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                all_pairs.append(record)
        for topic, pairs in tamil_sections:
            for q, a in pairs:
                record = {"instruction": q, "output": a, "topic": topic, "lang": "ta"}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                all_pairs.append(record)

    # Print summary
    print(f"Wrote {len(all_pairs)} pairs to {output_path}")
    from collections import Counter
    by_topic = Counter(p["topic"] for p in all_pairs)
    by_lang = Counter(p["lang"] for p in all_pairs)
    print("By topic:", dict(by_topic))
    print("By language:", dict(by_lang))


if __name__ == "__main__":
    output = Path(__file__).parent / "dataset.jsonl"
    build_dataset(output)
