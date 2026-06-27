"""
OfflineMidwife — 100-question evaluation dataset
50 English (EN-01 to EN-50) + 50 Sinhala (SI-01 to SI-50)
Replace EVAL_QUESTIONS in eval_gemma4_comparison.ipynb cell ev000008
"""

EVAL_QUESTIONS = [
    # ── ENGLISH QUESTIONS ──────────────────────────────────────────────────────

    # Hypertension / Pre-eclampsia
    {"id":"EN-01","lang":"en","topic":"hypertension",
     "question":"A 38-year-old primigravida at 36 weeks has BP 150/98, 1+ proteinuria, mild hand swelling. No headache or visual symptoms. Risk level and next step?"},
    {"id":"EN-02","lang":"en","topic":"hypertension",
     "question":"A woman at 26 weeks with chronic hypertension on methyldopa 250mg TID presents with BP 168/112 despite medication. What should I do?"},
    {"id":"EN-03","lang":"en","topic":"eclampsia",
     "question":"A woman at 30 weeks has a generalised tonic-clonic seizure in the clinic. No prior epilepsy. Immediate steps?"},
    {"id":"EN-04","lang":"en","topic":"hypertension",
     "question":"Which women should receive aspirin 75-150mg daily to prevent pre-eclampsia, and when should it be started?"},
    {"id":"EN-05","lang":"en","topic":"hypertension",
     "question":"A woman has BP 178/116 and severe headache at 34 weeks. Specialist hospital is 2 hours away. What do you do before transfer?"},

    # Reduced fetal movement
    {"id":"EN-06","lang":"en","topic":"reduced_fetal_movement",
     "question":"A mother at 32 weeks has not felt the baby move since yesterday morning. Good movements before. Recommended assessment?"},
    {"id":"EN-07","lang":"en","topic":"reduced_fetal_movement",
     "question":"Should pregnant women use kick charts? What does current RCOG guidance say about routine kick counting?"},

    # Postpartum haemorrhage
    {"id":"EN-08","lang":"en","topic":"postpartum_haemorrhage",
     "question":"A woman delivers at a peripheral clinic with 800ml blood loss within 30 min of birth. Placenta delivered. Immediate management?"},
    {"id":"EN-09","lang":"en","topic":"postpartum_haemorrhage",
     "question":"What uterotonic drugs are used for prevention and treatment of PPH, and what are the preferred first-line choices?"},
    {"id":"EN-10","lang":"en","topic":"postpartum_haemorrhage",
     "question":"A woman delivered 2 hours ago. Uterus is well contracted but fresh bleeding continues. What is the likely cause and management?"},
    {"id":"EN-11","lang":"en","topic":"postpartum_haemorrhage",
     "question":"A woman has secondary PPH — heavy bleeding 12 days postpartum with fever. What are the causes and management?"},

    # Anaemia
    {"id":"EN-12","lang":"en","topic":"anaemia",
     "question":"A pregnant woman at 28 weeks has Hb 9.2 g/dL. She has been on oral iron for 4 weeks with no improvement. Next step?"},
    {"id":"EN-13","lang":"en","topic":"anaemia",
     "question":"At what haemoglobin level should a pregnant woman be referred for blood transfusion?"},
    {"id":"EN-14","lang":"en","topic":"anaemia",
     "question":"A woman at 34 weeks has Hb 7.2 g/dL, is breathless on exertion, and has pale conjunctivae. What is the risk level and management?"},

    # Diabetes
    {"id":"EN-15","lang":"en","topic":"diabetes",
     "question":"A woman at 26 weeks has a random blood glucose of 11.2 mmol/L. No prior diabetes. What investigations are required?"},
    {"id":"EN-16","lang":"en","topic":"diabetes",
     "question":"Target fasting and 2-hour post-meal blood glucose for a pregnant woman with gestational diabetes on diet control?"},
    {"id":"EN-17","lang":"en","topic":"diabetes",
     "question":"A woman with GDM on insulin becomes confused, sweaty and unresponsive. What is the likely diagnosis and immediate action?"},

    # Antenatal care
    {"id":"EN-18","lang":"en","topic":"antenatal_care",
     "question":"A woman at 10 weeks, first visit, BMI 36, no known conditions. Complete booking assessment the PHM should perform?"},
    {"id":"EN-19","lang":"en","topic":"antenatal_care",
     "question":"Which routine blood tests should be offered at the first antenatal visit in Sri Lanka?"},
    {"id":"EN-20","lang":"en","topic":"antenatal_care",
     "question":"A woman at 20 weeks has fundal height of 18 cm. What is the interpretation and next step?"},

    # Neonatal care
    {"id":"EN-21","lang":"en","topic":"neonatal",
     "question":"What are the danger signs in a newborn that require immediate referral to hospital?"},
    {"id":"EN-22","lang":"en","topic":"neonatal",
     "question":"A 3-day-old baby has deep yellow jaundice reaching the palms and soles. Risk level and action?"},
    {"id":"EN-23","lang":"en","topic":"neonatal",
     "question":"A newborn at 1 minute of life is floppy, not breathing and has a heart rate of 60 bpm. What do you do?"},
    {"id":"EN-24","lang":"en","topic":"neonatal",
     "question":"A baby is born at 2.1 kg at 37 weeks. What are the special care requirements for this low birth weight baby?"},
    {"id":"EN-25","lang":"en","topic":"neonatal",
     "question":"How should the umbilical cord stump be cared for after birth? What signs indicate infection?"},

    # Postnatal maternal care
    {"id":"EN-26","lang":"en","topic":"postnatal",
     "question":"A woman on day 3 postpartum has fever 38.5°C, tender uterus, and offensive lochia. What is the diagnosis and management?"},
    {"id":"EN-27","lang":"en","topic":"postnatal",
     "question":"A breastfeeding mother on day 8 has a red, tender, hot area on one breast with fever. Management?"},
    {"id":"EN-28","lang":"en","topic":"postnatal",
     "question":"What does normal lochia look like at day 1, day 5, and day 14 postpartum?"},
    {"id":"EN-29","lang":"en","topic":"postnatal",
     "question":"A woman 2 weeks postpartum is crying most of the day, not bonding with the baby, and says she wishes she had never had the baby. What is the risk level and next step?"},

    # Breastfeeding
    {"id":"EN-30","lang":"en","topic":"breastfeeding",
     "question":"When should breastfeeding be initiated and what is the recommended duration of exclusive breastfeeding?"},
    {"id":"EN-31","lang":"en","topic":"breastfeeding",
     "question":"A mother says her baby is not latching properly and her nipples are cracked and bleeding. How do you help her?"},

    # Immunisation
    {"id":"EN-32","lang":"en","topic":"immunisation",
     "question":"What vaccines should a newborn receive at birth and at 6 weeks according to the Sri Lanka EPI schedule?"},
    {"id":"EN-33","lang":"en","topic":"immunisation",
     "question":"A pregnant woman has no record of rubella vaccination. Rubella IgG is negative. What do you advise?"},

    # Labour complications
    {"id":"EN-34","lang":"en","topic":"labour",
     "question":"The cord is seen at the vulva after membrane rupture at 36 weeks. What is the immediate action?"},
    {"id":"EN-35","lang":"en","topic":"labour",
     "question":"After delivery of the head, the shoulders do not deliver with normal traction. What manoeuvres do you use for shoulder dystocia?"},
    {"id":"EN-36","lang":"en","topic":"labour",
     "question":"Heavy meconium-stained liquor is seen at ARM in a term labour. What is the significance and management?"},
    {"id":"EN-37","lang":"en","topic":"labour",
     "question":"A woman at 34 weeks presents with painful contractions every 5 minutes and cervix 3 cm dilated. Diagnosis and management?"},

    # Antepartum haemorrhage
    {"id":"EN-38","lang":"en","topic":"aph",
     "question":"A woman at 32 weeks has painless bright red vaginal bleeding. Vital signs stable. What is the priority investigation and why?"},
    {"id":"EN-39","lang":"en","topic":"aph",
     "question":"A woman at 36 weeks has sudden onset severe abdominal pain, a woody-hard uterus, and no fetal movements. Diagnosis and action?"},

    # Infections
    {"id":"EN-40","lang":"en","topic":"infections",
     "question":"A pregnant woman has dysuria, frequency and cloudy urine at 20 weeks. Management?"},
    {"id":"EN-41","lang":"en","topic":"infections",
     "question":"A pregnant woman at 28 weeks has platelet count of 45,000 during a dengue febrile illness. Risk level and action?"},
    {"id":"EN-42","lang":"en","topic":"infections",
     "question":"A pregnant woman is newly diagnosed HIV positive at her first antenatal visit. What is the immediate management and counselling?"},

    # Nutrition and lifestyle
    {"id":"EN-43","lang":"en","topic":"nutrition",
     "question":"How much weight should a woman of normal BMI gain during pregnancy? What about overweight women?"},
    {"id":"EN-44","lang":"en","topic":"nutrition",
     "question":"When should folic acid be started, what dose, and for how long in a woman planning pregnancy?"},

    # Family planning
    {"id":"EN-45","lang":"en","topic":"family_planning",
     "question":"A breastfeeding mother 6 weeks postpartum wants contraception. What are the safest options and which should be avoided?"},
    {"id":"EN-46","lang":"en","topic":"family_planning",
     "question":"What are the three criteria for the Lactational Amenorrhoea Method (LAM) to be effective as contraception?"},

    # Miscellaneous
    {"id":"EN-47","lang":"en","topic":"thalassaemia",
     "question":"Both partners are thalassaemia trait carriers. What is the risk to the baby and what counselling is needed?"},
    {"id":"EN-48","lang":"en","topic":"misc",
     "question":"A woman had a previous caesarean section. She is now 38 weeks in a new pregnancy. What determines if VBAC is appropriate?"},
    {"id":"EN-49","lang":"en","topic":"misc",
     "question":"A woman at 39 weeks states her waters broke 2 hours ago. No contractions. What is the management of term PROM?"},
    {"id":"EN-50","lang":"en","topic":"misc",
     "question":"Fundal height at 28 weeks is 32 cm. What does this suggest and what is the next investigation?"},

    # ── SINHALA QUESTIONS ──────────────────────────────────────────────────────

    # Hypertension
    {"id":"SI-01","lang":"si","topic":"hypertension",
     "question":"ගර්භිනී කාන්තාවක්ගේ රුධිර පීඩනය 155/100 mmHg. කිසිදු රෝග ලක්ෂණයක් නැත. ජෝජු ක්‍රියාමාරගය කුමක්ද?"},
    {"id":"SI-02","lang":"si","topic":"hypertension",
     "question":"ගර්භිනීව සිටින කාන්තාවක් රුධිර පීඩනය 170/114, ප්‍රෝටීනිහිතය 3+, හිසරදය සහ ද්‍රුෂ්ටි ගැටලු. හදිස්සි ක්‍රියාව කුමක්ද?"},
    {"id":"SI-03","lang":"si","topic":"eclampsia",
     "question":"සතිය 38 ගර්භිනී කාන්තාවකට සෙලවීම් ගිහිල්ලා දැන් හිත නොතේරේ. මේ අවස්ථාවේ ක්‍රියාවලිය?"},
    {"id":"SI-04","lang":"si","topic":"hypertension",
     "question":"ගර්භිනී කාන්තාවකගේ රුධිර පීඩනය 160/105 mmHg, හිසරදය ඇත. රෝහලට යාමට පෙර PHM ලෙස කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-05","lang":"si","topic":"hypertension",
     "question":"ප්‍රී-එක්ලැම්ප්සියා වැළැක්වීම සඳහා ඇස්පිරින් ලබා දිය යුතු කාන්තාවන් කවුද? කවදා ආරම්භ කළ යුතුද?"},

    # Reduced fetal movement
    {"id":"SI-06","lang":"si","topic":"reduced_fetal_movement",
     "question":"සතිය 36 ගර්භිනී කාන්තාවකට ඊයේ ඉදලා දරුවාගේ සෙලවීම් 4ක් විතරක් දැනුණා. PHM ලෙස ඔබ කුමක් කරනවාද?"},
    {"id":"SI-07","lang":"si","topic":"reduced_fetal_movement",
     "question":"ගර්භිනී කාන්තාවකට CTG කළ යුතු නම් කොහේ යොමු කළ යුතුද?"},

    # Postpartum haemorrhage
    {"id":"SI-08","lang":"si","topic":"postpartum_haemorrhage",
     "question":"ප්‍රසූතිය සිදු වී මිනිත්තු 15 ගත්, ජෙරනිය බිහිවී නැත, රුධිරය ගලා යයි. PHM ලෙස කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-09","lang":"si","topic":"postpartum_haemorrhage",
     "question":"ප්‍රසූතියෙන් දින 10 කට පසු ගර්භාෂයෙන් ඕනෑවට වඩා රුධිරය ගලා යයි. හේතු සහ කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-10","lang":"si","topic":"postpartum_haemorrhage",
     "question":"PPH සඳහා ට්‍රැනෙක්සමික් අම්ලය ලබා දිය යුත්තේ කෙසේද? මාත්‍රාව කීයද?"},

    # Anaemia
    {"id":"SI-11","lang":"si","topic":"anaemia",
     "question":"ගර්භිනී කාන්තාවකගේ හිමොග්ලොබින් 8.5 g/dL, සතිය 30, හුස්ම ගන්නට අමාරු. කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-12","lang":"si","topic":"anaemia",
     "question":"ගර්භිනී කාන්තාවකට යකඩ ටැබ්ලට් දෙන විට ශරීරය ජොරපිට ඇතිවේ. වෙනත් ක්‍රමයකින් ලබාදිය හැකිද?"},
    {"id":"SI-13","lang":"si","topic":"anaemia",
     "question":"ගර්භිනී කාන්තාවකගේ Hb 6.8 g/dL, සතිය 35. මෙය කෙතරම් භයානකද? කළ යුත්තේ කුමක්ද?"},

    # Diabetes
    {"id":"SI-14","lang":"si","topic":"diabetes",
     "question":"ගර්භිනී කාන්තාවකගේ රුධිර ග්ලූකෝස් 6.8 mmol/L. GDM ඇතිදැයි නිශ්චිතව දැනගන්නේ කෙසේද?"},
    {"id":"SI-15","lang":"si","topic":"diabetes",
     "question":"GDM ඇති ගර්භිනී කාන්තාවකට ඉන්සියුලින් ලබා දිනා විට කකුල් ලෙලදෙයි, දහඩිය, කතා කරන්නේ නෑ. PHM ලෙස කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-16","lang":"si","topic":"diabetes",
     "question":"GDM ඇති කාන්තාවකට ආහාර සම්බන්ධ උපදෙස් මොනවාද? ආහාර ගැනීමෙන් GDM පාලනය කළ හැකිද?"},

    # Antenatal care
    {"id":"SI-17","lang":"si","topic":"antenatal_care",
     "question":"ගර්භ සතිය 12 දී PHM සිදු කළ යුතු ඇගයීම් මොනවාද?"},
    {"id":"SI-18","lang":"si","topic":"antenatal_care",
     "question":"ගර්භිනී කාන්තාවක් දුම්කොළ පානය කරනවා. ගර්භනී සමයේ දුම්කොළ ගැන මගපෙන්වීම කුමක්ද?"},
    {"id":"SI-19","lang":"si","topic":"antenatal_care",
     "question":"ගර්භිනී කාන්තාවකට කොයි රෝග ලකුණු ගෙදර දී ඇති වුනොත් වහාම රෝහලට යන්න ඕනෑද?"},

    # Neonatal
    {"id":"SI-20","lang":"si","topic":"neonatal",
     "question":"නව ජාත ශිශුවකගේ භය ලකුණු මොනවාද? PHM ලෙස ඔබ වහා රෝහලට යෙදවිය යුතු සලකුණු?"},
    {"id":"SI-21","lang":"si","topic":"neonatal",
     "question":"දින 3 ක් වයසැති ළදරුවකුගේ සම, ඇස් සහ පපුව කහ පාටයි. ඉදිරි ක්‍රියාමාර්ගය?"},
    {"id":"SI-22","lang":"si","topic":"neonatal",
     "question":"ළදරුවා උපදින විට හුස්ම ගන්නේ නෑ, ශරීරය මෘදුයි. PHM ලෙස කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-23","lang":"si","topic":"neonatal",
     "question":"2.0 kg ශිශුවකු උපන්නා. පෙරකල්‌ ළදරුවාට විශේෂ සත්කාර ලෙස PHM ලෙස දිය යුතු ඉගැන්වීම් මොනවාද?"},
    {"id":"SI-24","lang":"si","topic":"neonatal",
     "question":"නාළඹ කඩා ගිය පසු දින කීයකට සුව වේද? ආසාදන ලකුණු මොනවාද?"},

    # Postnatal maternal
    {"id":"SI-25","lang":"si","topic":"postnatal",
     "question":"ප්‍රසූතියෙන් දින 3 ට ගිහිල්ලා උෂ්ණත්වය 38.5°C, ගර්භාෂය ස්පර්ශ කළ විට රිදේ, ලොකියා දුගඳ දෙයි. රෝගය කුමක්ද, කළ යුත්තේ?"},
    {"id":"SI-26","lang":"si","topic":"postnatal",
     "question":"මව්කිරි දෙන අම්මාට දින 8 ට ගිහිල්ලා පපුවේ රතු, උණ, රිදෙන ප්‍රදේශයක් ඇත. PHM ලෙස?"},
    {"id":"SI-27","lang":"si","topic":"postnatal",
     "question":"ප්‍රසූතියෙන් සති 2 කට පසු අම්මා දිනෙන් දිනේ කඳුළු ගලා, ළදරුවා ස්පර්ශ කිරීමට අකමැතිය. මෙය කුමක්ද?"},
    {"id":"SI-28","lang":"si","topic":"postnatal",
     "question":"සාමාන්‍ය ලොකියා ප්‍රසූතිය සිදු වී දිනය, 5 දිනය, 14 දිනය දෙස ගත් කළ කෙසේ ද?"},

    # Breastfeeding
    {"id":"SI-29","lang":"si","topic":"breastfeeding",
     "question":"ළදරුවාගේ නිසි ලෙස කිරි ගැනීම සහ පපුව ගෑගෑවීම නිවැරදිව සිදු වෙනවාද යන්න PHM ලෙස කෙසේ ඇගයීය හැකිද?"},
    {"id":"SI-30","lang":"si","topic":"breastfeeding",
     "question":"සුපිරිව මව්කිරි දීම (exclusive breastfeeding) කෙතරම් කාලයක් කළ යුතුද? ඊට හේතු?"},

    # Immunisation
    {"id":"SI-31","lang":"si","topic":"immunisation",
     "question":"ශ්‍රී ලංකා EPI කාලසටහනට අනුව ළදරුවකු ලැබූ වහාම සහ සති 6 ට ලබා දිය යුතු එන්නත් මොනවාද?"},
    {"id":"SI-32","lang":"si","topic":"immunisation",
     "question":"ගර්භිනී කාන්තාවකගේ රූබෙලා IgG නිශේධ (negative). ඇය ගැන කළ යුත්තේ කුමක්ද?"},

    # Labour
    {"id":"SI-33","lang":"si","topic":"labour",
     "question":"ආර්ද්‍ර කෝෂය කැඩීමෙන් පසු පෙකණු හිල් දිස්වේ. URGENT ලෙස කළ යුත්තේ කුමක්ද?"},
    {"id":"SI-34","lang":"si","topic":"labour",
     "question":"ළදරුවාගේ හිස ප්‍රසූත් වූ පසු උරහිස් ඇවිල්ලේ නොමැත. PHM ලෙස?"},
    {"id":"SI-35","lang":"si","topic":"labour",
     "question":"ARM කළ පසු මිශ්‍ර ද්‍රව (meconium-stained liquor) දිස්වේ. මෙය භයානකද? කළ යුත්තේ?"},
    {"id":"SI-36","lang":"si","topic":"labour",
     "question":"සතිය 34 ළඟා ශ්‍රී ගර්භිනී කාන්තාවකට මිනිත්තු 5කට වරක් රිදෙන සංකෝචනය. ගැබ් ගෙල 3 cm. රෝගය කුමක්ද?"},

    # APH
    {"id":"SI-37","lang":"si","topic":"aph",
     "question":"සතිය 32 ගර්භිනී කාන්තාවකට රිදීමක් නොමැතිව යෝනි මාර්ගයෙන් රුධිරය ගලා යයි. PHM ලෙස කළ නොකළ යුතු දේ?"},
    {"id":"SI-38","lang":"si","topic":"aph",
     "question":"සතිය 36 ගර්භිනී කාන්තාවකට හදිසිය බඩේ දැඩි රිදීම, ගර්භාෂය ගල් ගැහුවා. දරුවාගේ සෙලවීම් නැත. රෝගය සහ ක්‍රියාව?"},

    # Infections
    {"id":"SI-39","lang":"si","topic":"infections",
     "question":"ගර්භිනී කාන්තාවකට මුත්‍රා කිරීමේ දැවිල්ල, නිතර මුත්‍රා, බඩ රිදීම. සතිය 24. කළ යුත්තේ?"},
    {"id":"SI-40","lang":"si","topic":"infections",
     "question":"ගර්භිනී කාන්තාවකට ඩෙංගු උෂ්ණය, රුධිරාණු 40,000 ට හිත. PHM ලෙස නිරීක්ෂණ?"},

    # Nutrition
    {"id":"SI-41","lang":"si","topic":"nutrition",
     "question":"ගර්භනී සමයේ ෆොලික් අම්ලය කෙතරම් ලබා ගත යුතුද? ආරම්භ කළ යුත්තේ කවදාද?"},
    {"id":"SI-42","lang":"si","topic":"nutrition",
     "question":"ගර්භනී සමයේ ශරීර බරේ වැඩිවීම සාමාන්‍ය BMI ඇති කාන්තාවකට කෙතරම් ද?"},

    # Family planning
    {"id":"SI-43","lang":"si","topic":"family_planning",
     "question":"ප්‍රසූතියෙන් සති 6 කට මව්කිරි දෙන අම්මාවකට ආරක්ෂිත ගැබ් ගැනීම් වැළැක්වීමේ ක්‍රම මොනවාද?"},
    {"id":"SI-44","lang":"si","topic":"family_planning",
     "question":"LAM (Lactational Amenorrhoea Method) ක්‍රමය ක්‍රියාත්මක වීමට ඉටු කළ යුතු කොන්දේසි 3 මොනවාද?"},

    # Misc / Special topics
    {"id":"SI-45","lang":"si","topic":"thalassaemia",
     "question":"ස්වාමිපුරුෂයා සහ භාර්යාව දෙදෙනාම thalassaemia trait (ලක්ෂණ ජාවාරම) දරයි. දරුවාට ඇති අවදානම? ඊළඟ ක්‍රියාව?"},
    {"id":"SI-46","lang":"si","topic":"misc",
     "question":"ගර්භිනී කාන්තාවකගේ fundal height සතිය 28 ට 32 cm. ඉදිරි ක්‍රියාව?"},
    {"id":"SI-47","lang":"si","topic":"misc",
     "question":"කලින් CS කළ කාන්තාවකට සාමාන්‍ය ප්‍රසූතියක් (VBAC) සිදු කළ හැකිද? කොන්දේසි?"},
    {"id":"SI-48","lang":"si","topic":"misc",
     "question":"ගර්භ සතිය 38 දී ළදරුවා breech (පිටිකාරී) ස්ථානයේ ඇත. PHM ලෙස කළ යුත්තේ?"},
    {"id":"SI-49","lang":"si","topic":"misc",
     "question":"සතිය 39 ගර්භිනී කාන්තාවකගේ දිය ගෙඩිය කැඩී ඇත. සංකෝචනය නොමැත. PHM ලෙස කළ යුත්තේ?"},
    {"id":"SI-50","lang":"si","topic":"postnatal",
     "question":"ප්‍රසූතියෙන් මාස 3 ට ඉදිරිට ගර්භ ගැනීම් වැළැක්වීම සඳහා DMPA ලබා ගත හැකිද? යම් ආරෝප (contraindications) ඇතිද?"},
]
