import re


inputstring = \
"""
void test(void) {
55                   push        rbp
48 83 EC 30          sub         rsp,30h
48 8D 6C 24 20       lea         rbp,[rsp+20h]
48 89 04 24          mov         qword ptr [rsp],rax
48 C7 C0 2C 00 00 00 mov         rax,2Ch
C7 04 04 CC CC CC CC mov         dword ptr [rsp+rax],0CCCCCCCCh
48 83 E8 04          sub         rax,4
48 83 F8 04          cmp         rax,4
7F EF                jg          test+15h (07FF614841351h)
48 8B 04 24          mov         rax,qword ptr [rsp]
C7 04 24 CC CC CC CC mov         dword ptr [rsp],0CCCCCCCCh
C7 44 24 04 CC CC CC CC mov         dword ptr [rsp+4],0CCCCCCCCh
48 89 5D 00          mov         qword ptr [rbp],rbx
	__asm {
		push rax;
50                   push        rax
		push rbx;
53                   push        rbx

		pop rbx;
5B                   pop         rbx
		pop rax;
58                   pop         rax
	}
}
"""

output = \
"""
BYTE shellcode[{bytes}] = {{\n\
{byte_block}
}};
"""

content = ""

regex = r"^([0-9,A-F ]{2,})(.*)"


reg = re.compile(regex, re.MULTILINE)


lines = reg.findall(inputstring)
print(inputstring)

block = ''
number_of_bytes = 0
for line in lines:
    print(line)
    formatted_line = '\t'
    bytes_on_line = line[0].strip().split(' ')
    number_of_bytes += len(bytes_on_line)
    for opcode in line[0].strip().split(' '):
        formatted_line += '0x' + str(opcode) + ', '
    formatted_line += " "*((60 - len(bytes_on_line)*6)) + "//" + line[1].strip() + '\n'
    block += formatted_line


print(output.format(bytes=number_of_bytes,byte_block=block))