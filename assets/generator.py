import datetime
import random
import re
import string


def get_YearMonthDay_from_Date(date):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    splitter = '/' if date.find('/') > 0 else '-'
    if re.match(pattern, date) is not None:
        ymd = date.split(splitter)
    else:
        ymd = date.split(splitter)[::-1]

    return ymd


def generate_Date(v1, v2, v3):
    print('generate_Date v1=' + v1 + ' v2=' + v2)
    if v1 != '' and v2 != '':

        ymd1 = get_YearMonthDay_from_Date(v1)
        ymd2 = get_YearMonthDay_from_Date(v2)

        start_date = datetime.date(int(ymd1[0]), int(ymd1[1]), int(ymd1[2]))
        end_date = datetime.date(int(ymd2[0]), int(ymd2[1]), int(ymd2[2]))

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return str(random_date)

    else:
        print("Data não foi preenchida corretamente.")
        return False


def generate_String(value, qtd):
    signs_without_quotes = string.punctuation[0:1] + string.punctuation[2:]  # remove simbolo: "
    signs_without_quotes = signs_without_quotes[0:5] + signs_without_quotes[6:]  # remove simbolo: '

    if (qtd.find('~') == -1):
        num = int(qtd)
    else:
        vals = qtd.replace(" ", "").split('~')
        num = random.randint(int(vals[0]), int(vals[1]))

    if len(value) > 1:
        values = value.replace(" ", "").split(',')
        value = values[random.randint(1, len(values)) - 1]

    if value.casefold() == "signs" or value.casefold() == "sign":
        return ''.join([random.choice(signs_without_quotes) for n in range(num)])

    elif value.casefold() == "alphanumerics" \
            or value.casefold() == "alphanumeric" \
            or value.casefold() == "numbers/letters":
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(num)])

    elif value.casefold() == "any" \
            or value.casefold() == "all" \
            or value.casefold() == "any character" \
            or value.casefold() == "any_character" \
            or value.casefold() == "anycharacter":
        return ''.join([random.choice(string.ascii_letters + string.digits + signs_without_quotes) for n in range(num)])

    elif value.casefold() == "numbers" or value.casefold() == "number":
        return ''.join([random.choice(string.digits) for n in range(num)])

    elif value.casefold() == "letters" or value.casefold() == "letter":
        return ''.join([random.choice(string.ascii_letters) for n in range(num)])
    else:
        return value * num


def generate_int(v1, v2, v3):
    if (v1 != '' and v2 != '' and v3 != ''):
        a = random.randint(int(v1), int(v2))
        vals = v3.replace(" ", "").split(';')
        b = random.randint(0, len(vals))
        if (b == 0):
            return str(a)
        else:
            return str(vals[b - 1])

    elif (v1 != '' and v2 != ''):
        return str(int(random.uniform(int(v1), int(v2))))

    else:
        vals = v3.replace(" ", "").split(';')
        return str(int(random.uniform(0, len(vals) - 1)))


def generate_decimal_numbers(type_name, v1, v2, v3):
    if (v1 != '' and v2 != '' and v3 != ''):
        a = random.uniform(float(v1), float(v2))
        vals = v3.replace(" ", "").split(';')
        b = random.randint(0, len(vals))
        if (b == 0):
            if (type_name == 'double'):
                return str(round(a, 6))
            else:
                return str(round(a, 3))

        else:
            if (type_name == 'double'):
                return str(round(float(vals[b - 1]), 6))
            else:
                return vals[random.randint(0, len(vals) - 1)]

    elif (v1 != '' and v2 != ''):
        if (type_name == 'double'):
            return str(round(random.uniform(float(v1), float(v2)), 6))
        else:
            return str(round(random.uniform(float(v1), float(v2)), 3))

    else:
        vals = v3.replace(" ", "").split(';')
        return vals[random.randint(0, len(vals) - 1)]


def generate_param_value(MUT, i, j):  # i = parameter order / j = testset order
    if (MUT.params[i].type_name == 'String'):
        vals1 = MUT.testsets[j].ranges[i].v1[1:len(MUT.testsets[j].ranges[i].v1) - 1].replace(" ", "").split('][')
        vals2 = MUT.testsets[j].ranges[i].v2[1:len(MUT.testsets[j].ranges[i].v2) - 1].replace(" ", "").split('][')

        content = ''
        for x in range(0, len(vals1)):
            content += generate_String(vals1[x], vals2[x])
        return '\"' + content + '\"'

    elif (MUT.params[i].type_name == 'char'):
        vals = MUT.testsets[j].ranges[i].v1.replace(" ", "").split(';')
        opcoes = ''
        for x in range(0, len(vals)):
            opcoes += generate_String(vals[x], '1')
        return "\'" + opcoes[random.randint(0, len(opcoes) - 1)] + "\'"

    elif (MUT.params[i].type_name == 'int'):
        return generate_int(MUT.testsets[j].ranges[i].v1, MUT.testsets[j].ranges[i].v2, MUT.testsets[j].ranges[i].v3)

    elif MUT.params[i].type_name == 'double' or MUT.params[i].type_name == 'float':
        return generate_decimal_numbers(MUT.params[i].type_name,
                                        MUT.testsets[j].ranges[i].v1,
                                        MUT.testsets[j].ranges[i].v2,
                                        MUT.testsets[j].ranges[i].v3)

    elif MUT.params[i].type_name == 'Date':
        return generate_Date(MUT.testsets[j].ranges[i].v1, MUT.testsets[j].ranges[i].v2, MUT.testsets[j].ranges[i].v3)

    else:  # boolean
        if (MUT.testsets[j].ranges[i].v1.casefold() == "true"):
            return "true"
        else:
            return "false"


