import re
from cvss import CVSS2, CVSS3, CVSS4

# 定义CVSS2向量的标准顺序及其有效值
cvss2_vector_structure = {
    'AV': ['L', 'A', 'N'],
    'AC': ['H', 'M', 'L'],
    'Au': ['N', 'S', 'M'],
    'C': ['N', 'P', 'C'],
    'I': ['N', 'P', 'C'],
    'A': ['N', 'P', 'C'],
    'E': ['U', 'POC', 'F', 'H', 'ND'],
    'RL': ['OF', 'TF', 'W', 'U', 'ND'],
    'RC': ['UC', 'UR', 'C', 'ND'],
    'CDP': ['N', 'L', 'LM', 'MH', 'H', 'ND'],
    'TD': ['N', 'L', 'M', 'H', 'ND'],
    'CR': ['L', 'M', 'H', 'ND'],
    'IR': ['L', 'M', 'H', 'ND'],
    'AR': ['L', 'M', 'H', 'ND']
}

cvss20_full_values = {
    'AV': {'Network': 'N', 'Adjacent Network': 'A', 'Local': 'L'},
    'AC': {'Low': 'L', 'Medium': 'M', 'High': 'H'},
    'AU': {'None': 'N', 'Single': 'S', 'Multiple': 'M'},
    'C': {'None': 'N', 'Partial': 'P', 'Complete': 'C'},
    'I': {'None': 'N', 'Partial': 'P', 'Complete': 'C'},
    'A': {'None': 'N', 'Partial': 'P', 'Complete': 'C'},
    'E': {'Not Defined': 'ND', 'Unproven': 'U', 'Proof-of-Concept': 'POC',
          'Functional': 'F', 'High': 'H', 'Unproven that exploit exists': 'U',
          'Proof of concept code': 'POC', 'Functional exploit exists': 'F'},
    'RL': {'Not Defined': 'ND', 'Official Fix': 'OF', 'Official fix': 'OF',
           'Temporary Fix': 'TF', 'Temporary fix': 'TF', 'Workaround': 'W', 'Unavailable': 'U'},
    'RC': {'Not Defined': 'ND', 'Unconfirmed': 'UC', 'Uncorroborated': 'UR', 'Confirmed': 'C'},
    'CDP': {'Not Defined': 'ND', 'None': 'N', 'Low': 'L', 'light loss': 'L', 'Low (light loss)': 'L',
            'Low-Medium': 'LM', 'Medium-High': 'MH',
            'High': 'H', 'catastrophic loss': 'H', 'High (catastrophic loss)': 'H'},
    'TD': {'Not Defined': 'ND', 'None': 'N', 'Low': 'L', 'Medium': 'M', 'High': 'H'},
    'CR': {'Not Defined': 'ND', 'Low': 'L', 'Medium': 'M', 'High': 'H'},
    'IR': {'Not Defined': 'ND', 'Low': 'L', 'Medium': 'M', 'High': 'H'},
    'AR': {'Not Defined': 'ND', 'Low': 'L', 'Medium': 'M', 'High': 'H'}
}

cvss20_vector_fullnames = {
    'Access Vector': 'AV',
    'Access Vector (AV)': 'AV',
    'AV': 'AV',
    'Access Complexity': 'AC',
    'Access Complexity (AC)': 'AC',
    'AC': 'AC',
    'Authentication': 'Au',
    'Authentication (AU)': 'Au',
    'Au': 'Au',
    'Confidentiality': 'C',
    'Confidentiality (C)': 'C',
    'Confidentiality Impact': 'C',
    'Confidentiality Impact (C)': 'C',
    'C': 'C',
    'Integrity': 'I',
    'Integrity (I)': 'I',
    'Integrity Impact': 'I',
    'Integrity Impact (I)': 'I',
    'I': 'I',
    'Availability': 'A',
    'Availability (A)': 'A',
    'Availability Impact': 'A',
    'Availability Impact (A)': 'A',
    'A': 'A',
    'Exploitability': 'E',
    'Exploitability (E)': 'E',
    'Exploit Code Maturity': 'E',
    'Exploit Code Maturity (E)': 'E',
    'Exploit Maturity': 'E',
    'Exploit Maturity (E)': 'E',
    'E': 'E',
    'Remediation Level': 'RL',
    'Remediation Level (RL)': 'RL',
    'RL': 'RL',
    'Report Confidence': 'RC',
    'Report Confidence (RC)': 'RC',
    'RC': 'RC',
    'Collateral Damage Potential': 'CDP',
    'Collateral Damage Potential (CDP)': 'CDP',
    'CDP': 'CDP',
    'Target Distribution': 'TD',
    'Target Distribution (TD)': 'TD',
    'TD': 'TD',
    'Confidentiality Requirement': 'CR',
    'Confidentiality Requirement (CR)': 'CR',
    'CR': 'CR',
    'Integrity Requirement': 'IR',
    'Integrity Requirement (IR)': 'IR',
    'IR': 'IR',
    'Availability Requirement': 'AR',
    'Availability Requirement (AR)': 'AR',
    'AR': 'AR'
}

