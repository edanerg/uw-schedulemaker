import re

####
# Terminology
# 1. Course Code e.g. CS, PMATH, CO ...
# 2. Course Number e.g. 350, 350C
####

#### MAIN Function

# Given a list of course taken by the user and the prerequisites (in original form from database),
# returns true if the user satisfies
# the prerequisites requirement, false otherwise
# e.g. check_prereq(["PHYS 334", "PHYS 364", "PHYS 365", "AMATH 332"],
#                   "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)") => True
#      check_prereq(["PHYS 334", "PHYS 364"],
#                   "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)")) => False


def check_prereq(course_taken, prereq):
    for i in range(len(course_taken)):
        course_taken[i] = re.sub(pattern=r"\W", repl="", string=course_taken[i])
        course_taken[i] = course_taken[i].upper()
    parsed_prereq = prereq_parser(prereq)
    return check_prereq_recursive(course_taken, parsed_prereq)

####

#### Helper Function


# A function to check if input is a number or numeric string
def is_numeric(input):
    if type(input) == int:
        return True
    elif type(input) == str:
        return input.isnumeric()
    return False


# A function to parse the prerequisites string
def prereq_parser(prereq):

    ####
    # 1. Clean up and format string prereq
    ####

    prereq = re.sub(pattern=r"([\/,;])", repl=r"\1 ", string=prereq)  # adding space after , or ;

    # match any potential course pattern e.g CS350
    match = re.search(pattern=r"^.*[0-9]{2,3}(?!%)[A-Z\)]*(.*\))*", string=prereq)
    if match:
        prereq = match.group(0) # the entire match
    else:
        return [] # return empty list for strings with no course pattern e.g. "Art students only"

    # add "and" in front of "," or " " of the sentence one|two|three|1|2|3 of ...
    # e.g. NE 122,  1 of PHYS 112, 122 => NE 122 and 1 of PHYS 112, 122
    prereq = re.sub(pattern=r"(,\s*)(one|two|three|four|1|2|3|4)( of)", repl=r" and \2\3", string=prereq, flags=re.IGNORECASE)

    # for course number that are preceded by more than one course code, split the course code on seperator
    # and add the course number after each course number
    # e.g. CS/CO 350 => CS350/CO350
    while True:
        temp = re.sub(pattern=r"([A-Z]{2,})([,\/\s]+[^0-9]+)([0-9]{2,3})",
                      repl=r"\1 \3\2\3", string=prereq)
        if prereq == temp:
            break
        prereq = temp

    # add course code to course number that are not preceded by course code
    # e.g.  CO 250 350 352 255 355 => CO 250 CO 350 CO 352 CO 255 CO 355
    while True:
        temp = re.sub(pattern=r"^(^|.*[^A-Z])([A-Z]{2,})(([^A-Z][A-Z]?)+)([\/\s]+)([0-9]{2,3}(?!%))",
                      repl=r"\1\2\3\5\2 \6", string=prereq)
        if prereq == temp:
            break
        prereq = temp

    return prereq_parser_recursive(prereq)


# recursive function for prereq_parser
def prereq_parser_recursive(prereq):
    # Remove any white space in the beginning and end of the prereq
    prereq = prereq.strip()

    # Remove extra parentheses from prereq / remove parenthesis from prereq if prereq has only one condition
    # e.g. ((PHY 334 ...)) => PHY 334 ...
    match = re.search(pattern=r"^\(([^\(\)]+|(\(.+\).*)*)\)$", string=prereq)
    if match:
        return prereq_parser_recursive(match.group(1))

    # the 1 in the list indicates an or condition
    sepdict = {r";": [], r"and": [], r"\&": [], r"": [], r",": [], r"or": [1], r"\/": [1]}
    numdict = {"one": 1, "two": 2, "three": 3, "four": 4, "1": 1, "2": 2, "3": 3, "4": 4}

    for sep, template_list in sepdict.items():
        if sep == "":
            # for any sentence that starts with one|two|... of
            match = re.search(pattern=r"^(one|two|three|1|2|3) of(.+)$",
                              string=prereq, flags=re.IGNORECASE)

            if match:
                token = match
                token_1 = token.group(1)
                token_2 = token.group(2)
                # for sentences after "one|two|three|1|2|3 of " , replace all instances of "," into "or" and recurse
                # into the sentence after "one|two|three|1|2|3 of "
                list_temp = prereq_parser_recursive(re.sub(pattern=r",(?=[^\)]*(?:\(|$))", repl=r" or", string=token_2))
                if len(list_temp) == 1:  # Case: 1 course/ number
                    return list_temp
                else: # Case: more than 1: covert the first token into number and append the requirements
                    return [numdict[token_1.lower()]] + list_temp[1:]

        else:
            # Tokenize prereq by spliting prereq on sep
            # e.g. prereq = AMATH 331/ PMATH 331 => tokens = [AMATH 331, PMATH 331]
            pattern = sep + r"(?=[^\)]*(?:\(|$))"
            tokens = list(filter(None, re.split(pattern=pattern, string=prereq, flags=re.IGNORECASE)))
            if tokens[0] != prereq:
                result = []
                for token in tokens:
                    parsed_token = prereq_parser_recursive(token)
                    template_list_empty = not template_list # true if template_list is empty
                    # skip if parsed token is empty or contains only 1 number
                    if not parsed_token or (len(parsed_token) == 1 and is_numeric(parsed_token[0])):
                        continue
                    if (template_list_empty and is_numeric(parsed_token[0])) or (not template_list_empty and len(parsed_token) > 1):
                        parsed_token = [parsed_token]
                    result = result + parsed_token

                return template_list + result

    prereq = re.sub(pattern=r"\W", repl="", string=prereq) # remove any non-word characters e.g space e.g "CS 348" => "CS348"
    match = re.search(pattern=r"[A-Z]{2,}[0-9]{2,3}[A-Z]*", string=prereq) # search for course code + course number pattern in prereq
    if match:
        return [match.group(0)]
    else:
        return