def header_content(MUT):
    content = ''
    if (MUT.package_name != ''):
        content += "package " + MUT.package_name + ";\n"
    content += "import org.junit.*;\nimport static org.junit.Assert.assertTrue;\n\npublic class "
    content += MUT.class_name + "Test extends " + MUT.class_name + "{\n"
    return content


def generate_expected_output(MUT, i):  # i = testset order
    signs_without_quotes = r"""!#$%&()*+,-.\\\/:;<=>?@\[\]^_`{|}~"""

    v1 = MUT.testsets[i].expected_range.v1
    v2 = MUT.testsets[i].expected_range.v2
    v3 = MUT.testsets[i].expected_range.v3
    content = '^'
    if MUT.output_type == 'String':
        substr = v1[1:len(v1) - 1].replace(" ", "").split('][')
        qtd_range = v2[1:len(v2) - 1].replace(" ", "").split('][')

        for x in range(0, len(substr)):
            if substr[x] == 'numbers':
                content += '[0-9]'
            elif substr[x] == 'letters':
                content += '[a-zA-Z]'
            elif substr[x] == 'numbers/letters' or substr[x] == 'alphanumerics' or substr[x] == 'alphanumeric':
                content += '[a-zA-Z0-9]'
            elif substr[x].casefold() == "any" \
                or substr[x].casefold() == "all" \
                or substr[x].casefold() == "any character" \
                or substr[x].casefold() == "any_character" \
                or substr[x].casefold() == "anycharacter":
                content += '.'
            elif substr[x].casefold() == "signs" or substr[x].casefold() == "sign":
                content += '[' + signs_without_quotes + ']'
            else:
                content += '(' + substr[x] + ")"
            qtd_ini, qtd_fim = qtd_range[x].split('~')

            content += '{' + qtd_ini + ',' + qtd_fim + '}'

        content = 'retorno.matches(\"' + content + '$\")'

    elif (MUT.output_type == 'char'):
        vals = v1.replace(" ", "").split(';')
        opcoes = ''
        for x in range(0, len(vals)):
            opcoes += generate_String(vals[x], '1')
        provided_chars = v1.replace(" ", "").split(';')
        for character in provided_chars:
            if content != '':
                content += ' || retorno == \'' + character + '\''
            else:
                content += 'retorno == \'' + character + '\''

    elif (MUT.output_type == 'boolean'):

        if (v1.casefold() == "true"):
            content += "retorno"
        else:
            return "!retorno"

    else:  # if (MUT.output_type == 'int' or MUT.output_type == 'double' or MUT.output_type == 'float'):
        if (v1 != '' and v2 != ''):
            content = '(retorno >= ' + v1 + ' && retorno <= ' + v2 + ')'
        if (v3 != ''):
            vals = v3.replace(" ", "").split(';')
            for x in range(0, len(vals)):
                if (content != ''):
                    content += ' || retorno == ' + vals[x]
                else:
                    content += 'retorno == ' + vals[x]

    return content


def test_content(MUT, test_set_name, cont, testset_position):
    content = "\n\t@Test\n\tpublic void " + test_set_name + str(cont) + "() {\n\t\t"
    content += MUT.output_type + " retorno = " + MUT.name + "("

    # TO DO: gerar valores
    for x in range(0, len(MUT.params)):
        if (x == 0):
            content += generate_param_value(MUT, x, testset_position)
        else:
            content += ", " + generate_param_value(MUT, x, testset_position)

    content += ");\n\t\tassertTrue("
    content += generate_expected_output(MUT, testset_position)
    content += ");\n\t}\n"
    return content


def replaceMethodNameWithPlaceholder(test_method_str):
    pattern = r'@Test\s+public\s+void\s+\w+\s*\(\)\s*\{'
    return re.sub(pattern, '@Test\n\tpublic void METHODNAME() {', test_method_str)


def methodDoesNotExistYet(testMethodGenerated, methodsAlreadyWritten):
    method_str_under_verif = replaceMethodNameWithPlaceholder(testMethodGenerated)
    return all(replaceMethodNameWithPlaceholder(method) != method_str_under_verif for method in methodsAlreadyWritten)


def generate_tests(MUT, file_path=''):
    file_location = file_path + ('' if file_path.endswith('/') else '/') + MUT.class_name + 'Test.java'
    testfile = open(file_location, 'a+')
    testfile.seek(0)
    previous = testfile.readlines()

    if len(previous) == 0:
        testfile.write(header_content(MUT))
    else:
        testfile.seek(0)
        testfile.truncate()
        testfile.write(''.join([a for a in previous[:-1]]))

    cont = 1
    for i in range(0, len(MUT.testsets)):
        methodsAlreadyWritten = []
        retries = 1000
        j = 0
        while j < MUT.testsets[i].number_of_cases:
            j += 1
            testMethodGenerated = test_content(MUT, MUT.testsets[i].name, cont, i)
            if methodDoesNotExistYet(testMethodGenerated, methodsAlreadyWritten):
                testfile.write(testMethodGenerated)
                methodsAlreadyWritten.append(testMethodGenerated)
                cont += 1
            elif retries != 0:
                j -= 1
                retries -= 1

    testfile.write("\n}")
    testfile.close()