# cvss2_pattern = re.compile(
#     r"^AV:[NAL]/AC:[LMH]/Au:[MSN]/C:[NPC]/I:[NPC]/A:[NPC]"  # 可用性影响
#     r"(/E:(U|POC|F|H|ND))?(/RL:(OF|TF|W|U|ND))?"  # 报告时间
#     r"(/RC:(UC|UR|C|ND))?(/CDP:(N|L|LM|MH|H|ND))?"  # 受影响的数据流
#     r"(/TD:(N|L|M|H|ND))?(/CR:(L|M|H|ND))?"  # 残余的保密性影响
#     r"(/IR:(L|M|H|ND))?(/AR:(L|M|H|ND))?$"
# )
# 正则表达式匹配CVSS2向量格式
cvss2_pattern = re.compile(r'^(AV:[LAN]/AC:[HML]/Au:[NSM]/C:[NPC]/I:[NPC]/A:[NPC])')

# 定义CVSS3.0向量的标准顺序及其有效值
cvss3_vector_structure = {
    'AV': ['N', 'A', 'L', 'P'],
    'AC': ['L', 'H'],
    'PR': ['N', 'L', 'H'],
    'UI': ['N', 'R'],
    'S': ['U', 'C'],
    'C': ['H', 'L', 'N'],
    'I': ['H', 'L', 'N'],
    'A': ['H', 'L', 'N'],
    'E': ['X', 'U', 'P', 'F', 'H'],
    'RL': ['X', 'O', 'T', 'W', 'U'],
    'RC': ['X', 'U', 'R', 'C'],
    'CR': ['X', 'H', 'M', 'L'],
    'IR': ['X', 'H', 'M', 'L'],
    'AR': ['X', 'H', 'M', 'L'],
    'MAV': ['X', 'N', 'A', 'L', 'P'],
    'MAC': ['X', 'L', 'H'],
    'MPR': ['X', 'N', 'L', 'H'],
    'MUI': ['X', 'N', 'R'],
    'MS': ['X', 'U', 'C'],
    'MC': ['X', 'H', 'L', 'N'],
    'MI': ['X', 'H', 'L', 'N'],
    'MA': ['X', 'H', 'L', 'N']
}

cvss31_full_values = {
    # Base Metrics
    'AV': {'Network': 'N', 'Adjacent Network': 'A', 'Local': 'L', 'Physical': 'P', 'Adjacent': 'A'},
    'AC': {'Low': 'L', 'High': 'H'},
    'PR': {'None': 'N', 'Low': 'L', 'High': 'H'},
    'UI': {'None': 'N', 'Required': 'R'},
    'S': {'Unchanged': 'U', 'Changed': 'C'},
    'C': {'High': 'H', 'Low': 'L', 'None': 'N'},
    'I': {'High': 'H', 'Low': 'L', 'None': 'N'},
    'A': {'High': 'H', 'Low': 'L', 'None': 'N'},

    # Temporal Metrics
    'E': {'Not Defined': 'X', 'Unproven': 'U', 'Proof-of-Concept': 'P', 'Functional': 'F', 'High': 'H'},
    'RL': {'Not Defined': 'X', 'Official Fix': 'O', 'Temporary Fix': 'T', 'Workaround': 'W', 'Unavailable': 'U'},
    'RC': {'Not Defined': 'X', 'Unknown': 'U', 'Reasonable': 'R', 'Confirmed': 'C'},

    # Environmental Metrics
    'CR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
    'IR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
    'AR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
    'MAV': {'Not Defined': 'X', 'Network': 'N', 'Adjacent Network': 'A', 'Local': 'L', 'Physical': 'P'},
    'MAC': {'Not Defined': 'X', 'Low': 'L', 'High': 'H'},
    'MPR': {'Not Defined': 'X', 'None': 'N', 'Low': 'L', 'High': 'H'},
    'MUI': {'Not Defined': 'X', 'None': 'N', 'Required': 'R'},
    'MS': {'Not Defined': 'X', 'Unchanged': 'U', 'Changed': 'C'},
    'MC': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
    'MI': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
    'MA': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'}
}

