import re


inputstring = \
"""
volatile void stump(void) {
	char a = 0;
88 44 24 24          mov         byte ptr [rsp+24h],al
	char b = 0;
88 44 24 25          mov         byte ptr [rsp+25h],al

	__asm {
		mov rax, [a];
48 8A 44 24 24       mov         al,byte ptr [rsp+24h]
		mov rbx, [b];
48 8A 5C 24 25       mov         bl,byte ptr [rsp+25h]
		mov [b], rax;
48 88 44 24 25       mov         byte ptr [rsp+25h],al
		mov [a], rbx;
48 88 5C 24 24       mov         byte ptr [rsp+24h],bl
	stump();
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