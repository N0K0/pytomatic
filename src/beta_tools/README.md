
# Content of the folder
The contents of this folder is generally not directly related to the pytomatic project in large or,
not up to a standar where i want to make them "official".
This is a place to dump small helper tools that i'm been using in the development of personal scripts.

## Overview of the tools

### Shelly
A simple pythonscript to extract and format the shellcode given in an output-dump from visual studio

**Input:**
```     
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
```
**Output:**

```
char *shellcode = 	"\x55"                                  // push        rbp
	"\x48\x83\xEC\x30"                      // sub         rsp,30h
	"\x48\x8D\x6C\x24\x20"                  // lea         rbp,[rsp+20h]
	"\x48\x89\x04\x24"                      // mov         qword ptr [rsp],rax
	"\x48\xC7\xC0\x2C\x00\x00\x00"          // mov         rax,2Ch
	"\xC7\x04\x04\xCC\xCC\xCC\xCC"          // mov         dword ptr [rsp+rax],0CCCCCCCCh
	"\x48\x83\xE8\x04"                      // sub         rax,4
	"\x48\x83\xF8\x04"                      // cmp         rax,4
	"\x7F\xEF"                              // jg          test+15h (07FF614841351h)
	"\x48\x8B\x04\x24"                      // mov         rax,qword ptr [rsp]
	"\xC7\x04\x24\xCC\xCC\xCC\xCC"          // mov         dword ptr [rsp],0CCCCCCCCh
	"\xC7\x44\x24\x04\xCC\xCC\xCC\xCC"      // mov         dword ptr [rsp+4],0CCCCCCCCh
	"\x48\x89\x5D\x00"                      // mov         qword ptr [rbp],rbx
	"\x50"                                  // push        rax
	"\x53"                                  // push        rbx
	"\x5B"                                  // pop         rbx
	"\x58"                                  // pop         rax
;
```