cvss31_vector_fullnames = {
    # Base Metrics
    'Attack Vector': 'AV',
    'Attack Vector (AV)': 'AV',
    'AV': 'AV',
    'Attack Complexity': 'AC',
    'Attack Complexity (AC)': 'AC',
    'AC': 'AC',
    'Privileges Required': 'PR',
    'Privileges Required (PR)': 'PR',
    'PR': 'PR',
    'User Interaction': 'UI',
    'User Interaction (UI)': 'UI',
    'UI': 'UI',
    'Scope': 'S',
    'Scope (S)': 'S',
    'S': 'S',
    'Confidentiality (C)': 'C',
    'Confidentiality': 'C',
    'Confidentiality Impact': 'C',
    'Confidentiality Impact (C)': 'C',
    'C': 'C',
    'Integrity (I)': 'I',
    'Integrity': 'I',
    'Integrity Impact': 'I',
    'Integrity Impact (I)': 'I',
    'I': 'I',
    'Availability': 'A',
    'Availability (A)': 'A',
    'Availability Impact': 'A',
    'Availability Impact (A)': 'A',
    'A': 'A',

    # Temporal Metrics
    'Exploit Code Maturity': 'E',
    'Exploit Code Maturity (E)': 'E',
    'Exploit Maturity (E)': 'E',
    'Exploit Maturity': 'E',
    'E': 'E',
    'Remediation Level (RL)': 'RL',
    'Remediation Level': 'RL',
    'RL': 'RL',
    'Report Confidence (RC)': 'RC',
    'Report Confidence': 'RC',
    'RC': 'RC',

    # Environmental Metrics
    'Confidentiality Requirement': 'CR',
    'Confidentiality Requirements (CR)': 'CR',
    'CR': 'CR',
    'Integrity Requirement': 'IR',
    'Integrity Requirements (IR)': 'IR',
    'IR': 'IR',
    'Availability Requirement': 'AR',
    'Availability Requirements (AR)': 'AR',
    'AR': 'AR',
    'Modified Attack Vector': 'MAV',
    'Modified Attack Vector (MAV)': 'MAV',
    'MAV': 'MAV',
    'Modified Attack Complexity': 'MAC',
    'Modified Attack Complexity (MAC)': 'MAC',
    'MAC': 'MAC',
    'Modified Privileges Required': 'MPR',
    'Modified Privileges Required (MPR)': 'MPR',
    'MPR': 'MPR',
    'Modified User Interaction': 'MUI',
    'Modified User Interaction (MUI)': 'MUI',
    'MUI': 'MUI',
    'Modified Scope': 'MS',
    'Modified Scope (MS)': 'MS',
    'MS': 'MS',
    'Modified Confidentiality Impact': 'MC',
    'Modified Confidentiality Impact (MC)': 'MC',
    'MC': 'MC',
    'Modified Integrity Impact': 'MI',
    'Modified Integrity Impact (MI)': 'MI',
    'MI': 'MI',
    'Modified Availability Impact': 'MA',
    'Modified Availability Impact (MA)': 'MA',
    'MA': 'MA'
}

# 正则表达式匹配CVSS3.0向量格式
# cvss3_pattern = re.compile(
#     r"^AV:[NALP]/AC:[LH]/PR:[NLH]/UI:[NR]/S:[UC]/C:[HLN]/I:[HLN]/A:[HLN]"
#     r"(/E:[XUPFH])?(/RL:[XOTWU])?(/RC:[XURC])?"
#     r"(/CR:[XLMH])?(/IR:[XLMH])?(/AR:[XLMH])?"
#     r"(/MAV:[XNALP])?(/MAC:[XLH])?(/MPR:[XUNLH])?(/MUI:[XNR])?(/MS:[XUC])?"
#     r"(/MC:[XNLH])?(/MI:[XNLH])?(/MA:[XNLH])?$"
# )
cvss3_pattern = re.compile(r'^(AV:[NALP]/AC:[LH]/PR:[NLH]/UI:[NR]/S:[UC]/C:[HLN]/I:[HLN]/A:[HLN])')

