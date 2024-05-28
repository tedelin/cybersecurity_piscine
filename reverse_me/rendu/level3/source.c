#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


void yes() {
	puts("Good job.");
	return;
}
void no() {
	puts("Nope.");
	exit(1);
}


int main() {
	char input[48];
	char ref[9];
	bool varr;
	printf("Please enter key: ");
	int res = scanf("%s", input);
	if (res != 1)
		no();
	if (input[1] != '2')
		no();
	if (input[0] != '4')
		no();
	fflush(stdin);
	memset(ref, 0, 9);
	ref[0] = '*';
	int counter = 2;
	int idx = 1;
	while (1) {
		int len_ref = strlen(ref);
		varr = false;
		if (len_ref < 8) {
			len_ref = strlen(input);
			varr = counter < len_ref; 
		}
		if (!varr) break;
		char input_char[4] = {input[counter], input[counter + 1], input[counter + 2], 0};
		int input_int = atoi(input_char);
		ref[idx] = (char)input_int;
		counter += 3;
		idx += 1;
	}
	ref[idx] = 0;
	int cmp = strcmp(ref, "********");
	if (cmp == 0)
		yes();
	else
		no();
}
