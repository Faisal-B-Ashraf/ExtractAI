def get_prompts():
    """
    Returns task-specific prompts and instructions for extracting data from documents.
    """
    return {
        "Dam_Name": {
    "system_message": "You are an assistant that extracts the name of the dam, project, lock, or relevant structure mentioned in the document.",
    "user_preamble": (
        "Extract the name of the dam, project, lock, or relevant structure explicitly mentioned in the text.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the name of the dam here]\n"
        "- Context: [Provide any additional details or notes about the dam, if available]\n"
        "Do not combine Value and Context into a single field. Separate them clearly."
    )
},
        "Location": {
    "system_message": "Extract the location of the dam or project as explicitly stated in the document.",
    "user_preamble": (
        "Extract the location of the dam or project as follows:\n\n"
        "- Value: Provide the geographic location explicitly mentioned in the document, such as the nearest city, state, river, or specific geographic coordinates.\n"
        "- Context: Provide additional details or inferred information based on nearby landmarks or references.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the location here]\n"
        "- Context: [Provide additional notes or clarifications]\n"
        "Do not combine Value and Context into a single field. Separate them clearly."
    )
}
,"County": {
    "system_message": "Extract the county or counties where the dam or project is located, as mentioned in the document.",
    "user_preamble": (
        "Extract the county information as follows:\n\n"
        "- Value: Provide the name of the county or counties explicitly mentioned in the document where the dam or project is located.\n"
        "- Context: If no county information is explicitly provided, return 'Not mentioned' as the value and explain why in the context.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the county name(s) here]\n"
        "- Context: [Provide relevant notes or clarifications]\n"
        "Do not combine Value and Context into a single field. Separate them clearly."
    )
}
,"Primary_Purpose": {
    "system_message": "Identify the primary purpose of the dam or project as described in the document.",
    "user_preamble": (
        "Extract the primary purpose of the dam or project as follows:\n\n"
        "- Value: Provide the primary purpose of the dam or project (e.g., flood control, hydropower, navigation, irrigation, recreation, water supply, or environmental conservation).\n"
        "- Context: If multiple purposes are mentioned, identify the primary one based on the text's emphasis. Provide additional details or justifications.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the primary purpose here]\n"
        "- Context: [Provide additional notes or justifications]\n"
        "Do not combine Value and Context into a single field. Separate them clearly."
    )
}
,
        "Minimum_Flow": {
    "system_message": "Analyze dam flow requirements from the Water Control Manual (WCM) or FERC license documents. Extract the single most operationally critical minimum flow value and provide detailed context.",
    "user_preamble": (
        "Extract the minimum flow information as follows:\n\n"
        "- Value: Provide only the single most critical minimum flow value explicitly stated in the document. Ensure the value is in cubic feet per second (cfs). Do not include any context here.\n"
        "- Context: Provide detailed explanations, including:\n"
        "  - Type of flow (e.g., instantaneous, daily, weekly average).\n"
        "  - Conditions or regulatory requirements tied to the flow (e.g., seasonal needs, inflow thresholds, fish spawning mandates).\n"
        "  - Timeframes or situations (e.g., 'Nov 1 - Jan 15 for chum spawning').\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the flow value here]\n"
        "- Context: [Provide detailed context and explanations about the flow here]\n"
        "Do not combine Value and Context into a single field. They must be separated clearly."
    )
},
        "Usable_Storage_Volume": {
    "system_message": "Analyze the document for storage volumes associated with the dam or reservoir. Extract usable storage volume if explicitly stated, or infer it based on operational pool ranges, total storage, and flood storage data provided in the document.",
    "user_preamble": (
        "Extract the usable storage volume as follows:\n\n"
        "- Value: Provide the operationally usable storage volume explicitly stated in the document, converted to acre-feet.\n"
        "- Context: If no explicit value is provided, infer the usable storage volume using the following methodology:\n"
        "  - If operational pool ranges are provided (e.g., minimum and maximum pool elevations), calculate the usable storage volume based on storage at these elevations.\n"
        "  - Use the formula: Usable Storage Volume = Total Storage Volume - Dead Storage Volume - Flood Storage Volume (if explicitly mentioned).\n"
        "- Include the following details in the context:\n"
        "  - Specific terms or values used (e.g., 'total storage,' 'active storage,' 'flood storage') and their definitions as provided in the document.\n"
        "  - Elevations or ranges associated with the storage components.\n"
        "  - Explicit mention of whether flood storage is included or excluded in the calculation.\n"
        "  - Any assumptions made or ambiguities identified in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the storage volume here]\n"
        "- Context: [Provide additional notes, calculations, or clarifications]\n"
        "Do not combine Value and Context into a single field. Separate them clearly."
    )
},
        "Stream_Temperature": {
    "system_message": "You are an assistant tasked with analysing stream temperature management for dams. Your goal is to extract key details about temperature regulation, infrastructure, and ecological considerations explicitly mentioned in the document.",
    "user_preamble": (
        "Extract information related to stream temperature management as follows:\n\n"
        "- Value: Provide a summary of whether the stream temperature is actively managed and, if so, how.\n"
        "- Context: Provide detailed answers to the following questions:\n"
        "  1. Does the release of water need to be managed to control water temperature downstream?\n"
        "  2. What specific regulations are in place with regards to downstream temperature?\n"
        "  3. Does the reservoir become stratified? If so, provide details.\n"
        "  4. Does the dam have selective withdrawal infrastructure to control water release temperature? If yes, describe it.\n"
        "  5. What is the primary reason for the stream temperature control (e.g., fish habitats, ecological factors, thermoelectric power plants)?\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert a short summary about whether stream temperature is actively managed]\n"
        "- Context: [Provide detailed answers to the five questions in the format specified above]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Maximum_Pool_Elevation": {
    "system_message": "You are an assistant tasked with extracting and converting maximum pool elevation data for hydropower reservoirs. Your goal is to extract elevation values and ensure they are expressed in feet (ft), while documenting any details explicitly stated in the document in the context field.",
    "user_preamble": (
        "Extract the maximum pool elevation information as follows:\n\n"
        "- Value: Provide the maximum pool elevation converted to feet (ft), even if the original value is in meters or another unit. Use the conversion factor: 1 meter = 3.28084 feet. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. The original value and unit as mentioned in the document (e.g., meters or any other unit).\n"
        "  2. Any purpose, conditions, or constraints related to this elevation explicitly described in the document.\n"
        "  3. References to other elevations explicitly mentioned in the document.\n"
        "  4. Any regulatory or safety requirements tied to this elevation explicitly stated in the document.\n"
        "  5. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the maximum pool elevation here in feet (ft) or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Normal_Maximum_Operating_Pool_Level": {
    "system_message": "You are an assistant tasked with extracting the Normal Maximum Operating Pool Level from hydropower-related documents. This level reflects the highest water level typically maintained under normal operating conditions.",
    "user_preamble": (
        "Extract the Normal Maximum Operating Pool Level information as follows:\n\n"
        "- Value: Provide the Normal Maximum Operating Pool Level converted to feet (ft), even if the original value is in meters or another unit. Use the conversion factor: 1 meter = 3.28084 feet. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. The original value and unit as mentioned in the document (e.g., meters or any other unit).\n"
        "  2. Any explicitly stated operational purpose, constraints, or conditions tied to this level.\n"
        "  3. References to other water levels (e.g., flood surcharge level, minimum operating level) if explicitly mentioned.\n"
        "  4. Any regulatory or safety requirements directly tied to this level explicitly stated in the document.\n"
        "  5. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Normal Maximum Operating Pool Level here in feet (ft) or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Maximum_Operating_Pool_Level": {
    "system_message": "You are an assistant tasked with extracting the Maximum Operating Pool Level from hydropower-related documents. This level represents the highest water level that can be maintained during controlled operations under safe conditions.",
    "user_preamble": (
        "Extract the Maximum Operating Pool Level information as follows:\n\n"
        "- Value: Provide the Maximum Operating Pool Level converted to feet (ft), even if the original value is in meters or another unit. Use the conversion factor: 1 meter = 3.28084 feet. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. The original value and unit as mentioned in the document (e.g., meters or any other unit).\n"
        "  2. Any explicitly stated operational purpose, constraints, or conditions tied to this level.\n"
        "  3. References to other water levels (e.g., Normal Maximum Operating Pool Level, Maximum Pool Elevation) if explicitly mentioned.\n"
        "  4. Any regulatory or safety requirements directly tied to this level explicitly stated in the document.\n"
        "  5. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Maximum Operating Pool Level here in feet (ft) or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Minimum_Pool_Elevation": {
    "system_message": "You are an assistant tasked with extracting the Minimum Pool Elevation from hydropower-related documents. This level represents the lowest water elevation at which normal operations can be maintained.",
    "user_preamble": (
        "Extract the Minimum Pool Elevation information as follows:\n\n"
        "- Value: Provide the Minimum Pool Elevation converted to feet (ft), even if the original value is in meters or another unit. Use the conversion factor: 1 meter = 3.28084 feet. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. The original value and unit as mentioned in the document (e.g., meters or any other unit).\n"
        "  2. Any explicitly stated operational purpose, constraints, or conditions tied to this level.\n"
        "  3. References to other water levels (e.g., normal or maximum pool levels) explicitly mentioned in the document.\n"
        "  4. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Minimum Pool Elevation here in feet (ft) or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Power_Head": {
    "system_message": "You are an assistant tasked with extracting the Power Head from hydropower-related documents. This refers to the effective vertical height of water available to drive the turbines.",
    "user_preamble": (
        "Extract the Power Head information as follows:\n\n"
        "- Value: Provide the Power Head converted to feet (ft), even if the original value is in meters or another unit. Use the conversion factor: 1 meter = 3.28084 feet. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. The original value and unit as mentioned in the document (e.g., meters or any other unit).\n"
        "  2. Any explicitly stated operational conditions or constraints tied to the power head.\n"
        "  3. References to other related metrics (e.g., pool elevations) explicitly mentioned in the document.\n"
        "  4. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Power Head here in feet (ft) or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Power_Capacity": {
    "system_message": "You are an assistant tasked with extracting the Power Capacity of a hydropower plant from relevant documents. This refers to the total installed turbine capacity in megawatts (MW).",
    "user_preamble": (
        "Extract the Power Capacity information as follows:\n\n"
        "- Value: Provide the Power Capacity in megawatts (MW) as explicitly stated in the document. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. Any references to individual turbine capacities or total installed capacity.\n"
        "  2. Additional operational details explicitly tied to the power capacity.\n"
        "  3. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Power Capacity here in MW or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Annual_Flow_Peak": {
    "system_message": "You are an assistant tasked with extracting the Annual Flow Peak from hydropower-related documents. This represents the highest flow rate measured during a year.",
    "user_preamble": (
        "Extract the Annual Flow Peak information as follows:\n\n"
        "- Value: Provide the Annual Flow Peak in cubic feet per second (cfs) as explicitly stated in the document. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. Any references to specific timeframes, conditions, or events tied to the peak flow.\n"
        "  2. Any regulatory or operational details explicitly associated with the peak flow.\n"
        "  3. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Annual Flow Peak here in cfs or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Annual_Flow_Mean": {
    "system_message": "You are an assistant tasked with extracting the Annual Flow Mean from hydropower-related documents. This represents the average flow rate over a year.",
    "user_preamble": (
        "Extract the Annual Flow Mean information as follows:\n\n"
        "- Value: Provide the Annual Flow Mean in cubic feet per second (cfs) as explicitly stated in the document. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. Any references to specific timeframes or averaging methods used.\n"
        "  2. Any regulatory or operational details explicitly associated with the mean flow.\n"
        "  3. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Annual Flow Mean here in cfs or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Spillway_Maximum_Discharge_Flow": {
    "system_message": "You are an assistant tasked with extracting the Spillway Maximum Discharge Flow from hydropower-related documents. This represents the maximum flow capacity of the spillway.",
    "user_preamble": (
        "Extract the Spillway Maximum Discharge Flow information as follows:\n\n"
        "- Value: Provide the maximum discharge flow in cubic feet per second (cfs) as explicitly stated in the document. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. Any conditions, scenarios, or constraints tied to the spillway's maximum capacity.\n"
        "  2. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Spillway Maximum Discharge Flow here in cfs or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
},
        "Energy_Output": {
    "system_message": "You are an assistant tasked with extracting the Energy Output from hydropower-related documents. This refers to the estimated annual generation in megawatt-hours (MWh).",
    "user_preamble": (
        "Extract the Energy Output information as follows:\n\n"
        "- Value: Provide the estimated annual energy generation in megawatt-hours (MWh) as explicitly stated in the document. If no value is provided, return 'Not mentioned'.\n"
        "- Context: Provide only information explicitly stated in the document, including:\n"
        "  1. Any details regarding how the energy output was estimated.\n"
        "  2. If no relevant details are found, return 'Not mentioned'.\n\n"
        "Do not infer or interpret any information not directly stated in the document.\n\n"
        "Ensure your output strictly follows this format:\n"
        "- Value: [Insert the Energy Output here in MWh or 'Not mentioned']\n"
        "- Context: [Provide only explicitly stated details from the document]\n"
        "Do not combine Value and Context into a single field. Keep them separate."
    )
}

    }