cvss4_vector_structure = {
    # // Base metrics
    'AV': ['N', 'A', 'L', 'P'],
    'AC': ['L', 'H'],
    'AT': ['N', 'P'],
    'PR': ['N', 'L', 'H'],
    'UI': ['N', 'P', 'A'],
    'VC': ['H', 'L', 'N'],
    'VI': ['H', 'L', 'N'],
    'VA': ['H', 'L', 'N'],
    'SC': ['H', 'L', 'N'],
    'SI': ['H', 'L', 'N'],
    'SA': ['H', 'L', 'N'],
    # Threat Metrics
    'E': ["X", "A", "P", "U"],
    # // Environmental metrics
    'CR': ['X', 'H', 'M', 'L'],
    'IR': ['X', 'H', 'M', 'L'],
    'AR': ['X', 'H', 'M', 'L'],
    'MAV': ['X', 'N', 'A', 'L', 'P'],
    'MAC': ['X', 'L', 'H'],
    'MAT': ['X', 'N', 'P'],
    'MPR': ['X', 'N', 'L', 'H'],
    'MUI': ['X', 'N', 'P', 'A'],
    'MVC': ['X', 'H', 'L', 'N'],
    'MVI': ['X', 'H', 'L', 'N'],
    'MVA': ['X', 'H', 'L', 'N'],
    'MSC': ['X', 'H', 'L', 'N'],
    'MSI': ['X', 'S', 'H', 'L', 'N'],
    'MSA': ['X', 'S', 'H', 'L', 'N'],
    # // Supplemental metrics
    'S': ['X', 'N', 'P'],
    'AU': ['X', 'N', 'Y'],
    'R': ['X', 'A', 'U', 'I'],
    'V': ['X', 'D', 'C'],
    'RE': ['X', 'L', 'M', 'H'],
    'U': ['X', 'Clear', 'Green', 'Amber', 'Red']
}

cvss4_full_values = {'AV': {'Network': 'N', 'Adjacent': 'A', 'Local': 'L', 'Physical': 'P'},
                     'AC': {'Low': 'L', 'High': 'H'},
                     'AT': {'None': 'N', 'Physical': 'P', 'Partial': 'P'},
                     'PR': {'None': 'N', 'Low': 'L', 'High': 'H'},
                     'UI': {'None': 'N', 'Required': 'P', 'All': 'A', "Active": "A", "Passive": "P", 'Partial': 'P'},
                     'VC': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'VI': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'VA': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'SC': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'SI': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'SA': {'High': 'H', 'Low': 'L', 'None': 'N'},
                     'E': {'Not Defined': 'X', 'High': 'A', 'Proof-of-Concept': 'P', 'Unproven': 'U'},
                     'CR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
                     'IR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
                     'AR': {'Not Defined': 'X', 'High': 'H', 'Medium': 'M', 'Low': 'L'},
                     'MAV': {'Not Defined': 'X', 'Network': 'N', 'Adjacent': 'A', 'Local': 'L', 'Physical': 'P', 'Partial': 'P'},
                     'MAC': {'Not Defined': 'X', 'Low': 'L', 'High': 'H'},
                     'MAT': {'Not Defined': 'X', 'None': 'N', 'Physical': 'P'},
                     'MPR': {'Not Defined': 'X', 'None': 'N', 'Low': 'L', 'High': 'H'},
                     'MUI': {'Not Defined': 'X', 'None': 'N', 'Required': 'P', 'All': 'A'},
                     'MVC': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'MVI': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'MVA': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'MSC': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'MSI': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'MSA': {'Not Defined': 'X', 'High': 'H', 'Low': 'L', 'None': 'N'},
                     'S': {'Not Defined': 'X', 'None': 'N', 'Partial': 'P'},
                     'AU': {'Not Defined': 'X', 'None': 'N', 'Yes': 'Y', 'No': 'N'},
                     'R': {'Not Defined': 'X', 'Unavailable': 'A', 'Workaround': 'U', 'Temporary Fix': 'I'},
                     'V': {'Not Defined': 'X', 'Confirmed': 'D', 'Unconfirmed': 'C'},
                     'RE': {'Not Defined': 'X', 'Low': 'L', 'Medium': 'M', 'High': 'H'},
                     'U': {'Not Defined': 'X', 'Clear': 'Clear', 'Green': 'Green', 'Amber': 'Amber', 'Red': 'Red'}
                     }