# recursive function for check_prereq_recursive
def check_prereq_recursive(course_taken, parsed_prereq):
    if not parsed_prereq:
        return True
    num_requirement = 0 # keeps track of number of requirements needed to satisfy prerequisites
    if is_numeric(parsed_prereq[0]):
        num_requirement = parsed_prereq[0]
    else:
        num_requirement = len(parsed_prereq)

    for i in range(len(parsed_prereq)):
        if num_requirement == 0:
            return True
        if num_requirement > (len(parsed_prereq) - i):
            return False
        if is_numeric(parsed_prereq[i]):
            if i == 0:
                continue
            else:
                print("WARNING: ERROR IN PARSING PREREQUISITES!\n")
                return
        if type(parsed_prereq[i]) == list:
            result = check_prereq_recursive(course_taken, parsed_prereq[i])
            if result:
                num_requirement -= 1
        elif type(parsed_prereq[i]) == str:
            result = parsed_prereq[i] in course_taken
            if result:
                num_requirement -= 1
        else:
            print("WARNING: ERROR IN PARSING PREREQUISITES, ENCOUNTER UNSUPPORTED TYPE IN PARSING PARSED_PREREQUISITES\n")

    return num_requirement == 0


####

#### TESTS
assert(check_prereq(["PHYS 334", "PHYS 364", "PHYS 365", "AMATH 332"],
                    "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)"))
assert(not check_prereq(["PHYS 334", "PHYS 364"],
                        "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)"))
assert(check_prereq(["PHYS 334", "PHYS 364", "AMATH 332", "AMATH 353"],
                    "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)"))
assert(not check_prereq(["PHYS 334", "PHYS 364", "AMATH 332"],
                        "PHYS 334 or AMATH 373; PHYS 364 or AMATH 351; PHYS 365 or (AMATH 332 and 353)"))

assert(check_prereq(["AMATH 331"],
                    "AMATH/PMATH 331 or PMATH 351; Not open to General Mathematics students"))
assert(check_prereq(["PMATH 331"],
                    "AMATH/PMATH 331 or PMATH 351; Not open to General Mathematics students"))
assert(not check_prereq(["PMATH 352"],
                        "AMATH/PMATH 331 or PMATH 351; Not open to General Mathematics students"))
assert(check_prereq(["PMATH 351"],
                    "AMATH/PMATH 331 or PMATH 351; Not open to General Mathematics students"))
assert(not check_prereq([],
                        "AMATH/PMATH 331 or PMATH 351; Not open to General Mathematics students"))

assert(check_prereq(["CO 350", "CO352", "MATH138"],
                    "(One of CO 250/350, 352, 255/355, CM 340) and MATH 128 with a grade of at least 70% or MATH 138 or 148; Not open to General Mathematics students"))
assert(check_prereq(["CO 350", "CO352", "MATH128"],
                    "(One of CO 250/350, 352, 255/355, CM 340) and MATH 128 with a grade of at least 70% or MATH 138 or 148; Not open to General Mathematics students"))
assert(check_prereq(["CO 350", "MATH128"],
                    "(One of CO 250/350, 352, 255/355, CM 340) and MATH 128 with a grade of at least 70% or MATH 138 or 148; Not open to General Mathematics students"))
assert(not check_prereq(["CO 350"],
                        "(One of CO 250/350, 352, 255/355, CM 340) and MATH 128 with a grade of at least 70% or MATH 138 or 148; Not open to General Mathematics students"))

assert(check_prereq(["NE 122", "PHYS112", "SYDE111", "SYDE112", "PHYS252"],
                    "1 of PHYS 112,122,125, ECE106,(NE 122, 1 of PHYS 112,122,125,ECE 126);1 of MATH128,138,148,(SYDE 111,112);1 of PHYS 233,234,(1 of PHYS224,241,242, 252),256,280,380,ECE 209,370,375,NE 232,241,SYDE 283,AMATH 231,373,CM 473, CS 473, CHEM/BIO 209, 356"))
assert(not check_prereq(["NE 122", "PHYS112", "SYDE111", "SYDE112", "PHYS252"],
                        "3 of PHYS 112,122,125, ECE106,(NE 122, 1 of PHYS 112,122,125,ECE 126);1 of MATH128,138,148,(SYDE 111,112);1 of PHYS 233,234,(1 of PHYS224,241,242, 252),256,280,380,ECE 209,370,375,NE 232,241,SYDE 283,AMATH 231,373,CM 473, CS 473, CHEM/BIO 209, 356"))
####

#### REFERENCES
# https://github.com/uWaterloo/Parsers
####