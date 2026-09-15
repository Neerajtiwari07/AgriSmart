import csv
import os


INPUT_FILE = "datasets/agri_faq_clean.csv"
OUTPUT_FILE = "datasets/agri_faq_clean.csv"


NEW_RECORDS = [

    # ============================================================
    # TOMATO
    # ============================================================

    {
        "Question": "When should tomato be planted?",
        "Keywords": "tomato,sowing,planting",
        "Answer": "Tomato planting time depends on the local climate, season, and variety.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "sowing",
    },
    {
        "Question": "टमाटर की बुवाई कब करें?",
        "Keywords": "टमाटर,बुवाई,रोपाई",
        "Answer": "टमाटर की बुवाई या रोपाई का समय स्थानीय जलवायु, मौसम और किस्म पर निर्भर करता है।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "sowing",
    },
    {
        "Question": "What soil is suitable for tomato?",
        "Keywords": "tomato,soil,soil type",
        "Answer": "Tomato generally performs well in fertile, well-drained soil with suitable soil pH.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "soil",
    },
    {
        "Question": "टमाटर के लिए कौन सी मिट्टी अच्छी होती है?",
        "Keywords": "टमाटर,मिट्टी,soil",
        "Answer": "टमाटर के लिए उपजाऊ और अच्छी जल निकासी वाली मिट्टी उपयुक्त होती है।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "soil",
    },
    {
        "Question": "How often should tomato be irrigated?",
        "Keywords": "tomato,irrigation,water",
        "Answer": "Tomato should receive regular irrigation according to soil moisture, weather, and crop growth stage.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "irrigation",
    },
    {
        "Question": "टमाटर में कितनी सिंचाई करनी चाहिए?",
        "Keywords": "टमाटर,सिंचाई,पानी",
        "Answer": "टमाटर में मिट्टी की नमी, मौसम और फसल की अवस्था के अनुसार नियमित सिंचाई करनी चाहिए।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "irrigation",
    },
    {
        "Question": "How to improve tomato yield?",
        "Keywords": "tomato,yield,production",
        "Answer": "Use healthy planting material, suitable soil, balanced nutrition, proper irrigation, and timely pest and disease management.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "yield",
    },
    {
        "Question": "टमाटर की पैदावार कैसे बढ़ाएं?",
        "Keywords": "टमाटर,पैदावार,उत्पादन",
        "Answer": "स्वस्थ रोपण सामग्री, उपयुक्त मिट्टी, संतुलित पोषण, सही सिंचाई और समय पर कीट एवं रोग प्रबंधन करें।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "yield",
    },

    # ============================================================
    # WHEAT
    # ============================================================

    {
        "Question": "How to select wheat seeds?",
        "Keywords": "wheat,seed,selection",
        "Answer": "Choose healthy, certified, and suitable seed varieties recommended for the local growing conditions.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "seed",
    },
    {
        "Question": "गेहूं के लिए बीज कैसे चुनें?",
        "Keywords": "गेहूं,बीज,चयन",
        "Answer": "स्थानीय परिस्थितियों के लिए अनुशंसित स्वस्थ और प्रमाणित बीज का चयन करें।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "seed",
    },
    {
        "Question": "How to manage weeds in wheat?",
        "Keywords": "wheat,weed,weeding",
        "Answer": "Monitor the field regularly and use suitable cultural, mechanical, or recommended weed management practices.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "weed",
    },
    {
        "Question": "गेहूं में खरपतवार कैसे नियंत्रित करें?",
        "Keywords": "गेहूं,खरपतवार,निराई",
        "Answer": "खेत की नियमित निगरानी करें और उपयुक्त कृषि, यांत्रिक या अनुशंसित खरपतवार प्रबंधन उपाय अपनाएं।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "weed",
    },

    # ============================================================
    # RICE
    # ============================================================

    {
        "Question": "When should rice be transplanted?",
        "Keywords": "rice,paddy,transplanting",
        "Answer": "Rice transplanting time depends on the variety, local climate, nursery age, and water availability.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "transplanting",
    },
    {
        "Question": "धान की रोपाई कब करनी चाहिए?",
        "Keywords": "धान,रोपाई,transplanting",
        "Answer": "धान की रोपाई का समय किस्म, स्थानीय मौसम, पौध की अवस्था और पानी की उपलब्धता पर निर्भर करता है।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "transplanting",
    },
    {
        "Question": "How to reduce water use in rice farming?",
        "Keywords": "rice,water,irrigation,water saving",
        "Answer": "Use suitable water management practices and avoid unnecessary continuous flooding.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "water",
    },
    {
        "Question": "धान में पानी की बचत कैसे करें?",
        "Keywords": "धान,पानी,सिंचाई,जल बचत",
        "Answer": "उपयुक्त जल प्रबंधन अपनाएं और आवश्यकता से अधिक लगातार पानी भरने से बचें।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "water",
    },

    # ============================================================
    # MUSTARD
    # ============================================================

    {
        "Question": "How to select mustard seeds?",
        "Keywords": "mustard,seed,selection",
        "Answer": "Select healthy, good-quality, and locally recommended mustard seed varieties.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "seed",
    },
    {
        "Question": "सरसों के बीज का चयन कैसे करें?",
        "Keywords": "सरसों,बीज,चयन",
        "Answer": "स्वस्थ, अच्छी गुणवत्ता वाले और स्थानीय परिस्थितियों के लिए अनुशंसित सरसों के बीज चुनें।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "seed",
    },
    {
        "Question": "How to control aphids in mustard?",
        "Keywords": "mustard,aphid,pest",
        "Answer": "Monitor the crop regularly and use integrated pest management or recommended control measures when needed.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "pest",
    },
    {
        "Question": "सरसों में माहू का नियंत्रण कैसे करें?",
        "Keywords": "सरसों,माहू,कीट",
        "Answer": "फसल की नियमित निगरानी करें और आवश्यकता होने पर एकीकृत कीट प्रबंधन या अनुशंसित नियंत्रण उपाय अपनाएं।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "pest",
    },

    # ============================================================
    # POTATO
    # ============================================================

    {
        "Question": "When should potato be planted?",
        "Keywords": "potato,planting,sowing",
        "Answer": "Potato planting time depends on the local climate, season, variety, and production conditions.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "sowing",
    },
    {
        "Question": "आलू की बुवाई कब करें?",
        "Keywords": "आलू,बुवाई,रोपण",
        "Answer": "आलू की बुवाई का समय स्थानीय जलवायु, मौसम, किस्म और उत्पादन परिस्थितियों पर निर्भर करता है।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "sowing",
    },
    {
        "Question": "How to select potato seed tubers?",
        "Keywords": "potato,seed,tuber,selection",
        "Answer": "Use healthy, disease-free, and suitable-quality seed tubers recommended for the growing region.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "seed",
    },
    {
        "Question": "आलू के बीज कंद कैसे चुनें?",
        "Keywords": "आलू,बीज,कंद,चयन",
        "Answer": "स्वस्थ, रोगमुक्त और क्षेत्र के लिए उपयुक्त गुणवत्ता वाले बीज कंद चुनें।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "seed",
    },

    # ============================================================
    # MAIZE
    # ============================================================

    {
        "Question": "When should maize be sown?",
        "Keywords": "maize,corn,sowing,planting",
        "Answer": "Maize sowing time depends on the local climate, season, soil moisture, and production system.",
        "Category": "Maize",
        "Language": "English",
        "Topic": "sowing",
    },
    {
        "Question": "मक्का की बुवाई कब करें?",
        "Keywords": "मक्का,बुवाई,रोपण",
        "Answer": "मक्का की बुवाई का समय स्थानीय जलवायु, मौसम, मिट्टी की नमी और उत्पादन प्रणाली पर निर्भर करता है।",
        "Category": "Maize",
        "Language": "Hindi",
        "Topic": "sowing",
    },
    {
        "Question": "How much water does maize need?",
        "Keywords": "maize,corn,water,irrigation",
        "Answer": "Maize water requirements vary with growth stage, soil, weather, and rainfall.",
        "Category": "Maize",
        "Language": "English",
        "Topic": "irrigation",
    },
    {
        "Question": "मक्का में सिंचाई कैसे करें?",
        "Keywords": "मक्का,सिंचाई,पानी",
        "Answer": "मक्का में सिंचाई फसल की अवस्था, मिट्टी, मौसम और वर्षा के अनुसार करनी चाहिए।",
        "Category": "Maize",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    # ============================================================
    # SOYBEAN
    # ============================================================

    {
        "Question": "When should soybean be sown?",
        "Keywords": "soybean,soya,sowing",
        "Answer": "Soybean sowing time depends on the local rainfall pattern, soil moisture, climate, and variety.",
        "Category": "Soybean",
        "Language": "English",
        "Topic": "sowing",
    },
    {
        "Question": "सोयाबीन की बुवाई कब करें?",
        "Keywords": "सोयाबीन,बुवाई,रोपण",
        "Answer": "सोयाबीन की बुवाई का समय स्थानीय वर्षा, मिट्टी की नमी, जलवायु और किस्म पर निर्भर करता है।",
        "Category": "Soybean",
        "Language": "Hindi",
        "Topic": "sowing",
    },

    # ============================================================
    # ONION
    # ============================================================

    {
        "Question": "When should onion be planted?",
        "Keywords": "onion,planting,sowing",
        "Answer": "Onion planting time depends on the variety, local climate, season, and production method.",
        "Category": "Onion",
        "Language": "English",
        "Topic": "sowing",
    },
    {
        "Question": "प्याज की रोपाई कब करें?",
        "Keywords": "प्याज,रोपाई,बुवाई",
        "Answer": "प्याज की रोपाई का समय किस्म, स्थानीय जलवायु, मौसम और उत्पादन विधि पर निर्भर करता है।",
        "Category": "Onion",
        "Language": "Hindi",
        "Topic": "sowing",
    },

    # ============================================================
    # SOIL
    # ============================================================

    {
        "Question": "Why is soil testing important?",
        "Keywords": "soil,soil testing,nutrients",
        "Answer": "Soil testing helps identify nutrient status and supports more suitable fertilizer and soil management decisions.",
        "Category": "Soil",
        "Language": "English",
        "Topic": "soil",
    },
    {
        "Question": "मिट्टी की जांच क्यों जरूरी है?",
        "Keywords": "मिट्टी,जांच,पोषक तत्व",
        "Answer": "मिट्टी की जांच से पोषक तत्वों की स्थिति समझने और उपयुक्त खाद एवं मिट्टी प्रबंधन का निर्णय लेने में मदद मिलती है।",
        "Category": "Soil",
        "Language": "Hindi",
        "Topic": "soil",
    },
    {
        "Question": "How does soil pH affect crops?",
        "Keywords": "soil,pH,crop,nutrients",
        "Answer": "Soil pH affects nutrient availability and can influence crop growth and fertilizer efficiency.",
        "Category": "Soil",
        "Language": "English",
        "Topic": "soil",
    },
    {
        "Question": "मिट्टी का pH फसल को कैसे प्रभावित करता है?",
        "Keywords": "मिट्टी,pH,फसल,पोषक तत्व",
        "Answer": "मिट्टी का pH पोषक तत्वों की उपलब्धता को प्रभावित करता है और फसल की वृद्धि पर असर डाल सकता है।",
        "Category": "Soil",
        "Language": "Hindi",
        "Topic": "soil",
    },

    # ============================================================
    # WATER MANAGEMENT
    # ============================================================

    {
        "Question": "What are the signs of over irrigation?",
        "Keywords": "irrigation,over irrigation,water",
        "Answer": "Waterlogging, poor root growth, yellowing, and increased disease risk can indicate excessive irrigation.",
        "Category": "Water Management",
        "Language": "English",
        "Topic": "irrigation",
    },
    {
        "Question": "अधिक सिंचाई के क्या नुकसान हैं?",
        "Keywords": "सिंचाई,अधिक पानी,जलभराव",
        "Answer": "जलभराव, जड़ों की खराब वृद्धि, पत्तियों का पीलापन और रोग का बढ़ा जोखिम अधिक सिंचाई के संकेत या परिणाम हो सकते हैं।",
        "Category": "Water Management",
        "Language": "Hindi",
        "Topic": "irrigation",
    },
    {
        "Question": "How does drip irrigation save water?",
        "Keywords": "drip,irrigation,water saving",
        "Answer": "Drip irrigation delivers water closer to the root zone and can reduce unnecessary water loss.",
        "Category": "Water Management",
        "Language": "English",
        "Topic": "water",
    },
    {
        "Question": "ड्रिप सिंचाई से पानी कैसे बचता है?",
        "Keywords": "ड्रिप,सिंचाई,जल बचत",
        "Answer": "ड्रिप सिंचाई पानी को जड़ क्षेत्र के पास पहुंचाती है और अनावश्यक पानी की हानि कम करने में मदद कर सकती है।",
        "Category": "Water Management",
        "Language": "Hindi",
        "Topic": "water",
    },

    # ============================================================
    # WEATHER
    # ============================================================

    {
        "Question": "How can heavy rainfall affect crops?",
        "Keywords": "rainfall,heavy rain,crop,weather",
        "Answer": "Heavy rainfall can cause waterlogging, nutrient loss, erosion, lodging, and increased disease risk.",
        "Category": "Weather",
        "Language": "English",
        "Topic": "rain",
    },
    {
        "Question": "भारी बारिश से फसल को क्या नुकसान हो सकता है?",
        "Keywords": "बारिश,भारी बारिश,फसल,मौसम",
        "Answer": "भारी बारिश से जलभराव, पोषक तत्वों की हानि, मिट्टी का कटाव, फसल गिरना और रोग का जोखिम बढ़ सकता है।",
        "Category": "Weather",
        "Language": "Hindi",
        "Topic": "rain",
    },
    {
        "Question": "How can heat stress affect crops?",
        "Keywords": "heat,temperature,stress,crop",
        "Answer": "High temperatures can increase water demand, reduce growth, affect flowering, and lower crop performance.",
        "Category": "Weather",
        "Language": "English",
        "Topic": "weather",
    },
    {
        "Question": "अधिक गर्मी से फसल पर क्या असर पड़ता है?",
        "Keywords": "गर्मी,तापमान,फसल",
        "Answer": "अधिक तापमान से पानी की आवश्यकता बढ़ सकती है, वृद्धि प्रभावित हो सकती है और फूल आने पर असर पड़ सकता है।",
        "Category": "Weather",
        "Language": "Hindi",
        "Topic": "weather",
    },

    # ============================================================
    # FERTILIZER
    # ============================================================

    {
        "Question": "Why should fertilizer be based on soil testing?",
        "Keywords": "fertilizer,soil test,nutrients,NPK",
        "Answer": "Soil testing helps match fertilizer decisions with nutrient status and can reduce unnecessary fertilizer use.",
        "Category": "Fertilizer",
        "Language": "English",
        "Topic": "fertilizer",
    },
    {
        "Question": "मिट्टी की जांच के आधार पर खाद क्यों डालनी चाहिए?",
        "Keywords": "खाद,मिट्टी जांच,उर्वरक,NPK",
        "Answer": "मिट्टी की जांच से पोषक तत्वों की स्थिति के अनुसार खाद की योजना बनाने और अनावश्यक उपयोग कम करने में मदद मिलती है।",
        "Category": "Fertilizer",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    # ============================================================
    # IPM / PEST
    # ============================================================

    {
        "Question": "What is integrated pest management?",
        "Keywords": "IPM,pest,integrated pest management",
        "Answer": "Integrated pest management combines monitoring, preventive practices, biological methods, and suitable control measures to manage pests.",
        "Category": "Pest",
        "Language": "English",
        "Topic": "IPM",
    },
    {
        "Question": "एकीकृत कीट प्रबंधन क्या है?",
        "Keywords": "IPM,कीट,एकीकृत कीट प्रबंधन",
        "Answer": "एकीकृत कीट प्रबंधन में निगरानी, रोकथाम, जैविक उपाय और आवश्यकता अनुसार उपयुक्त नियंत्रण उपायों का संयोजन किया जाता है।",
        "Category": "Pest",
        "Language": "Hindi",
        "Topic": "IPM",
    },
    {
        "Question": "Why should crops be monitored for pests?",
        "Keywords": "pest,monitoring,crop",
        "Answer": "Regular monitoring helps detect pest problems early and supports timely management decisions.",
        "Category": "Pest",
        "Language": "English",
        "Topic": "pest",
    },
    {
        "Question": "फसल में कीटों की निगरानी क्यों करनी चाहिए?",
        "Keywords": "कीट,निगरानी,फसल",
        "Answer": "नियमित निगरानी से कीट की समस्या को जल्दी पहचानने और समय पर प्रबंधन का निर्णय लेने में मदद मिलती है।",
        "Category": "Pest",
        "Language": "Hindi",
        "Topic": "pest",
    },

    # ============================================================
    # DISEASE
    # ============================================================

    {
        "Question": "How can crop diseases be prevented?",
        "Keywords": "crop,disease,prevention",
        "Answer": "Use healthy planting material, maintain field hygiene, monitor crops regularly, and follow suitable disease management practices.",
        "Category": "Disease",
        "Language": "English",
        "Topic": "disease",
    },
    {
        "Question": "फसल में रोगों से बचाव कैसे करें?",
        "Keywords": "फसल,रोग,रोकथाम",
        "Answer": "स्वस्थ रोपण सामग्री का उपयोग करें, खेत की स्वच्छता बनाए रखें, नियमित निगरानी करें और उपयुक्त रोग प्रबंधन उपाय अपनाएं।",
        "Category": "Disease",
        "Language": "Hindi",
        "Topic": "disease",
    },

    # ============================================================
    # HARVEST / STORAGE
    # ============================================================

    {
        "Question": "Why is timely harvesting important?",
        "Keywords": "harvest,harvesting,crop",
        "Answer": "Timely harvesting can help maintain crop quality and reduce losses caused by over-maturity, weather, pests, or diseases.",
        "Category": "Post Harvest",
        "Language": "English",
        "Topic": "harvest",
    },
    {
        "Question": "समय पर फसल की कटाई क्यों जरूरी है?",
        "Keywords": "कटाई,फसल,harvest",
        "Answer": "समय पर कटाई से फसल की गुणवत्ता बनाए रखने और अधिक पकने, मौसम, कीट या रोग से होने वाले नुकसान को कम करने में मदद मिल सकती है।",
        "Category": "Post Harvest",
        "Language": "Hindi",
        "Topic": "harvest",
    },
    {
        "Question": "How can harvested crops be stored safely?",
        "Keywords": "storage,post harvest,crop",
        "Answer": "Harvested crops should be cleaned, properly dried when appropriate, protected from moisture and pests, and stored in suitable conditions.",
        "Category": "Post Harvest",
        "Language": "English",
        "Topic": "storage",
    },
    {
        "Question": "कटाई के बाद फसल को सुरक्षित कैसे रखें?",
        "Keywords": "भंडारण,कटाई,फसल,post harvest",
        "Answer": "फसल को साफ करें, आवश्यकता अनुसार अच्छी तरह सुखाएं, नमी और कीटों से बचाएं और उपयुक्त परिस्थितियों में भंडारित करें।",
        "Category": "Post Harvest",
        "Language": "Hindi",
        "Topic": "storage",
    },

    # ============================================================
    # FARM MANAGEMENT
    # ============================================================

    {
        "Question": "How can a farmer plan crop production?",
        "Keywords": "farm,planning,crop,production",
        "Answer": "Crop planning should consider soil, climate, water availability, input costs, expected demand, and available resources.",
        "Category": "Farm Management",
        "Language": "English",
        "Topic": "planning",
    },
    {
        "Question": "किसान फसल उत्पादन की योजना कैसे बनाएं?",
        "Keywords": "किसान,फसल,योजना,उत्पादन",
        "Answer": "फसल योजना बनाते समय मिट्टी, जलवायु, पानी की उपलब्धता, लागत, बाजार की मांग और उपलब्ध संसाधनों को ध्यान में रखें।",
        "Category": "Farm Management",
        "Language": "Hindi",
        "Topic": "planning",
    },

    # ============================================================
    # DIGITAL AGRICULTURE / AI
    # ============================================================

    {
        "Question": "How can AI help farmers?",
        "Keywords": "AI,artificial intelligence,farming,farmer",
        "Answer": "AI can support farmers through crop recommendations, weather analysis, disease detection, farm monitoring, and decision support.",
        "Category": "Technology",
        "Language": "English",
        "Topic": "AI",
    },
    {
        "Question": "AI किसानों की कैसे मदद कर सकता है?",
        "Keywords": "AI,कृत्रिम बुद्धिमत्ता,किसान,खेती",
        "Answer": "AI फसल सिफारिश, मौसम विश्लेषण, रोग पहचान, खेत की निगरानी और निर्णय सहायता में किसानों की मदद कर सकता है।",
        "Category": "Technology",
        "Language": "Hindi",
        "Topic": "AI",
    },
    {
        "Question": "What is precision farming?",
        "Keywords": "precision farming,smart farming,technology",
        "Answer": "Precision farming uses data and technology to manage crops and farm inputs more efficiently according to field conditions.",
        "Category": "Technology",
        "Language": "English",
        "Topic": "smart farming",
    },
    {
        "Question": "प्रिसीजन फार्मिंग क्या है?",
        "Keywords": "प्रिसीजन फार्मिंग,स्मार्ट खेती,तकनीक",
        "Answer": "प्रिसीजन फार्मिंग में डेटा और तकनीक की मदद से खेत की परिस्थितियों के अनुसार फसल और कृषि संसाधनों का अधिक प्रभावी प्रबंधन किया जाता है।",
        "Category": "Technology",
        "Language": "Hindi",
        "Topic": "smart farming",
    },
]   
    # ============================================================
# PHASE 5 - RAG 2.0
# CROP-SPECIFIC AGRICULTURE KNOWLEDGE
# ============================================================
additional_records = [

    # ========================================================
    # TOMATO
    # ========================================================

    {
        "Question": "टमाटर में कौन सी खाद डालें?",
        "Keywords": "टमाटर,खाद,उर्वरक,fertilizer",
        "Answer": "टमाटर में खाद का चयन मिट्टी की जांच और फसल की अवस्था के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश वाले उर्वरकों का उपयोग किया जा सकता है।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for tomato?",
        "Keywords": "tomato,fertilizer,fertiliser",
        "Answer": "For tomato, select fertilizer based on soil testing and crop growth stage. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "टमाटर में कितनी बार सिंचाई करें?",
        "Keywords": "टमाटर,सिंचाई,पानी,irrigation",
        "Answer": "टमाटर में सिंचाई मिट्टी की नमी, मौसम और फसल की अवस्था के अनुसार करें। मिट्टी को बहुत अधिक सूखने या लगातार जलभराव से बचाएँ।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    {
        "Question": "How often should tomato be irrigated?",
        "Keywords": "tomato,irrigation,water",
        "Answer": "Irrigate tomato according to soil moisture, weather, and crop growth stage. Avoid both excessive drying and prolonged waterlogging.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "irrigation",
    },

    {
        "Question": "टमाटर के लिए कैसी मिट्टी अच्छी होती है?",
        "Keywords": "टमाटर,मिट्टी,soil",
        "Answer": "टमाटर के लिए अच्छी जल निकासी वाली उपजाऊ मिट्टी उपयुक्त होती है। मिट्टी की जांच के आधार पर पोषक तत्वों और pH का प्रबंधन करें।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "soil",
    },

    {
        "Question": "What type of soil is suitable for tomato?",
        "Keywords": "tomato,soil",
        "Answer": "Tomato grows well in fertile, well-drained soil. Soil testing can be used to manage nutrient availability and soil pH.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "soil",
    },

    {
        "Question": "टमाटर में कीटों से कैसे बचाव करें?",
        "Keywords": "टमाटर,कीट,pest,कीड़ा",
        "Answer": "टमाटर की फसल में नियमित रूप से कीटों की निगरानी करें। संक्रमित पौधों और पत्तियों की पहचान करके उचित एकीकृत कीट प्रबंधन अपनाएँ।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "pest",
    },

    {
        "Question": "How can tomato pests be managed?",
        "Keywords": "tomato,pest,insect",
        "Answer": "Monitor tomato plants regularly for pests and use appropriate integrated pest management practices based on the identified pest.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "pest",
    },


    # ========================================================
    # WHEAT
    # ========================================================

    {
        "Question": "गेहूं में कौन सी खाद डालें?",
        "Keywords": "गेहूं,खाद,उर्वरक,wheat,fertilizer",
        "Answer": "गेहूं में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for wheat?",
        "Keywords": "wheat,fertilizer",
        "Answer": "For wheat, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "गेहूं में सिंचाई कब करें?",
        "Keywords": "गेहूं,सिंचाई,पानी,wheat,irrigation",
        "Answer": "गेहूं में सिंचाई मिट्टी की नमी, मौसम और फसल की अवस्था के अनुसार करें। महत्वपूर्ण वृद्धि अवस्थाओं पर पर्याप्त नमी बनाए रखना आवश्यक है।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    {
        "Question": "How should wheat be irrigated?",
        "Keywords": "wheat,irrigation,water",
        "Answer": "Irrigate wheat according to soil moisture, weather, and crop growth stage. Maintain adequate moisture during important crop growth stages.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "irrigation",
    },


    # ========================================================
    # RICE
    # ========================================================

    {
        "Question": "धान में कौन सी खाद डालें?",
        "Keywords": "धान,खाद,उर्वरक,rice,fertilizer",
        "Answer": "धान में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for rice?",
        "Keywords": "rice,fertilizer",
        "Answer": "For rice, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "धान में सिंचाई और पानी का प्रबंधन कैसे करें?",
        "Keywords": "धान,सिंचाई,पानी,rice,irrigation",
        "Answer": "धान में पानी का प्रबंधन मिट्टी, मौसम और खेती की पद्धति के अनुसार करें। अनावश्यक रूप से लगातार अधिक पानी रखने से बचें।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    {
        "Question": "How should water be managed in rice?",
        "Keywords": "rice,water,irrigation",
        "Answer": "Manage water in rice according to soil, weather, and cultivation method. Avoid keeping excessive water continuously when it is not required.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "irrigation",
    },


    # ========================================================
    # POTATO
    # ========================================================

    {
        "Question": "आलू में कौन सी खाद डालें?",
        "Keywords": "आलू,खाद,उर्वरक,potato,fertilizer",
        "Answer": "आलू में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित नाइट्रोजन, फास्फोरस और पोटाश पोषण बनाए रखें।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for potato?",
        "Keywords": "potato,fertilizer",
        "Answer": "For potato, select fertilizer based on soil testing and crop requirements. Maintain balanced nitrogen, phosphorus, and potassium nutrition.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "आलू में सिंचाई कैसे करें?",
        "Keywords": "आलू,सिंचाई,पानी,potato,irrigation",
        "Answer": "आलू में सिंचाई मिट्टी की नमी और मौसम के अनुसार करें। जलभराव से बचें और फसल की वृद्धि अवस्था के अनुसार पानी दें।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    {
        "Question": "How should potato be irrigated?",
        "Keywords": "potato,irrigation,water",
        "Answer": "Irrigate potato according to soil moisture and weather. Avoid waterlogging and provide water according to the crop growth stage.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "irrigation",
    },


    # ========================================================
    # MUSTARD
    # ========================================================

    {
        "Question": "सरसों में कौन सी खाद डालें?",
        "Keywords": "सरसों,खाद,उर्वरक,mustard,fertilizer",
        "Answer": "सरसों में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए आवश्यक पोषक तत्वों की पूर्ति करें।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for mustard?",
        "Keywords": "mustard,fertilizer",
        "Answer": "For mustard, select fertilizer according to soil testing and crop requirements and maintain balanced crop nutrition.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "सरसों में सिंचाई कैसे करें?",
        "Keywords": "सरसों,सिंचाई,पानी,mustard,irrigation",
        "Answer": "सरसों में सिंचाई मिट्टी की नमी, मौसम और फसल की अवस्था के अनुसार करें। अनावश्यक अधिक सिंचाई और जलभराव से बचें।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "irrigation",
    },

    {
        "Question": "How should mustard be irrigated?",
        "Keywords": "mustard,irrigation,water",
        "Answer": "Irrigate mustard according to soil moisture, weather, and crop growth stage. Avoid unnecessary excessive irrigation and waterlogging.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "irrigation",
    },
]
NEW_RECORDS = [
        # ============================================================
    # PHASE 5 - CROP-SPECIFIC FERTILIZER KNOWLEDGE
    # ============================================================

    {
        "Question": "टमाटर में कौन सी खाद डालें?",
        "Keywords": "टमाटर,खाद,उर्वरक,fertilizer",
        "Answer": "टमाटर में खाद का चयन मिट्टी की जांच और फसल की अवस्था के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश वाले उर्वरकों का उपयोग किया जा सकता है।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for tomato?",
        "Keywords": "tomato,fertilizer,fertiliser",
        "Answer": "For tomato, select fertilizer based on soil testing and crop growth stage. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "गेहूं में कौन सी खाद डालें?",
        "Keywords": "गेहूं,खाद,उर्वरक,wheat,fertilizer",
        "Answer": "गेहूं में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for wheat?",
        "Keywords": "wheat,fertilizer",
        "Answer": "For wheat, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "धान में कौन सी खाद डालें?",
        "Keywords": "धान,खाद,उर्वरक,rice,fertilizer",
        "Answer": "धान में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for rice?",
        "Keywords": "rice,fertilizer",
        "Answer": "For rice, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "आलू में कौन सी खाद डालें?",
        "Keywords": "आलू,खाद,उर्वरक,potato,fertilizer",
        "Answer": "आलू में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित नाइट्रोजन, फास्फोरस और पोटाश पोषण बनाए रखें।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for potato?",
        "Keywords": "potato,fertilizer",
        "Answer": "For potato, select fertilizer based on soil testing and crop requirements. Maintain balanced nitrogen, phosphorus, and potassium nutrition.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "सरसों में कौन सी खाद डालें?",
        "Keywords": "सरसों,खाद,उर्वरक,mustard,fertilizer",
        "Answer": "सरसों में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए आवश्यक पोषक तत्वों की पूर्ति करें।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for mustard?",
        "Keywords": "mustard,fertilizer",
        "Answer": "For mustard, select fertilizer according to soil testing and crop requirements and maintain balanced crop nutrition.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "fertilizer",
    },
]
    # ============================================================
    # CROP-SPECIFIC FERTILIZER KNOWLEDGE
    # ============================================================
additional_records = [
    {
        "Question": "टमाटर में कौन सी खाद डालें?",
        "Keywords": "टमाटर,खाद,उर्वरक,fertilizer",
        "Answer": "टमाटर में खाद का चयन मिट्टी की जांच और फसल की अवस्था के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश वाले उर्वरकों का उपयोग किया जा सकता है।",
        "Category": "Tomato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for tomato?",
        "Keywords": "tomato,fertilizer,fertiliser",
        "Answer": "For tomato, select fertilizer based on soil testing and crop growth stage. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Tomato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "गेहूं में कौन सी खाद डालें?",
        "Keywords": "गेहूं,खाद,उर्वरक,wheat,fertilizer",
        "Answer": "गेहूं में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Wheat",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for wheat?",
        "Keywords": "wheat,fertilizer",
        "Answer": "For wheat, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Wheat",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "धान में कौन सी खाद डालें?",
        "Keywords": "धान,खाद,उर्वरक,rice,fertilizer",
        "Answer": "धान में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए नाइट्रोजन, फास्फोरस और पोटाश का उपयोग किया जा सकता है।",
        "Category": "Rice",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for rice?",
        "Keywords": "rice,fertilizer",
        "Answer": "For rice, select fertilizer according to soil testing and crop requirements. Balanced nitrogen, phosphorus, and potassium nutrition can be used.",
        "Category": "Rice",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "आलू में कौन सी खाद डालें?",
        "Keywords": "आलू,खाद,उर्वरक,potato,fertilizer",
        "Answer": "आलू में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित नाइट्रोजन, फास्फोरस और पोटाश पोषण बनाए रखें।",
        "Category": "Potato",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for potato?",
        "Keywords": "potato,fertilizer",
        "Answer": "For potato, select fertilizer based on soil testing and crop requirements. Maintain balanced nitrogen, phosphorus, and potassium nutrition.",
        "Category": "Potato",
        "Language": "English",
        "Topic": "fertilizer",
    },

    {
        "Question": "सरसों में कौन सी खाद डालें?",
        "Keywords": "सरसों,खाद,उर्वरक,mustard,fertilizer",
        "Answer": "सरसों में उर्वरक का चयन मिट्टी की जांच और फसल की आवश्यकता के आधार पर करें। संतुलित पोषण के लिए आवश्यक पोषक तत्वों की पूर्ति करें।",
        "Category": "Mustard",
        "Language": "Hindi",
        "Topic": "fertilizer",
    },

    {
        "Question": "What fertilizer should be used for mustard?",
        "Keywords": "mustard,fertilizer",
        "Answer": "For mustard, select fertilizer according to soil testing and crop requirements and maintain balanced crop nutrition.",
        "Category": "Mustard",
        "Language": "English",
        "Topic": "fertilizer",
    },
]



def load_existing_records():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        return list(reader)


def record_key(record):
    question = (record.get("Question") or "").strip().lower()
    language = (record.get("Language") or "").strip().lower()

    return question, language


def main():

    print("=" * 70)
    print("AGRISMART AI - DATASET AUGMENTATION")
    print("=" * 70)

    existing_records = load_existing_records()

    print("Existing records :", len(existing_records))
    print("New records      :", len(NEW_RECORDS))

    existing_keys = {
        record_key(record)
        for record in existing_records
    }

    added_records = []
    skipped_records = []

    for record in NEW_RECORDS:

        key = record_key(record)

        if key in existing_keys:
            skipped_records.append(record)
            continue

        added_records.append(record)
        existing_keys.add(key)

    final_records = existing_records + added_records

    fieldnames = [
        "Question",
        "Keywords",
        "Answer",
        "Category",
        "Language",
        "Topic",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for record in final_records:

            writer.writerow({
                "Question": (record.get("Question") or "").strip(),
                "Keywords": (record.get("Keywords") or "").strip(),
                "Answer": (record.get("Answer") or "").strip(),
                "Category": (record.get("Category") or "").strip(),
                "Language": (record.get("Language") or "").strip(),
                "Topic": (record.get("Topic") or "").strip(),
            })

    print("\n" + "=" * 70)
    print("AUGMENTATION COMPLETE")
    print("=" * 70)

    print("Added records     :", len(added_records))
    print("Skipped duplicates:", len(skipped_records))
    print("Final records     :", len(final_records))
    print("Dataset           :", OUTPUT_FILE)

    print("\nAdded questions:")

    for index, record in enumerate(added_records, start=1):
        print(
            f"{index:02d}. "
            f"[{record['Language']}] "
            f"{record['Question']}"
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()