cvss4_vector_fullnames = {
    'Attack Vector': 'AV',
    'Attack Vector (AV)': 'AV',
    'AV': 'AV',
    'Attack Complexity': 'AC',
    'Attack Complexity (AC)': 'AC',
    'AC': 'AC',
    'Attack Requirements': 'AT',
    'Attack Requirements (AT)': 'AT',
    'AT': 'AT',
    'Privileges Required': 'PR',
    'Privileges Required (PR)': 'PR',
    'PR': 'PR',
    'User Interaction': 'UI',
    'User Interaction (UI)': 'UI',
    'UI': 'UI',
    'Confidentiality (VC)': 'VC',
    'VC': 'VC',
    'Integrity (VI)': 'VI',
    'VI': 'VI',
    'Availability (VA)': 'VA',
    'VA': 'VA',
    'Confidentiality (SC)': 'SC',
    'SC': 'SC',
    'Integrity (SI)': 'SI',
    'SI': 'SI',
    'Availability (SA)': 'SA',
    'SA': 'SA',

    'Exploit Code Maturity': 'E',
    'Exploit Maturity (E)': 'E',
    'E': 'E',
    'Confidentiality Requirement': 'CR',
    'Confidentiality Requirements (CR)': 'CR',
    'CR': 'CR',
    'Integrity Requirement': 'IR',
    'Integrity Requirements (IR)': 'IR',
    'IR': 'IR',
    'Availability Requirement': 'AR',
    'Availability Requirements (AR)': 'AR',
    'AR': 'AR',

    'Modified Attack Vector': 'MAV',
    'Attack Vector (MAV)': 'MAV',
    'MAV': 'MAV',
    'Modified Attack Complexity': 'MAC',
    'Attack Complexity (MAC)': 'MAC',
    'MAC': 'MAC',
    'Modified Attack Requirements': 'MAT',
    'Attack Requirements (MAT)': 'MAT',
    'MAT': 'MAT',
    'Modified Privileges Required': 'MPR',
    'Privileges Required (MPR)': 'MPR',
    'MPR': 'MPR',
    'Modified User Interaction': 'MUI',
    'User Interaction (MUI)': 'MUI',
    'MUI': 'MUI',
    'Modified Confidentiality (VC)': 'MVC',
    'Confidentiality (MVC)': 'MVC',
    'MVC': 'MVC',
    'Modified Integrity (VI)': 'MVI',
    'Integrity (MVI)': 'MVI',
    'MVI': 'MVI',
    'Modified Availability (VA)': 'MVA',
    'Availability (MVA)': 'MVA',
    'MVA': 'MVA',
    'Modified Confidentiality (SC)': 'MSC',
    'Confidentiality (MSC)': 'MSC',
    'MSC': 'MSC',
    'Modified Integrity (SI)': 'MSI',
    'Integrity (MSI)': 'MSI',
    'MSI': 'MSI',
    'Modified Availability (SA)': 'MSA',
    'Availability (MSA)': 'MSA',
    'MSA': 'MSA',

    'Supplemental': 'S',
    'Safety (S)': 'S',
    'S': 'S',
    'Authentication': 'AU',
    'Automatable (AU)': 'AU',
    'AU': 'AU',
    'Remediation Level': 'R',
    'Recovery (R)': 'R',
    'R': 'R',
    'Report Confidence': 'V',
    'Value Density (V)': 'V',
    'V': 'V',
    'Exploitability': 'RE',
    'Vulnerability Response Effort (RE)': 'RE',
    'RE': 'RE',
    'Unusual': 'U',
    'Provider Urgency (U)': 'U',
    'U': 'U'
}

# 正则表达式匹配假设的CVSS4.0向量格式
# cvss4_pattern = re.compile(
#     r'^AV:[NALP]/AC:[LH]/AT:[NP]/PR:[NLH]/UI:[NPA]/VC:[HLN]/VI:[HLN]/VA:[HLN]/SC:[HLN]/SI:[HLN]/SA:[HLN](/E:[XAPU])?(/CR:[XHML])?(/IR:[XHML])?(/AR:[XHML])?(/MAV:[XNALP])?(/MAC:[XLH])?(/MAT:[XNP])?(/MPR:[XNLH])?(/MUI:[XNPA])?(/MVC:[XNLH])?(/MVI:[XNLH])?(/MVA:[XNLH])?(/MSC:[XNLH])?(/MSI:[XNLHS])?(/MSA:[XNLHS])?(/S:[XNP])?(/AU:[XNY])?(/R:[XAUI])?(/V:[XDC])?(/RE:[XLMH])?(/U:(X|Clear|Green|Amber|Red))?$')

cvss4_pattern = re.compile(r'^(AV:[NALP]/AC:[LH]/AT:[NP]/PR:[NLH]/UI:[NPA]/VC:[HLN]/VI:[HLN]/VA:[HLN]/SC:[HLN]/SI:[HLN]/SA:[HLN])')


def is_valid_cvss4_vector(elements):
    """
    检查向量的每个元素值是否有效。
    """
    for key, value in elements.items():
        if key not in cvss4_vector_structure or value not in cvss4_vector_structure[key]:
            return False
    return True


def parse_cvss4_vector(vector):
    """
    解析假设的CVSS4.0向量为字典格式。
    """
    elements = vector.split('/')
    parsed_elements = {}
    for element in elements:
        key, value = element.split(':')
        parsed_elements[key] = value
    return parsed_elements


def correct_cvss4_vector(vector):
    """
    更正假设的CVSS4.0向量的顺序并检查有效性。
    :param vector:
    :return:
    """
    parsed_elements = parse_cvss4_vector(vector)

    if not is_valid_cvss4_vector(parsed_elements):
        return {"state": False}

    corrected_vector = []
    for key in cvss4_vector_structure.keys():
        if key in parsed_elements:
            corrected_vector.append(f"{key}:{parsed_elements[key]}")

    if not cvss4_pattern.match('/'.join(corrected_vector)):
        return {"state": False}

    n_vector = "CVSS:4.0/" + '/'.join(corrected_vector)
    try:
        score = CVSS4(n_vector).base_score
    except Exception as e:
        return {"state": False}
    return {"state": True, "vector": '/'.join(corrected_vector), 'score': score}


def json_data_to_cvss4_vector(json_data):
    """
    将json数据转换为CVSS4.0向量
    :param json_data:
    :return:
    """
    # 生成目标字符串
    result = []
    for key, value in json_data.items():
        short_key = cvss4_vector_fullnames.get(key)
        if short_key:
            short_value = cvss4_full_values.get(short_key, {}).get(value)
            if short_value:
                result.append(f'{short_key}:{short_value}')
            else:
                return {'state': False}
    # 使用斜杠分隔字段
    if not result:
        return {'state': False, 'message': 'No valid values found'}
    output = "/".join(result)
    return correct_cvss4_vector(output)


def is_valid_cvss3_vector(elements):
    """
    检查向量的每个元素值是否有效。
    """
    for key, value in elements.items():
        if key not in cvss3_vector_structure or value not in cvss3_vector_structure[key]:
            return False
    return True


def parse_cvss3_vector(vector):
    """
    解析CVSS3.0向量为字典格式。
    """
    elements = vector.split('/')
    parsed_elements = {}
    for element in elements:
        key, value = element.split(':')
        parsed_elements[key] = value
    return parsed_elements


def correct_cvss3_vector(vector, version):
    """
    更正CVSS3向量的顺序并检查有效性。
    :param vector: 向量
    :param version: 版本3.0、3.1,
    :return:
    """
    parsed_elements = parse_cvss3_vector(vector)
    if not is_valid_cvss3_vector(parsed_elements):
        return {"state": False}

    corrected_vector = []
    for key in cvss3_vector_structure.keys():
        if key in parsed_elements:
            corrected_vector.append(f"{key}:{parsed_elements[key]}")

    if not cvss3_pattern.match('/'.join(corrected_vector)):
        return {"state": False}

    n_vector = '/'.join(corrected_vector)
    if version == 3.0:
        n_vector = "CVSS:3.0/" + n_vector
    elif version == 3.1:
        n_vector = "CVSS:3.1/" + n_vector
    else:
        return {"state": False}
    try:
        score = float(CVSS3(n_vector).base_score)
    except Exception as e:
        return {"state": False}
    return {"state": True, "vector": '/'.join(corrected_vector), "score": score}


def json_data_to_cvss31_vector(json_data):
    """
    接收CVSS字典数据并将其转换为CVSS3.1向量。
    :param json_data:
    :return:
    """

    # 生成目标字符串
    result = []
    for key, value in json_data.items():
        short_key = cvss31_vector_fullnames.get(key)
        if short_key:
            short_value = cvss31_full_values.get(short_key, {}).get(value)
            if short_value:
                result.append(f'{short_key}:{short_value}')
            else:
                return {'state': False, 'message': f'Value "{value}" for "{key}" is not valid'}
    if not result:
        return {'state': False, 'message': 'No valid values found'}
    # 使用斜杠分隔字段
    output = "/".join(result)
    return correct_cvss3_vector(output, 3.1)


def is_valid_cvss2_vector(elements):
    """
    检查向量的每个元素值是否有效。
    """
    for key, value in elements.items():
        if key not in cvss2_vector_structure or value not in cvss2_vector_structure[key]:
            return False
    return True


def parse_cvss2_vector(vector):
    """
    解析CVSS2向量为字典格式。
    """
    elements = vector.split('/')
    parsed_elements = {}
    for element in elements:
        key, value = element.split(':')
        parsed_elements[key] = value
    return parsed_elements


def correct_cvss2_vector(vector):
    """
    更正CVSS2向量的顺序并检查有效性。
    :param vector: 向量
    :return:
    """
    parsed_elements = parse_cvss2_vector(vector)

    if not is_valid_cvss2_vector(parsed_elements):
        return {"state": False}

    corrected_vector = []
    for key in cvss2_vector_structure.keys():
        if key in parsed_elements:
            corrected_vector.append(f"{key}:{parsed_elements[key]}")
    if not cvss2_pattern.match('/'.join(corrected_vector)):
        return {"state": False}

    n_vector = '/'.join(corrected_vector)
    try:
        score = float(CVSS2(n_vector).base_score)
    except Exception as e:
        return {"state": False}
    return {"state": True, "vector": n_vector, "score": score}


def json_data_to_cvss20_vector(json_data):
    # 生成目标字符串
    result = []
    for key, value in json_data.items():
        short_key = cvss20_vector_fullnames.get(key)
        if short_key:
            short_value = cvss20_full_values.get(short_key, {}).get(value)
            if short_value:
                result.append(f'{short_key}:{short_value}')
            else:
                return {'state': False, 'message': f'Value "{value}" for "{key}" is not valid'}
    if not result:
        return {'state': False, 'message': 'No valid values found'}
    # 使用斜杠分隔字段
    output = "/".join(result)
    return correct_cvss2_vector(output)


def query_severity(score):
    if 10 >= score >= 9:
        severity = '超危'
    elif 9 > score >= 7:
        severity = '高危'
    elif 7 > score >= 4:
        severity = '中危'
    elif 4 > score >= 0:
        severity = '低危'
    else:
        severity = '未定义'
    return severity


if __name__ == '__main__':
    pass
    # 测试2
    # vectors = [
    #     "AV:A/AC:M/E:POC/RL:TF/RC:C/CDP:L/TD:M/CR:M/IR:M/AR:L/Au:M/C:P/I:C/A:P"
    # ]
    #
    # for vector in vectors:
    #     corrected_vector = correct_cvss2_vector(vector)
    #     print(corrected_vector)

    # 'CVSS:3.0/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:N/E:P/RL:O/RC:R'
    #
    # # 测试3
    # vectors = [
    #     "AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:N/E:P/RL:O/RC:R"
    # ]
    #
    # for vector in vectors:
    #     corrected_vector = correct_cvss3_vector(vector, 3.0)
    #     print(corrected_vector)

    # # 测试4.0
    # vectors = [
    #     # "AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"
    #     "AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/MAV:N"
    # ]
    #
    # for vector in vectors:
    #     corrected_vector = correct_cvss4_vector(vector)
    #     print(corrected_vector)
